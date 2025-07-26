
# Create your models here.
from django.db import models
from django_softdelete.models import SoftDeleteModel
from django.conf import settings
from notification_app.models import Log
from django.utils import timezone

import shop_app

class Category(SoftDeleteModel):
    """C'est une catégorie de produits, par exemple: Fruits, Légumes, etc."""
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shop = models.ForeignKey(shop_app.models.Shop, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        unique_together = ('nom', 'shop')

class Product(SoftDeleteModel):
    def product_image_upload_to(instance, filename):
        return f'products/{instance.shop.id}/{filename}'
    
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    prix = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    image = models.ImageField(upload_to=product_image_upload_to, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    shop = models.ForeignKey('shop_app.Shop', on_delete=models.CASCADE, related_name='products')
    expiration_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stock_threshold = models.PositiveIntegerField(default=5)
    
    def is_expired(self):
        """Vérifie si le produit est périmé"""
        if self.expiration_date:
            return self.expiration_date < timezone.now().date()
        return False
    
    def change_stock(self, quantite, raison, user=None):
        """Change le stock du produit et log l'action"""
        self.stock += quantite
        self.save()
        Log.objects.create(user=user, action=f'Stock de {self.nom} changé de {quantite} pour la raison: {raison}')
    def is_low_stock(self):
        return self.stock <= self.stock_threshold

    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        unique_together = ('nom', 'shop')
    
class ProductPacket(Product):
    """C'est un paquet de produits, peut être un carton, un sac, d'un même produit"""
    product = models.ForeignKey(Product, related_name='packets', on_delete=models.CASCADE)
    nombre_de_produits = models.PositiveIntegerField(default=2)
    
    def deballer(self, quantite=1, user=None):
        """Déballer le paquet, décrémente le nombre de paquets et crée des produits individuels, incrementant le stock du shop"""
        if self.stock >= quantite:
            self.stock -= quantite
            self.product.change_stock(self.nombre_de_produits * quantite, f'Déballé un {self.nom} en {self.nombre_de_produits}  {self.product.nom} ', user=user)
            self.product.save()
            self.save()
            return True
        return False
    
class Panier(SoftDeleteModel):
    """C'est un panier de produits, peut être un paquet ou un produit individuel"""
    client = models.ForeignKey('shop_app.Client', on_delete=models.CASCADE, related_name='paniers')
    shop = models.ForeignKey('shop_app.Shop', on_delete=models.CASCADE, related_name='paniers')
    prix_total = models.PositiveIntegerField(default=0)
    est_paye = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def get_prix_total(self):
        """Calculer le prix total du panier"""
        # Calculer le prix total en sommant les prix de chaque commande dans le panier
        self.prix_total = sum(commande.get_prix_total() for commande in self.commandes.all())
        if not self.id:
            self.save()
        return self.prix_total

    def payer(self, user=None):
        """Marquer le panier comme payé et mettre à jour le stock des produits"""
        if not self.est_paye:
            for commande in self.commandes_set.all():
                if commande.est_paye or commande.payer(user=user):
                    pass
                else:
                    return False
            self.est_paye = True
            self.save()
            # Log the action
            Log.objects.create(user=user, action=f'Panier de {self.client.nom} payé')
            return True
        return False
    
    def save(self, *args, **kwargs):
        """Override save to update the total price before saving"""
        super().save(*args, **kwargs)
        # self.prix_total = self.get_prix_total()
        
    def __str__(self):
        return f'Panier de  {self.client.nom}'
    
    

class Commande(SoftDeleteModel):
    """C'est une commande de produits, peut être un paquet ou un produit individuel"""
    client = models.ForeignKey('shop_app.Client', on_delete=models.CASCADE, related_name='commandes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='commandes')
    quantite = models.PositiveIntegerField(default=1)
    shop = models.ForeignKey('shop_app.Shop', on_delete=models.CASCADE, related_name='commandes')
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name='commandes', null=True, blank=True)
    prix_total = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    est_paye = models.BooleanField(default=False)
    
    
    def esy_payable(self):
        """Vérifie si la commande est payable"""
        if self.product.stock >= self.quantite and not self.est_paye:
            return True
        return False
    def payer(self, user=None):
        """Marquer la commande comme payée et mettre à jour le stock du produit"""
        if  self.est_payable():
            self.est_paye = True
            self.product.change_stock(-self.quantite, 'Commande payée', user=user)
            if self.product.is_low_stock():
                Log.objects.create(user=user, action=f'Produit {self.product.nom} en stock faible')
            self.save()
            # Log the action
            Log.objects.create(user=user, action=f'Commande de {self.quantite} {self.product.nom} payée')
            return True
        return False
    
    def get_prix_total(self):
        """Calculer le prix total de la commande"""
        self.prix_total =  self.quantite * self.product.prix
        self.save()
        return self.prix_total

    def __str__(self):
        return f'Commande de {self.quantity} {self.product.nom} par {self.user.username}'



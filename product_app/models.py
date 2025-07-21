
# Create your models here.
from django.db import models
from django_softdelete.models import SoftDeleteModel
from django.conf import settings
from notification_app.models import Log

class Category(SoftDeleteModel):
    """C'est une catégorie de produits, par exemple: Fruits, Légumes, etc."""
    nom = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Product(SoftDeleteModel):
    def product_image_upload_to(instance, filename):
        return f'products/{instance.shop.id}/{filename}'
    
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    prix = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to=product_image_upload_to, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    shop = models.ForeignKey('shop_app.Shop', on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stock_threshold = models.PositiveIntegerField(default=5)

    def is_low_stock(self):
        return self.stock <= self.stock_threshold

    def __str__(self):
        return self.nom
    
class ProductPacket(SoftDeleteModel, Product):
    """C'est un paquet de produits, peut être un carton, un sac, d'un même produit"""
    product = models.ForeignKey(Product, related_name='packets', on_delete=models.CASCADE)
    nombre_de_produits = models.PositiveIntegerField(default=2)
    
    def deballer(self, user):
        """Déballer le paquet, décrémente le nombre de paquets et crée des produits individuels, incrementant le stock du shop"""
        if self.stock >= 1:
            self.stock -= 1
            self.product.stock += self.nombre_de_produits
            self.product.save()
            self.save()
            # Log the action
            Log.objects.create(user=user, action=f'Déballé un {self.nom} en {self.nombre_de_produits}  {self.product.nom} ')
            return True
        return False
    
class Panier(SoftDeleteModel):
    """C'est un panier de produits, peut être un paquet ou un produit individuel"""
    client = models.ForeignKey('shop_app.Client', on_delete=models.CASCADE, related_name='paniers')
    prix_total = models.PositiveIntegerField(default=0)
    est_paye = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def get_prix_total(self):
        """Calculer le prix total du panier"""
        if self.prix_total:
            return self.prix_total
        # Calculer le prix total en sommant les prix de chaque commande dans le panier
        self.prix_total = sum(commande.get_prix_total() for commande in self.commandes_set.all())
        self.save()
        return self.prix_total

    def payer(self, user=None):
        """Marquer le panier comme payé et mettre à jour le stock des produits"""
        if not self.est_paye:
            for commande in self.commandes_set.all():
                commande.payer(user=user)
            self.est_paye = True
            self.save()
            # Log the action
            Log.objects.create(user=user, action=f'Panier de {self.client.nom} payé')
            return True
        return False

    def __str__(self):
        return f'Panier de  {self.client.nom}'
    
    

class Commande(SoftDeleteModel):
    """C'est une commande de produits, peut être un paquet ou un produit individuel"""
    client = models.ForeignKey('shop_app.Client', on_delete=models.CASCADE, related_name='commandes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='commandes')
    quantite = models.PositiveIntegerField(default=1)
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name='commandes', null=True, blank=True)
    prix_total = models.PositiveIntegerField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    est_paye = models.BooleanField(default=False)
    
    def payer(self, user=None):
        """Marquer la commande comme payée et mettre à jour le stock du produit"""
        if not self.est_paye:
            self.est_paye = True
            self.product.stock -= self.quantite
            self.product.save()
            if self.product.is_low_stock():
                Log.objects.create(user=user, action=f'Produit {self.product.nom} en stock faible')
            self.save()
            # Log the action
            Log.objects.create(user=user, action=f'Commande de {self.quantite} {self.product.nom} payée')
            return True
        return False
    
    def get_prix_total(self):
        """Calculer le prix total de la commande"""
        if self.prix_total:
            return self.prix_total
        self.prix_total =  self.quantite * self.product.prix
        self.save()
        return self.prix_total

    def __str__(self):
        return f'Commande de {self.quantity} {self.product.nom} par {self.user.username}'



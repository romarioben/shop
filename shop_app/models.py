from django.db import models
from django_softdelete.models import SoftDeleteModel

# Create your models here.
class Shop(SoftDeleteModel):
    nom = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey('auth_app.User', on_delete=models.CASCADE, related_name='shops')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    numero_telephone = models.CharField(max_length=20, blank=True, null=True)
    gerants = models.ManyToManyField('auth_app.User', related_name='gerants_shops', blank=True)

    def __str__(self):
        return self.nom + '-' + self.owner.username
    
    def creer_client_anomyme(self ):
        """Crée un client anonyme pour cette boutique"""
        client, created = Client.objects.get_or_create(nom='Anonyme', prenom='Anonyme', owner=self.owner)
        if created:
            client.save()
        return client

    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'

class Client(SoftDeleteModel):
    """C'est un client qui peut acheter des produits dans la boutique"""
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='clients')
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    numero_telephone = models.CharField(max_length=20, blank=True, null=True)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
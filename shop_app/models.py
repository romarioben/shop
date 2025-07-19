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

    def __str__(self):
        return self.nom + '-' + self.owner.username

    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'
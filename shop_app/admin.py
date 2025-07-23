from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Shop)
class ShopModelAdmin(admin.ModelAdmin):
    def gerants(self, obj):
        return ", ".join([str(gerant) for gerant in obj.gerants.all()])
    list_display = ['id','nom', 'adresse', 'numero_telephone', 'owner', 'gerants', 'created_at', 'updated_at']
    
@admin.register(models.Client)
class ClientModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'prenom', 'adresse', 'numero_telephone', 'shop', 'created_at', 'updated_at']
    search_fields = ['nom', 'prenom', 'shop__nom']
    list_filter = ['shop']
    ordering = ['-created_at']
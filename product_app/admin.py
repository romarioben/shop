from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'created_at', 'updated_at']
    search_fields = ['nom']
    ordering = ['-created_at']
    
@admin.register(models.Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'prix', 'stock', 'category', 'created_at', 'updated_at']
    search_fields = ['nom', 'category__nom']
    list_filter = ['category']
    ordering = ['-created_at']
    
@admin.register(models.ProductPacket)
class ProductPacketModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'prix', 'stock', 'nombre_de_produits', 'product', 'created_at', 'updated_at']
    search_fields = ['nom', 'product__nom']
    list_filter = ['product']
    ordering = ['-created_at']
    
@admin.register(models.Commande)
class CommandeModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'client',  'est_paye', 'produit','quantite', 'prix_total','created_at', 'updated_at']
    search_fields = ['client__nom', 'status']
    list_filter = ['est_paye']
    ordering = ['-created_at']

@admin.register(models.Panier)
class PanierModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'prix_total', 'est_paye', 'date_created', 'date_updated']
    search_fields = ['client__nom']
    list_filter = ['est_paye']
    ordering = ['-date_created']

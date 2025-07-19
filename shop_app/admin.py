from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Shop)
class ShopModelAdmin(admin.ModelAdmin):
    list_display = ['id','nom', 'adresse', 'numero_telephone', 'owner', 'created_at', 'updated_at']
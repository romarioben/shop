from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id','username', 'email', 'role', 'last_name', 'first_name','is_email_verified', 'receive_notifications', 'numero_telephone']
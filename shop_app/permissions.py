from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from shop_app.models import Shop

class ShopPermission(BasePermission):
    """
    Custom permission to only allow users with a specific role to access shop-related views.
    """
    
    def has_permission(self, request, view):
        # Check if the user is authenticated and has the required role
        user = request.user
        shop_id = view.kwargs.get('shop_id')
        shop = get_object_or_404(Shop, id=shop_id) if shop_id else None
        if shop:
            gerants = shop.gerants.all()
            if user in gerants:
                return True
        return False
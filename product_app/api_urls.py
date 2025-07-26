from django.urls import path
from . import api_views


urlpatterns = [
    path('<int:shop_id>/categories/', api_views.CategoryListCreateAPIView.as_view(), name="category-list-create"),
    path('<int:shop_id>/categories/<int:pk>/', api_views.CategoryDetailUpdateDeleteAPIView.as_view(), name="category-detail-update-delete"),
    
    path('<int:shop_id>/products/', api_views.ProductListCreateAPIView.as_view(), name="product-list-create"),
    path('<int:shop_id>/products/<int:pk>/', api_views.ProductDetailUpdateDeleteAPIView.as_view(), name="product-detail-update-delete"),
    
    path('<int:shop_id>/product-packets/', api_views.ProductPacketListCreateAPIView.as_view(), name="product-packet-list-create"),
    path('<int:shop_id>/product-packets/<int:pk>/', api_views.ProductPacketDetailUpdateDeleteAPIView.as_view(), name="product-packet-detail-update-delete"),
    
    path('<int:shop_id>/paniers/', api_views.PanierListCreateAPIView.as_view(), name="panier-list-create"),
    path('<int:shop_id>/paniers/<int:pk>/', api_views.PanierDetailUpdateDeleteAPIView.as_view(), name="panier-detail-update-delete"),
    
    path('<int:shop_id>/commandes/', api_views.CommandeListCreateAPIView.as_view(), name="commande-list-create"),
    path('<int:shop_id>/commandes/<int:pk>/', api_views.CommandeDetailUpdateDeleteAPIView.as_view(), name="commande-detail-update-delete"),
    
]
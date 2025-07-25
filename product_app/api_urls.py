from django.urls import path
from . import api_views


urlpatterns = [
    path('<int:shop_id>/categories/', api_views.CategoryListCreateAPIView.as_view(), name="category-list-create"),
    path('<int:shop_id>/categories/<int:pk>/', api_views.CategoryDetailUpdateDeleteAPIView.as_view(), name="category-detail-update-delete"),
    path('<int:shop_id>/products/', api_views.ProductListCreateAPIView.as_view(), name="product-list-create"),
    path('<int:shop_id>/products/<int:pk>/', api_views.ProductDetailUpdateDeleteAPIView.as_view(), name="product-detail-update-delete"),
    
]
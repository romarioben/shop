from django.urls import path

from . import api_views

urlpatterns = [
    path('', api_views.ShopListCreateView.as_view(), name='shop-list-create'),
    path('<int:pk>/', api_views.ShopDetailUpdateDeleteView.as_view(), name='shop-detail-update-delete'),
    path('<str:search>/', api_views.ShopNomSearchView.as_view(), name='shop-nom-search'),
    
    path('client/', api_views.ClientListCreateView.as_view(), name='client-list-create'),
    path('<int:shop_id>/client/<int:pk>/', api_views.ClientDetailUpdateDeleteView.as_view(), name='shop-detail-update-delete'),
    path('<int:shop_id>/client/<str:search>/', api_views.ClientNomSearchView.as_view(), name='shop-nom-search'),
]

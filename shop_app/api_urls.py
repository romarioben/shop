from django.urls import path

from . import api_views

urlpatterns = [
    path('', api_views.ShopListCreateView.as_view(), name='shop-list-create'),
    path('<int:pk>/', api_views.ShopDetailUpdateDeleteView.as_view(), name='shop-detail-update-delete'),
    path('<str:search>/', api_views.ShopNomSearchView.as_view(), name='shop-nom-search'),
]

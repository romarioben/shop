from django.urls import path
from . import views, api_views


urlpatterns = [
    path('<int:pk>/', api_views.UserDetailUpdateDeleteView.as_view(), name="user-detail-update-delete"),
    path('profile/', api_views.profile, name="profile"),
    path('', api_views.UserCreateView.as_view(), name="user-create"),
    path('gerant/<int:shop_id>/', api_views.ShopGerantListCreateView.as_view(), name="shop-gerant-list-create"),
]
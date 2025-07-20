from django.urls import path
from . import views, api_views


urlpatterns = [
    path('<int:pk>/', api_views.UserDetailUpdateDeleteView.as_view(), name="user-detail-update-delete"),
]
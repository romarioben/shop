from django.db import models
from django_softdelete.models import SoftDeleteModel

# Create your models here.
class Log(SoftDeleteModel):
    user = models.ForeignKey('auth_app.User', on_delete=models.SET_NULL, related_name='logs')
    action = models.CharField(max_length=400)
    date_created = models.DateTimeField(auto_now_add=True)
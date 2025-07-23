from rest_framework import serializers
from django.utils import timezone

from auth_app.models import User

from .models import Shop, Client

class ShopSerializer(serializers.ModelSerializer):
    gerants = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        many=True,
        required=False # Allow shop to be created without gerants initially
    )
    owner_name = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Shop
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'gerants')
    
    def create(self, validated_data):
        gerants_data = validated_data.pop('gerants', [])
        shop = Shop.objects.create(**validated_data)
        shop.gerants.set(gerants_data) # Use .set() here
        return shop
    
    def update(self, instance, validated_data):
        gerants_data = validated_data.pop('gerants', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if gerants_data is not None:
            instance.gerants.set(gerants_data)
        instance.updated_at = timezone.now()
        instance.save()
        return instance

class ClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        client = Client.objects.create(**validated_data)
        return client

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_at = timezone.now()
        instance.save()
        return instance
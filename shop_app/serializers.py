from rest_framework import serializers
from django.utils import timezone

from .models import Shop, Client

class ShopSerializer(serializers.ModelSerializer):
    
    owner_name = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Shop
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def create(self, validated_data):
        shop = Shop.objects.create(**validated_data)
        return shop
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
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
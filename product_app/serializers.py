from rest_framework import serializers
from .models import Product, Category, Commande, Panier, ProductPacket
from django.utils import timezone


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('id','created_at', 'updated_at')

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_at = timezone.now()
        instance.save()
        return instance

class ProductSerializer(serializers.ModelSerializer):
    category_nom = serializers.ReadOnlyField(source='category.nom')
    expired = serializers.SerializerMethodField()
    is_low_stock = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'category_nom', 'expired', 'is_low_stock')

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_at = timezone.now()
        instance.save()
        return instance
    
    def get_expired(self, obj):
        return obj.is_expired()
    
    def get_is_low_stock(self, obj):
        return obj.is_low_stock()

class ProductPacketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPacket
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_at = timezone.now()
        instance.save()
        return instance


class CommandeSerializer(serializers.ModelSerializer):
    product_nom = serializers.ReadOnlyField(source='product.nom')
    product_prix = serializers.ReadOnlyField(source='product.prix')

    class Meta:
        model = Commande
        fields = '__all__'
        read_only_fields = ('id','date_created', 'date_updated', 'est_paye', 'prix_total')

    def create(self, validated_data):
        commande = Commande.objects.create(**validated_data)
        return commande

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class PanierSerializer(serializers.ModelSerializer):
    client_nom = serializers.ReadOnlyField(source='client.nom')

    class Meta:
        model = Panier
        fields = '__all__'
        read_only_fields = ('id', 'date_created', 'date_updated', 'prix_total', 'est_paye')

    def create(self, validated_data):
        panier = Panier.objects.create(**validated_data)
        return panier

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_at = timezone.now()
        instance.save()
        return instance
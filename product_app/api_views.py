from django.shortcuts import get_object_or_404
from rest_framework import serializers

from shop_app.models import Shop
from .models import Product, Category, Commande, Panier, ProductPacket
from .serializers import CategorySerializer, ProductSerializer, ProductPacketSerializer
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

class ProductListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer 
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        shop_id = self.request.query_params.get('shop_id', None)
        shop = get_object_or_404(Shop, id=shop_id) if shop_id else None
        queryset = Product.objects.filter(shop=shop) if shop else []
        return queryset
    
    def get(self, request, shop_id, *args, **kwargs):
        """List all products of a shop"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request, *args, **kwargs):
        """Create a new product in a shop"""
        shop_id = request.data.get('shop_id')
        shop = get_object_or_404(Shop, id=shop_id)
        data = request.data.copy()
        data['shop'] = shop.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
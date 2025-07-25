from django.shortcuts import get_object_or_404
from rest_framework import serializers
from shop_app.models import Shop
from .models import Product, Category, Commande, Panier, ProductPacket
from .serializers import CategorySerializer, ProductSerializer, ProductPacketSerializer
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

class CategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        shop_id = self.kwargs.get('shop_id')
        shop = get_object_or_404(Shop, id=shop_id) if shop_id else None
        print(shop_id, shop)
        queryset = Category.objects.filter(shop=shop) if shop else []
        print(queryset)
        return queryset
    
    def get(self, request, *args, **kwargs):
        """List all categories of a shop"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request, shop_id,  *args, **kwargs):
        """Create a new category in a shop"""
        shop = get_object_or_404(Shop, id=shop_id)
        data = request.data.copy()
        data['shop'] = shop.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class CategoryDetailUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        shop_id = self.kwargs.get('shop_id')
        pk = self.kwargs.get('pk')
        shop = get_object_or_404(Shop, id=shop_id)
        category = get_object_or_404(Category, id=pk, shop=shop)
        return category
    
    def get(self, request, shop_id, pk, *args, **kwargs):
        """Retrieve a specific category"""
        category = self.get_object()
        serializer = self.get_serializer(category)
        return Response(serializer.data, status=200)
    
    def put(self, request, shop_id, pk, *args, **kwargs):
        """Update a specific category"""
        category = self.get_object()
        serializer = self.get_serializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, shop_id, pk, *args, **kwargs):
        """Partially update a specific category"""
        category = self.get_object()
        serializer = self.get_serializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, shop_id, pk, *args, **kwargs):
        """Delete a specific category"""
        category = self.get_object()
        category.delete()
        return Response(status=204)

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
    
    def post(self, request, shop_id, *args, **kwargs):
        """Create a new product in a shop"""
        shop = get_object_or_404(Shop, id=shop_id)
        data = request.data.copy()
        data['shop'] = shop.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class ProductDetailUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        shop_id = self.kwargs.get('shop_id')
        pk = self.kwargs.get('pk')
        shop = get_object_or_404(Shop, id=shop_id)
        product = get_object_or_404(Product, id=pk, shop=shop)
        return product
    
    def get(self, request, shop_id, pk, *args, **kwargs):
        """Retrieve a specific product"""
        product = self.get_object()
        serializer = self.get_serializer(product)
        return Response(serializer.data, status=200)
    
    def put(self, request, shop_id, pk, *args, **kwargs):
        """Update a specific product"""
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, shop_id, pk, *args, **kwargs):
        """Partially update a specific product"""
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, shop_id, pk, *args, **kwargs):
        """Delete a specific product"""
        product = self.get_object()
        product.delete()
        return Response(status=204)
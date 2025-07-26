from django.shortcuts import get_object_or_404
from rest_framework import serializers
from shop_app.models import Shop
from shop_app.permissions import ShopPermission
from .models import Product, Category, Commande, Panier, ProductPacket
from .serializers import CategorySerializer, CommandeSerializer, PanierSerializer, ProductSerializer, ProductPacketSerializer
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

class CategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, ShopPermission]
    
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
    permission_classes = [IsAuthenticated, ShopPermission]
    
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
    permission_classes = [IsAuthenticated, ShopPermission]
    
    def get_queryset(self):
        shop_id = self.kwargs.get('shop_id')
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
    permission_classes = [IsAuthenticated, ShopPermission]
    
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
    
class ProductPacketListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductPacketSerializer
    permission_classes = [IsAuthenticated, ShopPermission]
    
    def get_queryset(self):
        shop_id = self.kwargs.get('shop_id')
        shop = get_object_or_404(Shop, id=shop_id) if shop_id else None
        queryset = ProductPacket.objects.filter(shop=shop) if shop else []
        return queryset
    
    def get(self, request, shop_id, *args, **kwargs):
        """List all product packets of a shop"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request, shop_id, *args, **kwargs):
        """Create a new product packet in a shop"""
        shop = get_object_or_404(Shop, id=shop_id)
        data = request.data.copy()
        data['shop'] = shop.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class ProductPacketDetailUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductPacketSerializer
    permission_classes = [IsAuthenticated, ShopPermission]
    
    def get_object(self):
        shop_id = self.kwargs.get('shop_id')
        pk = self.kwargs.get('pk')
        shop = get_object_or_404(Shop, id=shop_id)
        product_packet = get_object_or_404(ProductPacket, id=pk, shop=shop)
        return product_packet
    
    def get(self, request, shop_id, pk, *args, **kwargs):
        """Retrieve a specific product packet"""
        product_packet = self.get_object()
        serializer = self.get_serializer(product_packet)
        return Response(serializer.data, status=200)
    
    def put(self, request, shop_id, pk, *args, **kwargs):
        """Update a specific product packet"""
        product_packet = self.get_object()
        serializer = self.get_serializer(product_packet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, shop_id, pk, *args, **kwargs):
        """Partially update a specific product packet"""
        product_packet = self.get_object()
        serializer = self.get_serializer(product_packet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, shop_id, pk, *args, **kwargs):
        """Delete a specific product packet"""
        product_packet = self.get_object()
        product_packet.delete()
        return Response(status=204)
    
class PanierListCreateAPIView(ListCreateAPIView):
    serializer_class = PanierSerializer
    permission_classes = [IsAuthenticated, ShopPermission]
    
    def get_queryset(self):
        shop_id = self.kwargs.get('shop_id')
        shop = get_object_or_404(Shop, id=shop_id) if shop_id else None
        queryset = Panier.objects.filter(shop=shop) if shop else []
        return queryset
    
    def get(self, request, shop_id, *args, **kwargs):
        """List all paniers of a shop"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request, shop_id, *args, **kwargs):
        """Create a new panier in a shop"""
        shop = get_object_or_404(Shop, id=shop_id)
        data = request.data.copy()
        data['shop'] = shop.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class PanierDetailUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):    
    serializer_class = PanierSerializer
    permission_classes = [IsAuthenticated, ShopPermission]
    
    def get_object(self):
        shop_id = self.kwargs.get('shop_id')
        pk = self.kwargs.get('pk')
        shop = get_object_or_404(Shop, id=shop_id)
        panier = get_object_or_404(Panier, id=pk, shop=shop)
        return panier
    
    def get(self, request, shop_id, pk, *args, **kwargs):
        """Retrieve a specific panier"""
        panier = self.get_object()
        serializer = self.get_serializer(panier)
        return Response(serializer.data, status=200)
    
    def put(self, request, shop_id, pk, *args, **kwargs):
        """Update a specific panier"""
        panier = self.get_object()
        serializer = self.get_serializer(panier, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, shop_id, pk, *args, **kwargs):
        """Partially update a specific panier"""
        panier = self.get_object()
        serializer = self.get_serializer(panier, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, shop_id, pk, *args, **kwargs):
        """Delete a specific panier"""
        panier = self.get_object()
        panier.delete()
        return Response(status=204)
    
class CommandeListCreateAPIView(ListCreateAPIView):
    serializer_class = CommandeSerializer
    permission_classes = [IsAuthenticated, ShopPermission]
    
    def get_queryset(self):
        shop_id = self.kwargs.get('shop_id')
        shop = get_object_or_404(Shop, id=shop_id) if shop_id else None
        queryset = Commande.objects.filter(shop=shop) if shop else []
        return queryset
    
    def get(self, request, shop_id, *args, **kwargs):
        """List all commandes of a shop"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request, shop_id, *args, **kwargs):
        """Create a new commande in a shop"""
        shop = get_object_or_404(Shop, id=shop_id)
        data = request.data.copy()
        data['shop'] = shop.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class CommandeDetailUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommandeSerializer
    permission_classes = [IsAuthenticated, ShopPermission]
    
    def get_object(self):
        shop_id = self.kwargs.get('shop_id')
        pk = self.kwargs.get('pk')
        shop = get_object_or_404(Shop, id=shop_id)
        commande = get_object_or_404(Commande, id=pk, shop=shop)
        return commande
    
    def get(self, request, shop_id, pk, *args, **kwargs):
        """Retrieve a specific commande"""
        commande = self.get_object()
        serializer = self.get_serializer(commande)
        return Response(serializer.data, status=200)
    
    def put(self, request, shop_id, pk, *args, **kwargs):
        """Update a specific commande"""
        commande = self.get_object()
        serializer = self.get_serializer(commande, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, shop_id, pk, *args, **kwargs):
        """Partially update a specific commande"""
        commande = self.get_object()
        serializer = self.get_serializer(commande, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, shop_id, pk, *args, **kwargs):
        """Delete a specific commande"""
        commande = self.get_object()
        commande.delete()
        return Response(status=204)
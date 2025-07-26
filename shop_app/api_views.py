from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from auth_app.permissions import EstAdminPermission
from .serializers import ClientSerializer, ShopSerializer
from .models import Client, Shop
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q



class ShopListCreateView(ListCreateAPIView):
    """
    View to list all shops or create a new shop.
    """
    permission_classes = [IsAuthenticated, EstAdminPermission]
    serializer_class = ShopSerializer

    def get_queryset(self):
        return Shop.objects.all()

    def post(self, request, *args, **kwargs):
        owner = request.user
        data = request.data.copy()
        data['owner'] = owner.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            shop = serializer.save()
        else:
            return Response(serializer.errors, status=400)
        shop.gerants.add(owner)
        return Response(serializer.data, status=201)
    
    def get(self, request, *args, **kwargs):
        owner = request.user
        shops = Shop.objects.filter(owner=owner)
        serializer = self.get_serializer(shops, many=True)
        return Response(serializer.data, status=200)

class ShopDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update or delete a shop.
    """
    permission_classes = [IsAuthenticated, EstAdminPermission]
    serializer_class = ShopSerializer

    def get_queryset(self):
        return Shop.objects.all()

    def get(self, request, pk, *args, **kwargs):
        shop = self.get_object()
        serializer = self.get_serializer(shop)
        return Response(serializer.data, status=200)

    def put(self, request, pk, *args, **kwargs):
        shop = self.get_object()
        serializer = ShopSerializer(shop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, pk, *args, **kwargs):
        shop = self.get_object()
        serializer = ShopSerializer(shop, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, *args, **kwargs):
        shop = self.get_object()
        shop.delete()
        return Response(status=204)
    
class ShopNomSearchView(ListCreateAPIView):
    """
    View to search for shops by Nom.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ShopSerializer

    def get_queryset(self):
        title = self.request.query_params.get('search', None)
        owner = self.request.user
        if title and owner:
            return Shop.objects.filter(nom__icontains=title, owner=owner)
        return Shop.objects.filter(owner=owner)

    def get(self, request, search, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)
    
class ClientListCreateView(ListCreateAPIView):
    """
    View to list all clients or create a new client.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer

    def get_queryset(self):
        """Return all clients for the authenticated user's shop."""
        shop_id = self.request.query_params.get('shop_id', None)
        if shop_id:
            return Client.objects.filter(shop__id=shop_id)
        return Client.objects.all()

    def post(self, request, shop_id, *args, **kwargs):
        """Create a new client in a shop."""
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            client = serializer.save()
            client.shop_id = shop_id
            client.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request, shop_id, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)
    
class ClientDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update or delete a client.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer

    def get_queryset(self):
        shop_id = self.request.query_params.get('shop_id', None)
        if shop_id:
            return Client.objects.filter(shop__id=shop_id)
        return Client.objects.all()

    def get(self, request,shop_id, pk, *args, **kwargs):
        client = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(client)
        return Response(serializer.data, status=200)

    def put(self, request, shop_id, pk, *args, **kwargs):
        client = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk, *args, **kwargs):
        client = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, *args, **kwargs):
        client = get_object_or_404(self.get_queryset(), pk=pk)
        client.delete()
        return Response(status=204)
    
class ClientNomSearchView(ListCreateAPIView):
    """
    View to search for clients by Nom.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer

    def get_queryset(self):
        title = self.request.query_params.get('search', None)
        shop_id = self.request.query_params.get('shop_id', None)
        if title and shop_id:
            return Client.objects.filter(Q(nom__icontains=title, shop__id=shop_id)| Q(prenom__icontains=title, shop__id=shop_id) | Q(adresse__icontains=title, shop__id=shop_id))
        return Client.objects.filter(shop__id=shop_id) if shop_id else Client.objects.all()

    def get(self, request, search, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)
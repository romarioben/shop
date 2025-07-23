from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ShopSerializer
from .models import Shop
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response



class ShopListCreateView(ListCreateAPIView):
    """
    View to list all shops or create a new shop.
    """
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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
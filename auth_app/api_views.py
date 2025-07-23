from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView

from . import models
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class UserDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update or delete a user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return models.User.objects.all()

    def get(self, request, pk, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=200)

    # def put(self, request, pk, *args, **kwargs):
    #     user = self.get_object()
    #     serializer = UserSerializer(user, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=200)
    #     return Response(serializer.errors, status=400)
    
    def patch(self, request, pk, *args, **kwargs):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    def delete(self, request, pk, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(status=204)

class UserCreateView(CreateAPIView):
    """
    View to create a new user.
    """
    #permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=201)
        return Response(serializer.errors, status=400)
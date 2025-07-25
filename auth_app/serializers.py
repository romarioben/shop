from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'last_name', 'first_name', 'is_email_verified', 'receive_notifications')
        read_only_fields = ('id', 'is_email_verified', 'receive_notifications')
        write_only_fields = ('password',)

    def create(self, validated_data):
        print("Creating user with data:", validated_data)
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
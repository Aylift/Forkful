from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'address']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
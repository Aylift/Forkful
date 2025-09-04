from rest_framework import serializers
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password_repeat', 'first_name', 'last_name']
        extra_kwargs = {'email': {'required': True, 'allow_blank': False}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password_repeat']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_repeat', None)
        return CustomUser.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    #TODO add validation


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
            model = CustomUser
            fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'address']
            read_only_fields = ['id', 'username', 'email']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
            model = CustomUser
            fields = ['first_name', 'last_name', 'phone_number', 'address']


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class CheckAuthResponseSerializer(serializers.Serializer):
    authenticated = serializers.BooleanField()
    user = serializers.DictField()

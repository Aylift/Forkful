from rest_framework import serializers
from .models import CustomUser, UserProfile
from datetime import date


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
        user = CustomUser.objects.create_user(**validated_data)

        UserProfile.objects.create(
            user=user,
            height=170,
            weight=70,
            gender='M',
            target_weight=70,
            target_calories=2000,
            target_protein=150,
            target_carbs=250,
            target_fat=65
        )
        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
            model = CustomUser
            fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'address']
            read_only_fields = ['id', 'username', 'email']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'address']


class UserProfileSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    bmi = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_age(self, obj):
         if obj.date_of_birth:
              return (date.today() - obj.date_of_birth).days // 365
         return None
    
    def get_bmi (self, obj):
        if obj.height and obj.weight:
            height_m = obj.height / 100
            return round(float(obj.weight) / (height_m ** 2), 2)
        return None
    

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['user', 'created_at', 'updated_at']
        
    def validate(self, attrs):
        if 'target_weight' in attrs and 'weight' in attrs:
            if attrs['fitness_goal'] == 'lose' and attrs['target_weight'] >= attrs['weight']:
                raise serializers.ValidationError("Target weight should be less than current weight for weight loss")
            elif attrs['fitness_goal'] == 'gain' and attrs['target_weight'] <= attrs['weight']:
                raise serializers.ValidationError("Target weight should be greater than current weight for weight gain")
        return attrs


class UserWithProfileSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'profile']
        read_only_fields = ['id', 'username', 'email']


class CheckAuthResponseSerializer(serializers.Serializer):
    authenticated = serializers.BooleanField()
    user = UserWithProfileSerializer()

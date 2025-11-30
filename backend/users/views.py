from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from .models import UserProfile
from .serializers import (
    RegisterSerializer, UserSerializer, UserWithProfileSerializer,
    UserProfileSerializer, UserProfileUpdateSerializer,
    UserUpdateSerializer, LogoutSerializer
)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Register new user",
        responses={201: UserWithProfileSerializer},
        tags=['Authentication']
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserWithProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    @extend_schema(
        summary="Login (Get Tokens)",
        tags=['Authentication']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserWithProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(summary="Get current user data", tags=['User Profile'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return self.request.user


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(summary="Update basic user info", tags=['User Profile'])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def get_object(self):
        return self.request.user


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserProfileUpdateSerializer
        return UserProfileSerializer

    @extend_schema(summary="Get fitness profile", tags=['User Profile'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Update fitness profile", tags=['User Profile'])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
    @extend_schema(exclude=True)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer

    @extend_schema(summary="Logout (Blacklist Token)", tags=['Authentication'])
    def post(self, request):
        return Response({
            'message': f'Goodbye {request.user.username}! Logout successful.'
        }, status=status.HTTP_200_OK)


class CheckAuthView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(summary="Check authentication status", tags=['Authentication'])
    def get(self, request):
        return Response({
            'authenticated': True,
            'user': UserWithProfileSerializer(request.user).data
        })

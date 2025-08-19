from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, ProfileUpdateSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                },
            'message': 'User created successfully'
            }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairSerializer(TokenObtainPairView):
    def validate(self, attrs):
            data = super().validate(attrs)
            # Add user info to login response
            data['user'] = {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
            }
            return data


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
            return super().get(request, *args, **kwargs)

    def get_object(self):
        return self.request.user


class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
            return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        profile_serializer = ProfileSerializer(instance)
        return Response({
            'message': 'Profile updated successfully',
            'user': profile_serializer.data
        })

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def get_object(self):
        return self.request.user


    class LogoutView(APIView):
        permission_classes = [permissions.IsAuthenticated]

        def post(self, request):
            try:
                refresh_token = request.data["refresh"]
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
            except Exception:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


    class CheckAuthView(APIView):
        permission_classes = [permissions.IsAuthenticated]

        def get(self, request):
            return Response({
                'authenticated': True,
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                }
            })

# TODO
# URLs setup → Test each endpoint with Postman
# Add DEFAULT_AUTHENTICATION_CLASSES in settings
# Create a @login_required endpoint to test auth
# Frontend integration - Store tokens in localStorage/cookies
# Add token refresh logic in your Vue app
# Implement logout (blacklist tokens if using that feature)

# Use Postman collections - Save all your requests for easy testing
# Add custom permissions - IsOwnerOrReadOnly for profile updates
# Email validation - Consider adding email verification later
# Password reset flow - Plan for forgotten passwords
# Rate limiting - Protect login endpoint from brute force

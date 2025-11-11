from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    LogoutView,
    CheckAuthView,
    UserUpdateView,
    UserProfileView,
)

app_name = 'users'

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/check/', CheckAuthView.as_view(), name='check_auth'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('auth/user/update/', UserUpdateView.as_view(), name='user_update'),
    path('auth/profile/update/', UserProfileView.as_view(), name='profile_update'),
]
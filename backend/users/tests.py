import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .models import UserProfile
from .serializers import RegisterSerializer, UserProfileSerializer, UserProfileUpdateSerializer

User = get_user_model()

class UsersAppTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', 
            password='password123',
            email='test@example.com'
        )
        
        self.birth_date = datetime.date(1990, 1, 1)
        self.profile = UserProfile.objects.create(
            user=self.user,
            height=180,
            weight=80.0,
            date_of_birth=self.birth_date,
            gender='M',
            target_weight=75.0,
            fitness_goal='lose',
            target_calories=2000,
            target_protein=150,
            target_carbs=200,
            target_fat=60
        )

        self.register_data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpassword123",
            "password_repeat": "newpassword123",
            "first_name": "New",
            "last_name": "User"
        }


    def test_user_str_method(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_profile_str_method(self):
        self.assertEqual(str(self.profile), 'Profile of testuser')


    def test_register_serializer_password_mismatch(self):
        data = self.register_data.copy()
        data['password_repeat'] = 'wrongpassword'
        serializer = RegisterSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn("Passwords don't match", str(context.exception))

    def test_register_serializer_create_user_and_profile(self):
        serializer = RegisterSerializer(data=self.register_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(UserProfile.objects.count(), 2)
        self.assertEqual(user.username, 'newuser')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.weight, 70) 

    def test_profile_serializer_get_age(self):
        serializer = UserProfileSerializer(instance=self.profile)
        expected_age = (datetime.date.today() - self.birth_date).days // 365
        self.assertEqual(serializer.data['age'], expected_age)

    def test_profile_serializer_get_bmi(self):
        serializer = UserProfileSerializer(instance=self.profile)
        expected_bmi = round(80.0 / (1.8 ** 2), 2)
        self.assertEqual(serializer.data['bmi'], expected_bmi)

    def test_profile_update_serializer_validation_fail(self):
        data = {
            'weight': 80.0,
            'target_weight': 85.0,
            'fitness_goal': 'lose'
        }
        serializer = UserProfileUpdateSerializer(instance=self.profile, data=data, partial=True)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn("Target weight should be less", str(context.exception))
        
        data = {
            'weight': 80.0,
            'target_weight': 75.0,
            'fitness_goal': 'gain'
        }
        serializer = UserProfileUpdateSerializer(instance=self.profile, data=data, partial=True)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn("Target weight should be greater", str(context.exception))

    def test_profile_update_serializer_validation_pass(self):
        data = {
            'weight': 80.0,
            'target_weight': 75.0,
            'fitness_goal': 'lose'
        }
        serializer = UserProfileUpdateSerializer(instance=self.profile, data=data, partial=True)
        self.assertTrue(serializer.is_valid(raise_exception=True))


    def test_register_view_success(self):
        response = self.client.post('/api/auth/register/', self.register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(UserProfile.objects.count(), 2)
        self.assertIn('user', response.data)
        self.assertIn('tokens', response.data)
        self.assertEqual(response.data['user']['username'], 'newuser')

    def test_register_view_password_mismatch(self):
        data = self.register_data.copy()
        data['password_repeat'] = 'wrong'
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_view_success(self):
        data = {"username": "testuser", "password": "password123"}
        response = self.client.post('/api/auth/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_view_fail(self):
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post('/api/auth/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_check_auth_view_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/auth/check/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['authenticated'], True)
        self.assertEqual(response.data['user']['username'], 'testuser')

    def test_check_auth_view_unauthenticated(self):
        response = self.client.get('/api/auth/check/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_view_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['profile']['height'], 180)

    def test_profile_view_unauthenticated(self):
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_update_view(self):
        self.client.force_authenticate(user=self.user)
        data = {'first_name': 'Updated', 'last_name': 'Name'}
        response = self.client.patch('/api/auth/user/update/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(response.data['last_name'], 'Name')

    def test_user_profile_get_view(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/auth/profile/update/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.pk)
        self.assertEqual(response.data['height'], 180)

    def test_user_profile_update_view(self):
        self.client.force_authenticate(user=self.user)
        data = {'height': 185, 'target_calories': 2200}
        response = self.client.patch('/api/auth/profile/update/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.height, 185)
        self.assertEqual(self.profile.target_calories, 2200)

    def test_logout_view(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/auth/logout/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Goodbye testuser', response.data['message'])
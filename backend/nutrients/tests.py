from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.test import APIClient
from rest_framework import status

from .models import Ingredient, Nutrient, IngredientNutrient

User = get_user_model()

class NutrientsAppTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = APIClient()

        self.ingredient = Ingredient.objects.create(name='Apple', category='Fruit')
        self.nutrient = Nutrient.objects.create(name='Sugar', unit='g')
        self.link = IngredientNutrient.objects.create(
            ingredient=self.ingredient,
            nutrient=self.nutrient,
            amount_per_100g=10.0
        )

    # --- Model Tests ---

    def test_ingredient_str_method(self):
        self.assertEqual(str(self.ingredient), 'Apple')

    def test_nutrient_str_method(self):
        self.assertEqual(str(self.nutrient), 'Sugar')

    def test_ingredient_nutrient_str_method(self):
        expected_str = f'Sugar in Apple'
        self.assertEqual(str(self.link), expected_str)

    def test_ingredient_nutrient_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            IngredientNutrient.objects.create(
                ingredient=self.ingredient,
                nutrient=self.nutrient,
                amount_per_100g=20.0 # Same ingredient/nutrient pair
            )

    # --- Ingredient Endpoint Tests ---

    def test_get_ingredient_list_unauthenticated(self):
        response = self.client.get('/api/ingredients/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Apple')

    def test_create_ingredient_unauthenticated(self):
        data = {'name': 'Banana', 'category': 'Fruit'}
        response = self.client.post('/api/ingredients/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_ingredient_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Banana', 'category': 'Fruit'}
        response = self.client.post('/api/ingredients/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ingredient.objects.count(), 2)

    def test_update_ingredient_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Green Apple', 'category': 'Fruit'}
        response = self.client.put(f'/api/ingredients/{self.ingredient.pk}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Green Apple')

    def test_delete_ingredient_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/ingredients/{self.ingredient.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ingredient.objects.count(), 0)

    # --- Nutrient Endpoint Tests ---

    def test_get_nutrient_list(self):
        response = self.client.get('/api/nutrients/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Sugar')

    def test_get_nutrient_detail(self):
        response = self.client.get(f'/api/nutrients/{self.nutrient.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Sugar')

    def test_create_nutrient_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Protein', 'unit': 'g'}
        response = self.client.post('/api/nutrients/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Nutrient.objects.count(), 2)

    # --- IngredientNutrient Endpoint Tests ---

    def test_get_ingredient_nutrient_list(self):
        response = self.client.get('/api/ingredient_nutrients/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['amount_per_100g'], 10.0)

    def test_get_ingredient_nutrient_detail(self):
        response = self.client.get(f'/api/ingredient_nutrients/{self.link.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount_per_100g'], 10.0)

    def test_create_ingredient_nutrient_authenticated(self):
        self.client.force_authenticate(user=self.user)
        vitamin_c = Nutrient.objects.create(name='Vitamin C', unit='mg')
        data = {
            'ingredient_id': self.ingredient.pk,
            'nutrient_id': vitamin_c.pk,
            'amount_per_100g': 8.4
        }
        response = self.client.post('/api/ingredient_nutrients/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(IngredientNutrient.objects.count(), 2)
        self.assertEqual(response.data['amount_per_100g'], 8.4)
        
    def test_delete_ingredient_nutrient_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/ingredient_nutrients/{self.link.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(IngredientNutrient.objects.count(), 0)
import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from .models import Meal, MealIngredient, DailyEntry
from nutrients.models import Nutrient, Ingredient, IngredientNutrient

User = get_user_model()


class MealsAppTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.other_user = User.objects.create_user(username='otheruser', password='password123')

        self.protein = Nutrient.objects.create(name='Protein', unit='g')
        self.fat = Nutrient.objects.create(name='Fat', unit='g')
        self.carbs = Nutrient.objects.create(name='Carbs', unit='g')

        self.chicken = Ingredient.objects.create(name='Chicken Breast')
        self.oil = Ingredient.objects.create(name='Olive Oil')

        IngredientNutrient.objects.create(
            ingredient=self.chicken, 
            nutrient=self.protein, 
            amount_per_100g=30.0
        )
        IngredientNutrient.objects.create(
            ingredient=self.oil, 
            nutrient=self.fat, 
            amount_per_100g=100.0
        )

        self.meal = Meal.objects.create(name='Basic Chicken', description='Just chicken and oil')

        MealIngredient.objects.create(
            meal=self.meal,
            ingredient=self.chicken,
            amount_in_grams=150.0 
        )
        MealIngredient.objects.create(
            meal=self.meal,
            ingredient=self.oil,
            amount_in_grams=10.0
        )
        
        self.today = datetime.date.today()
        self.entry = DailyEntry.objects.create(
            user=self.user,
            meal=self.meal,
            date=self.today,
            servings=1.0
        )

        self.client = APIClient()

    
    def test_meal_str_method(self):
        self.assertEqual(str(self.meal), 'Basic Chicken')

    def test_daily_entry_str_method(self):
        expected_str = f'testuser ate 1.0x Basic Chicken on {self.today}'
        self.assertEqual(str(self.entry), expected_str)

    def test_meal_total_nutrients_calculation(self):
        nutrients = self.meal.total_nutrients()
        
        self.assertIn('Protein', nutrients)
        self.assertIn('Fat', nutrients)
        
        self.assertAlmostEqual(nutrients['Protein']['amount'], 45.0)
        self.assertEqual(nutrients['Protein']['unit'], 'g')
        
        self.assertAlmostEqual(nutrients['Fat']['amount'], 10.0)
        self.assertEqual(nutrients['Fat']['unit'], 'g')
        
        self.assertNotIn('Carbs', nutrients)


    def test_get_meal_list_unauthenticated(self):
        response = self.client.get('/api/meals/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Basic Chicken')
        
        self.assertIn('total_nutrients', response.data[0])
        self.assertAlmostEqual(response.data[0]['total_nutrients']['Protein']['amount'], 45.0)

    def test_create_meal_authenticated(self):
        self.client.force_authenticate(user=self.user)
        
        new_meal_data = {
            "name": "New Salad",
            "description": "A new creation",
            "meal_ingredients": [
                {
                    "ingredient_id": self.chicken.pk,
                    "amount_in_grams": 50
                }
            ]
        }
        
        response = self.client.post('/api/meals/', new_meal_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Meal.objects.count(), 2)
        self.assertEqual(response.data['name'], 'New Salad')
        self.assertEqual(len(response.data['meal_ingredients']), 1)

    def test_create_meal_unauthenticated(self):
        new_meal_data = { "name": "Test", "meal_ingredients": [] }
        response = self.client.post('/api/meals/', new_meal_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_meal(self):
        self.client.force_authenticate(user=self.user)
        
        updated_data = {
            "name": "Updated Meal Name",
            "description": self.meal.description,
            "meal_ingredients": [
                {
                    "ingredient_id": self.chicken.pk,
                    "amount_in_grams": 200
                }
            ]
        }
        
        response = self.client.put(f'/api/meals/{self.meal.pk}/', updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Meal Name')
        
        self.meal.refresh_from_db()
        self.assertEqual(self.meal.name, 'Updated Meal Name')
        self.assertAlmostEqual(self.meal.total_nutrients()['Protein']['amount'], 60.0)

    def test_delete_meal(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(f'/api/meals/{self.meal.pk}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Meal.objects.count(), 0)


    def test_get_daily_entries_unauthenticated(self):
        response = self.client.get('/api/daily-entries/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_daily_entries_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/daily-entries/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.entry.pk)

    def test_get_daily_entries_filters_by_user(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get('/api/daily-entries/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_daily_entries_date_filter(self):
        yesterday = self.today - datetime.timedelta(days=1)
        DailyEntry.objects.create(user=self.user, meal=self.meal, date=yesterday)
        
        self.client.force_authenticate(user=self.user)
        
        response_today = self.client.get('/api/daily-entries/')
        self.assertEqual(len(response_today.data), 1)

        response_yesterday = self.client.get(f'/api/daily-entries/?date={yesterday}')
        self.assertEqual(len(response_yesterday.data), 1)
        
        response_tomorrow = self.client.get('/api/daily-entries/?date=2099-01-01')
        self.assertEqual(len(response_tomorrow.data), 0)

    def test_user_cannot_delete_other_users_entry(self):
        self.client.force_authenticate(user=self.other_user)
        
        response = self.client.delete(f'/api/daily-entries/{self.entry.pk}/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(DailyEntry.objects.count(), 1)

    def test_user_can_delete_own_entry(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(f'/api/daily-entries/{self.entry.pk}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DailyEntry.objects.count(), 0)
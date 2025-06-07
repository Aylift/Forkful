from django.db import models
from backend.nutrients.models import Ingredient, IngredientNutrient


class Meal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def total_nutrients(self):
        nutrients = {}
        for meal_ingredient in self.meal_ingredients.select_related('ingredient').prefetch_related('ingredient__nutrients__nutrient'):
            ingredient = meal_ingredient.ingredient
            for ingredient_nutrient in ingredient.nutrients.select_related('nutrient'):
                nutrient_name = ingredient_nutrient.nutrient.name
                nutrient_amount = (ingredient_nutrient.amount_per_100g / 100.0) * meal_ingredient.amount_in_grams
                nutrients[nutrient_name] = {
                    'amount': nutrients.get(nutrient_name, {}).get('amount', 0) + nutrient_amount,
                    'unit': ingredient_nutrient.nutrient.unit
                }
        return nutrients


class MealIngredient(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='meal_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount_in_grams = models.FloatField(help_text='Amount used in grams')

    class Meta:
        unique_together = ('meal', 'ingredient')

    def __str__(self):
        return f'{self.amount_in_grams}g of {self.ingredient.name} in {self.meal.name}'

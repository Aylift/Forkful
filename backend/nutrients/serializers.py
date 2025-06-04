from rest_framework import serializers
from .models import Ingredient, IngredientNutrient, Nutrient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'category']
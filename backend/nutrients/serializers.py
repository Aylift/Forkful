from rest_framework import serializers
from .models import Ingredient, IngredientNutrient, Nutrient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'category']


class NutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrient
        fields = ['name', 'unit']


class IngredientNutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientNutrient
        fields = ['ingredient', 'nutrient', 'amount_per_100g']
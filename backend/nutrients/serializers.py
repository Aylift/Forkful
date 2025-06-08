from rest_framework import serializers
from .models import Ingredient, IngredientNutrient, Nutrient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'category']



class NutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrient
        fields = ['id', 'name', 'unit']


class IngredientNutrientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    nutrient = NutrientSerializer(read_only=True)

    ingredient_id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source='ingredient', write_only=True
    )
    nutrient_id = serializers.PrimaryKeyRelatedField(
        queryset=Nutrient.objects.all(), source='nutrient', write_only=True
    )

    class Meta:
        model = IngredientNutrient
        fields = [
            'ingredient', 'nutrient', 'amount_per_100g',
            'ingredient_id', 'nutrient_id',
        ]

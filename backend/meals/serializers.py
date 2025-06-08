from rest_framework import serializers
from .models import Meal, MealIngredient
from nutrients.models import Ingredient
from nutrients.serializers import IngredientSerializer


class MealIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient',
        write_only=True
    )

    class Meta:
        model = MealIngredient
        fields = ['ingredient', 'ingredient_id', 'amount_in_grams']


class MealSerializer(serializers.ModelSerializer):
    meal_ingredients = MealIngredientSerializer(many=True)
    total_nutrients = serializers.SerializerMethodField()

    class Meta:
        model = Meal
        fields = ['id', 'name', 'description', 'meal_ingredients', 'total_nutrients']

    def get_total_nutrients(self, obj):
        return obj.total_nutrient()

    def create(self, validated_data):
        ingredients_data = validated_data.pop('meal_ingredients')
        meal = Meal.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            MealIngredient.objects.create(meal=meal, **ingredient_data)
        return meal

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('meal_ingredients')
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        instance.meal_ingredients.all().delete()

        for ingredient_data in ingredients_data:
            MealIngredient.objects.create(meal=instance, **ingredient_data)

        return instance

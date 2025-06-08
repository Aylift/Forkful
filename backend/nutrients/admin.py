from django.contrib import admin
from .models import Ingredient, IngredientNutrient, Nutrient


admin.site.register(Ingredient)
admin.site.register(Nutrient)
admin.site.register(IngredientNutrient)

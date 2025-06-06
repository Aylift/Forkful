from django.urls import path
from .views import IngredientListView, IngredientDetailView, NutrientListView, NutrientDetailView, IngredientNutrientListView, IngredientNutrientDetailView


urlpatterns = [
    path('ingredients/', IngredientListView.as_view(), name='ingredient_list'),
    path('ingredients/<int:pk>/', IngredientDetailView.as_view(), name='ingredient_detail'),
    path('nutrients/', NutrientListView.as_view(), name='nutrient_list'),
    path('nutrients/<int:pk>/', NutrientDetailView.as_view(), name='nutrient_detail'),
    path('ingredient_nutrients/', IngredientNutrientListView.as_view(), name='ingredient_nutrient_list'),
    path('ingredient_nutrients/<int:pk>/', IngredientNutrientDetailView.as_view(), name='ingredient_nutrient_detail')
]
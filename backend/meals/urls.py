from django.urls import path
from .views import MealListView, MealDetailView, MealIngredientListView, MealIngredientDetailView, DailyEntryListView, DailyEntryDetailView


urlpatterns = [
    path('meals/', MealListView.as_view(), name='meal_list'),
    path('meals/<int:pk>/', MealDetailView.as_view(), name='meal_detail'),
    path('meal_ingredients', MealIngredientListView.as_view(), name='meal_ingredient_list'),
    path('meal_ingredients/<int:pk>', MealIngredientDetailView.as_view(), name='meal_ingredient_detail'),
    path('daily-entries/', DailyEntryListView.as_view(), name='daily_entry_list'),
    path('daily-entries/<int:pk>/', DailyEntryDetailView.as_view(), name='daily_entry_detail'),
]
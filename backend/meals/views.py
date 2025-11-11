from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .models import Meal, MealIngredient, DailyEntry
from .serializers import MealIngredientSerializer, MealSerializer, DailyEntrySerializer
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from datetime import date


class MealListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    @extend_schema(
        summary="List of all meals",
        responses={200: MealSerializer(many=True)}
    )
    def get(self, request):
        meals = Meal.objects.all()
        serializer = MealSerializer(meals, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Add Meal",
        request=MealSerializer,
        responses={201: MealSerializer}
    )
    def post(self, request):
        serializer = MealSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MealDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    @extend_schema(
        summary="Retrieve a meal",
        responses={200: MealSerializer}
    )
    def get(self, request, pk):
        meal = get_object_or_404(Meal, pk=pk)
        serializer = MealSerializer(meal)
        return Response(serializer.data)

    @extend_schema(
        summary="Edit meal",
        request=MealSerializer,
        responses={200: MealSerializer}
    )
    def put(self, request, pk):
        meal = get_object_or_404(Meal, pk=pk)
        serializer = MealSerializer(meal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete Meal",
        responses={204: None}
    )
    def delete(self, request, pk):
        meal = get_object_or_404(Meal, pk=pk)
        meal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MealIngredientListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    @extend_schema(
        summary="List of all meal-ingredients association",
        responses={200: MealIngredientSerializer(many=True)}
    )
    def get(self, request):
        meal_ingredients = MealIngredient.objects.all()
        serializer = MealIngredientSerializer(meal_ingredients, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Add meal-ingredient association",
        request=MealIngredientSerializer,
        responses={201: MealIngredientSerializer}
    )
    def post(self, request):
        serializer = MealIngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MealIngredientDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    @extend_schema(
        summary="Retrieve a meal-ingredient association",
        responses={200: MealIngredientSerializer}
    )
    def get(self, request, pk):
        meal_ingredient = get_object_or_404(MealIngredient, pk=pk)
        serializer = MealIngredientSerializer(meal_ingredient)
        return Response(serializer.data)

    @extend_schema(
        summary="Edit meal-ingredient association",
        request=MealIngredientSerializer,
        responses={200: MealIngredientSerializer}
    )
    def put(self, request, pk):
        meal_ingredient = get_object_or_404(MealIngredient, pk=pk)
        serializer = MealIngredientSerializer(meal_ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete meal-ingredient association",
        responses={204: None}
    )
    def delete(self, request, pk):
        meal_ingredient = get_object_or_404(MealIngredient, pk=pk)
        meal_ingredient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class DailyEntryListView(generics.ListCreateAPIView):
    serializer_class = DailyEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = DailyEntry.objects.filter(user=self.request.user)

        date_param = self.request.query_params.get('date')
        if date_param:
            queryset = queryset.filter(date=date_param)
        else:
            queryset = queryset.filter(date=date.today)
            
        return queryset.select_related('meal')

    def perform_create(self, serializer):
        serializer.save()


class DailyEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DailyEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DailyEntry.objects.filter(user=self.request.user)

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import Meal, MealIngredient, DailyEntry
from .serializers import MealIngredientSerializer, MealSerializer, DailyEntrySerializer
from datetime import date


class MealListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        summary="List all meals",
        description="Returns a list of all available meals with calculated total nutrients.",
        responses={200: MealSerializer(many=True)},
        tags=['Meals']
    )
    def get(self, request):
        meals = Meal.objects.all()
        serializer = MealSerializer(meals, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create a new meal",
        request=MealSerializer,
        responses={201: MealSerializer},
        tags=['Meals']
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
        responses={200: MealSerializer},
        tags=['Meals']
    )
    def get(self, request, pk):
        meal = get_object_or_404(Meal, pk=pk)
        serializer = MealSerializer(meal)
        return Response(serializer.data)

    @extend_schema(
        summary="Update a meal",
        request=MealSerializer,
        responses={200: MealSerializer},
        tags=['Meals']
    )
    def put(self, request, pk):
        meal = get_object_or_404(Meal, pk=pk)
        serializer = MealSerializer(meal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete a meal",
        responses={204: None},
        tags=['Meals']
    )
    def delete(self, request, pk):
        meal = get_object_or_404(Meal, pk=pk)
        meal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MealIngredientListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(summary="List meal ingredients", tags=['Meal Ingredients'])
    def get(self, request):
        meal_ingredients = MealIngredient.objects.all()
        serializer = MealIngredientSerializer(meal_ingredients, many=True)
        return Response(serializer.data)

    @extend_schema(summary="Add ingredient to meal", tags=['Meal Ingredients'])
    def post(self, request):
        serializer = MealIngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MealIngredientDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(summary="Retrieve meal ingredient", tags=['Meal Ingredients'])
    def get(self, request, pk):
        meal_ingredient = get_object_or_404(MealIngredient, pk=pk)
        serializer = MealIngredientSerializer(meal_ingredient)
        return Response(serializer.data)

    @extend_schema(summary="Update meal ingredient", tags=['Meal Ingredients'])
    def put(self, request, pk):
        meal_ingredient = get_object_or_404(MealIngredient, pk=pk)
        serializer = MealIngredientSerializer(meal_ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary="Remove ingredient from meal", tags=['Meal Ingredients'])
    def delete(self, request, pk):
        meal_ingredient = get_object_or_404(MealIngredient, pk=pk)
        meal_ingredient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    summary="List daily entries",
    description="Get food log for the current user. Filter by date using '?date=YYYY-MM-DD'.",
    tags=['Food Log'],
    parameters=[
        OpenApiParameter(name='date', description='Filter by date (YYYY-MM-DD)', required=False, type=OpenApiTypes.DATE),
    ]
)
class DailyEntryListView(generics.ListCreateAPIView):
    serializer_class = DailyEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = DailyEntry.objects.filter(user=self.request.user)
        date_param = self.request.query_params.get('date')
        if date_param:
            queryset = queryset.filter(date=date_param)
        else:
            queryset = queryset.filter(date=date.today())
        return queryset.select_related('meal')

    @extend_schema(summary="Log a meal", tags=['Food Log'])
    def perform_create(self, serializer):
        serializer.save()


@extend_schema(tags=['Food Log'])
class DailyEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DailyEntrySerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(summary="Retrieve log entry")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Update log entry")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(summary="Delete log entry")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return DailyEntry.objects.filter(user=self.request.user)
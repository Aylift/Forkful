from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema
from .models import Ingredient, Nutrient, IngredientNutrient
from .serializers import IngredientSerializer, NutrientSerializer, IngredientNutrientSerializer


class IngredientListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(summary="List ingredients", tags=['Ingredients'])
    def get(self, request):
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    @extend_schema(summary="Create ingredient", request=IngredientSerializer, tags=['Ingredients'])
    def post(self, request):
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(summary="Update ingredient", tags=['Ingredients'])
    def put(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        serializer = IngredientSerializer(ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary="Delete ingredient", tags=['Ingredients'])
    def delete(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        ingredient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NutrientListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(summary="List nutrients", tags=['Nutrients'])
    def get(self, request):
        nutrients = Nutrient.objects.all()
        serializer = NutrientSerializer(nutrients, many=True)
        return Response(serializer.data)

    @extend_schema(summary="Create nutrient", tags=['Nutrients'])
    def post(self, request):
        serializer = NutrientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NutrientDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(summary="Retrieve nutrient", tags=['Nutrients'])
    def get(self, request, pk):
        nutrient = get_object_or_404(Nutrient, pk=pk)
        serializer = NutrientSerializer(nutrient)
        return Response(serializer.data)

    @extend_schema(summary="Update nutrient", tags=['Nutrients'])
    def put(self, request, pk):
        nutrient = get_object_or_404(Nutrient, pk=pk)
        serializer = NutrientSerializer(nutrient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary="Delete nutrient", tags=['Nutrients'])
    def delete(self, request, pk):
        nutrient = get_object_or_404(Nutrient, pk=pk)
        nutrient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientNutrientListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(summary="List ingredient-nutrient links", tags=['Ingredients'])
    def get(self, request):
        ingredient_nutrients = IngredientNutrient.objects.all()
        serializer = IngredientNutrientSerializer(ingredient_nutrients, many=True)
        return Response(serializer.data)

    @extend_schema(summary="Link nutrient to ingredient", tags=['Ingredients'])
    def post(self, request):
        serializer = IngredientNutrientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientNutrientDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(summary="Retrieve link", tags=['Ingredients'])
    def get(self, request, pk):
        nutrient_ingredient = get_object_or_404(IngredientNutrient, pk=pk)
        serializer = IngredientNutrientSerializer(nutrient_ingredient)
        return Response(serializer.data)

    @extend_schema(summary="Update link", tags=['Ingredients'])
    def put(self, request, pk):
        ingredient_nutrient = get_object_or_404(IngredientNutrient, pk=pk)
        serializer = IngredientNutrientSerializer(ingredient_nutrient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary="Delete link", tags=['Ingredients'])
    def delete(self, request, pk):
        ingredient_nutrient = get_object_or_404(IngredientNutrient, pk=pk)
        ingredient_nutrient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

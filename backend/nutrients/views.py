from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Ingredient, Nutrient
from .serializers import IngredientSerializer, NutrientSerializer
from rest_framework.generics import get_object_or_404
from rest_framework import status


class IngredientListView(APIView):
    @extend_schema(
        summary="List of all ingredients",
        responses={200: IngredientSerializer(many=True)}
    )
    def get(self, request):
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Add ingredient",
        request=IngredientSerializer,
        responses={201: IngredientSerializer}
    )
    def post(self, request):
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientDetailView(APIView):
    @extend_schema(
        summary="Edit ingredient",
        request=IngredientSerializer,
        responses={200: IngredientSerializer}
    )
    def put(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        serializer = IngredientSerializer(ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete ingredient",
        responses={204: None}
    )
    def delete(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        ingredient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NutrientListView(APIView):
    @extend_schema(
        summary="List of all nutrients",
        responses={200: NutrientSerializer(many=True)}
    )
    def get(self, request):
        nutrients = Nutrient.objects.all()
        serializer = NutrientSerializer(nutrients, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Add nutrient",
        request=NutrientSerializer,
        responses={201: NutrientSerializer}
    )
    def post(self, request):
        serializer = NutrientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NutrientDetailView(APIView):
    @extend_schema(
        summary="Edit nutrient",
        request=NutrientSerializer,
        responses={200: NutrientSerializer}
    )
    def put(self, request, pk):
        nutrient = get_object_or_404(Nutrient, pk=pk)
        serializer = NutrientSerializer(Nutrient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete nutrient",
        responses={204: None}
    )
    def delete(self, request, pk):
        nutrient = get_object_or_404(Nutrient, pk=pk)
        nutrient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



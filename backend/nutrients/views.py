from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Ingredient
from .serializers import IngredientSerializer
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

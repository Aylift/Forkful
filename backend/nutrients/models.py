from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Nutrient(models.Model):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=50, help_text='e.g. g, mg, kcal')

    def __str__(self):
        return self.name


class IngredientNutrient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='nutrients')
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    amount_per_100g = models.FloatField(help_text='Amount per 100g of ingredient')

    class Meta:
        unique_together = ('ingredient', 'nutrient')

    def __str__(self):
        return f'{self.nutrient} in {self.ingredient}'
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Możemy później rozwinąć CustomUser, albo zrobić kolejny model np. Profile z One-to-One do CustomUser i tam wrzucić dodatkowe fieldy
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    ACTIVITY_CHOICES = [
        (0, 'No activity'),
        (1, 'Little activity (1-2 light workouts a week)'),
        (2, 'Medium activity (3-4 medium workouts a week)'),
        (3, 'High activity (4-5 medium-heavy workouts a week)'),
        (4, 'Extreme activity (5+ intense workouts a week)')
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    GOAL_CHOICES = [
        ('lose', 'Lose weight'),
        ('maintain', 'Maintain weight'),
        ('gain', 'Gain weight'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')

    height = models.PositiveIntegerField(help_text="Height in cm", validators=[MinValueValidator(50), MaxValueValidator(300)])
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Current weight in kg")
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    activity_level = models.IntegerField(choices=ACTIVITY_CHOICES, default=2)
    target_weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Target weight in kg")
    fitness_goal = models.CharField(max_length=10, choices=GOAL_CHOICES, default='maintain')

    target_calories = models.PositiveIntegerField()
    target_protein = models.PositiveIntegerField()
    target_carbs = models.PositiveIntegerField()
    target_fat = models.PositiveIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
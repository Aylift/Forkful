from django.contrib.auth.models import AbstractUser
from django.db import models


# Możemy później rozwinąć CustomUser, albo zrobić kolejny model np. Profile z One-to-One do CustomUser i tam wrzucić dodatkowe fieldy
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.username

from django.db import models
from django.contrib.auth.models import User
from django.urls import revers

class City(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'
from django.db import models

# Create your models here.

class movies(models.Model):
    name = models.CharField()
    cover_image = models.ImageField()
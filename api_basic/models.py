from statistics import mode
from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return self.title


class zulassungen(models.Model):
    jahr = models.IntegerField(default=0)
    monat = models.IntegerField(default=0)
    marke = models.CharField(max_length=100, default="None")
    modell= models.CharField(max_length=100, default="None")
    anzahl = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return self.marke
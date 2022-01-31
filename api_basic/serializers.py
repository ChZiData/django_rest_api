from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers
from .models import Article
from .models import zulassungen


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'author', 'email', 'date']

class ZulassungenSerializer(serializers.ModelSerializer):
    class Meta:
        model = zulassungen
        fields = ['jahr', 'monat', 'marke', 'modell', 'anzahl', 'date']

class MarkenSerializer(serializers.ModelSerializer):
    class Meta:
        model = zulassungen
        fields = ['marke']
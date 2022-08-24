
from rest_framework import serializers
from reviews.models import Category, Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        model = Genre

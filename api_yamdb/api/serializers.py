
from rest_framework import serializers
from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category"""
    class Meta:
        fields = ('id', 'name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre"""
    class Meta:
        fields = ('id', 'name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title"""
    rating = serializers.FloatField()

    class Meta:
        fields = (
            'id',
            'name',
            # 'description',
            'year',
            'category',
            # 'genre',
            'rating',
        )
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title для методов POST и PATCH"""
    class Meta:
        fields = (
            'id',
            'name',
            # 'description',
            'year',
            'category',
            # 'genre',
        )
        model = Title

from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title


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


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    pub_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')

    def get_pub_date(self, obj):
        return obj.pub_date.strftime('%Y-%m-%dT%H:%M:%SZ')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для ревью."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    pub_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def get_pub_date(self, obj):
        return obj.pub_date.strftime('%Y-%m-%dT%H:%M:%SZ')

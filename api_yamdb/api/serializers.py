from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category"""
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre"""
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title"""
    rating = serializers.FloatField()

    class Meta:
        fields = (
            'id',
            'name',
            'description',
            'year',
            'category',
            'genre',
            'rating',
        )
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title для методов POST и PATCH"""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = (
            'id',
            'name',
            'description',
            'year',
            'category',
            'genre',
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

    # def validate(self, data):
    #     title_id = (
    #       self.context['request'].parser_context['kwargs']['title_id']
    #      )
    #     title = Title.objects.filter(id=title_id)
    #     text = data['text']
    #     if Review.objects.filter(title_id=title, text=text):
    #         raise serializers.ValidationError('Уже есть такой отзыв!')
    #     return data

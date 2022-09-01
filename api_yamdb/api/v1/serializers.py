from django.shortcuts import get_object_or_404
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator
import datetime as dt
from reviews.models import (Category, Comment, Genre,
                            Review, Title, User, ConfirmationCode)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class UserMeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения и обновления информации о авторе.
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ['role']


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для аутентификации."""
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, attrs):
        name = 'me'
        if attrs.get('username') == name:
            raise exceptions.ValidationError(
                f'Использовать имя {name} в качестве username запрещено.'
            )
        return attrs


class ConfirmationCodeSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(required=True)
    confirmation_code = serializers.SlugField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, attrs):
        user = get_object_or_404(User, username=attrs['username'])
        try:
            code = ConfirmationCode.objects.get(user=user)
        except ConfirmationCode.DoesNotExist:
            raise exceptions.ValidationError(
                'Отсутствует confirmation code'
            )
        if code.token != attrs['confirmation_code']:
            raise exceptions.ValidationError(
                'Некорректный confirmation code'
            )
        code.delete()
        return attrs


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category."""

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre."""

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title."""
    rating = serializers.FloatField()
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

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
        read_only_fields = (
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
    """Сериализатор модели Title для методов POST и PATCH."""
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

    def validate_year(self, year):
        if year > dt.datetime.now().year:
            raise serializers.ValidationError(
                'Год выхода произведения не может превышать текущий.'
            )
        return year


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

    def validate(self, data):
        title_id = (
            self.context['request'].parser_context['kwargs']['title_id']
        )
        title = get_object_or_404(Title, id=title_id)
        if (
                Review.objects.filter(
                    title=title, author=self.context['request'].user
                ).exists()
                and self.context['request'].method != 'PATCH'
        ):
            raise serializers.ValidationError('Вы уже оставляли отзыв!')
        return data

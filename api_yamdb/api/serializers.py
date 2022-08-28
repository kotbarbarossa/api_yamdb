from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.shortcuts import get_object_or_404
from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator
import datetime as dt
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import User, ConfirmationCode
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from reviews.models import User, ConfirmationCode


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def update(self, instance, validated_data):
        print('\n\n\n\n\n\n\n')
        print(instance.is_staff)
        print('\n\n\n\n\n\n\n')
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name',
                                                 instance.first_name)
        instance.last_name = validated_data.get('last_name',
                                                instance.last_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.role = validated_data.get('role', instance.role)
        if validated_data.get('role') == 'admin':
            instance.is_staff = True
        if validated_data.get('role') == 'moderator':
            instance.is_moderator = True
        instance.save()
        return instance


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ['role']


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        name = 'me'
        if validated_data.get('username') == name:
            raise exceptions.ValidationError(
                f'Использовать имя {name} в качестве username запрещено.'
            )
        return User.objects.create(**validated_data)


class MyTokenObtainSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD

    default_error_messages = {
        'no_active_account': ('No active account found '
                              'with the given credentials')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['confirmation_code'] = serializers.CharField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs['username'],
            'confirmation_code': attrs['confirmation_code'],
        }

        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = get_object_or_404(User, username=attrs['username'])

        try:
            code = ConfirmationCode.objects.get(user=self.user)
        except ConfirmationCode.DoesNotExist:
            raise exceptions.ValidationError(
                'Отсутствует confirmation code'
            )
        if code.token != attrs['confirmation_code']:
            raise exceptions.ValidationError(
                'Некорректный confirmation code'
            )
        code.delete()

        return {}


class MyTokenObtainPairSerializer(MyTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        print(data)
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


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

    # def validate(self, data):
    #     title_id = (
    #       self.context['request'].parser_context['kwargs']['title_id']
    #      )
    #     title = Title.objects.filter(id=title_id)
    #     text = data['text']
    #     if Review.objects.filter(title_id=title, text=text):
    #         raise serializers.ValidationError('Уже есть такой отзыв!')
    #     return data

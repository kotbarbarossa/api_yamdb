from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework import serializers, exceptions, status
from rest_framework.validators import UniqueValidator

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from yaml import serializer

import reviews
from api_yamdb import settings
from reviews.models import User, ConfirmationCode
from secrets import token_hex


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


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
        if validated_data['username'] == name:
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

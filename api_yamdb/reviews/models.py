from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE = (
    (
        ('user', 'Пользователь'),
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
    )
)


class User(AbstractUser):
    """Модель пользователя."""
    role = models.CharField(
        'Пользовательская роль',
        max_length=10,
        choices=ROLE,
        default=''
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )

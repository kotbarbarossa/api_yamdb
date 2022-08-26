from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель пользователя."""
    ROLE = (
        (
            ('user', 'Пользователь'),
            ('admin', 'Администратор'),
            ('moderator', 'Модератор'),
        )
    )

    role = models.CharField(
        'Пользовательская роль',
        max_length=10,
        choices=ROLE,
        default='user'
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )


class ConfirmationCode(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    token = models.CharField(max_length=255)


class Category(models.Model):
    """Модель для категорий. Присваевается одна на произведение"""
    name = models.CharField(max_length=48, verbose_name='Название категории')
    slug = models.SlugField(max_length=48, unique=True)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """Модель для Жанров. Множественное пристваивание на произведение"""
    name = models.CharField(max_length=48, verbose_name='Название жанра')
    slug = models.SlugField(max_length=48, unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель художественного произведения"""
    name = models.CharField(
        max_length=128,
        verbose_name='Название произведения'
    )
    # description = models.TextField(
    #     max_length=256,
    #     blank=True,
    #     null=True,
    #     verbose_name='Описание')
    year = models.IntegerField(verbose_name='Год выхода')
    category = models.ForeignKey(
        'Category',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория'
    )

    # genre = models.ManyToManyField(
    #     'Genre',
    #     through='TitleGenre',
    #     related_name='titles',
    #     verbose_name='Жанр'
    # )

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Модель связывающая произведение с жанрами"""
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title_id} относится к жанру {self.genre_id}'


class Review(models.Model):
    """Модель текстовых отзывов к произведениям."""
    title_id = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Произведение, к которому пишут отзыв',
    )
    text = models.TextField(
        verbose_name='Текст ревью',
        help_text='Текст нового ревью'
    )
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь',
        help_text='Пользователь, который производит ревью',
    )
    score = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Дата и время публикации',
        db_index=True
    )

    def __str__(self):
        return self.text[:20]


class Comment(models.Model):
    """Модель комментария к ревью."""
    review_id = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий',
        help_text='Комментарий, к ревью'
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст комментария'
    )
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        help_text='Автор комментария к ревью'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Дата и время публикации',
        db_index=True
    )

    def __str__(self):
        return self.text[:15]

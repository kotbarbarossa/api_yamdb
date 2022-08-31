from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime as dt
from django.core.exceptions import ValidationError
from reviews.managers import CustomUserManager

# длина вывода текстовой информации для моделей
STRING_LENGHT: int = 20


def year_validator(year):
    """Проверка что год не превышает текущий."""
    if year > dt.datetime.now().year:
        raise ValidationError(
            'Год выхода произведения не может превышать текущий.'
        )
    return year


class User(AbstractUser):
    """Модель пользователя."""
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLE = [
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
    ]

    role = models.CharField(
        'Пользовательская роль',
        max_length=20,
        choices=ROLE,
        default=USER
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN

    objects = CustomUserManager()

    class Meta:
        ordering = ['-id']


class ConfirmationCode(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    token = models.CharField(max_length=255)


class Category(models.Model):
    """Модель для категорий. Присваевается одна на произведение"""
    name = models.CharField(max_length=48, verbose_name='Название категории')
    slug = models.SlugField(max_length=48, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """Модель для Жанров. Множественное пристваивание на произведение"""
    name = models.CharField(max_length=48, verbose_name='Название жанра')
    slug = models.SlugField(max_length=48, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель художественного произведения"""
    name = models.CharField(
        max_length=128,
        verbose_name='Название произведения'
    )
    description = models.TextField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name='Описание')
    year = models.IntegerField(
        validators=[year_validator],
        verbose_name='Год выхода')
    category = models.ForeignKey(
        'Category',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория'
    )

    genre = models.ManyToManyField(
        'Genre',
        through='TitleGenre',
        related_name='titles',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Модель связывающая произведение с жанрами"""
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Название произведения'
    )
    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Название жанра'
    )

    class Meta:
        ordering = ('title_id',)
        verbose_name = 'Title Genre'
        verbose_name_plural = 'Title Genres'
        constraints = [
            models.UniqueConstraint(fields=['title_id', 'genre_id'],
                                    name=('unique genre')),
        ]

    def __str__(self):
        return f'{self.title_id} относится к жанру {self.genre_id}'


class Review(models.Model):
    """Модель текстовых отзывов к произведениям."""
    title = models.ForeignKey(
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
    score = models.PositiveIntegerField(
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name='Оценка произведения',
        help_text='Оценка произведения'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Дата и время публикации',
        db_index=True
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                name='unique_review',
                fields=['title', 'author'],
            )
        ]

    def __str__(self):
        return self.text[:STRING_LENGHT]


class Comment(models.Model):
    """Модель комментария к ревью."""
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Ревью',
        help_text='Ревью, к которому пишется комментарий'
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

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.text[:STRING_LENGHT]

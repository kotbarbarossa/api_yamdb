from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()


class Title(models.Model):
    pass


class Categorie(models.Model):
    pass


class Genre(models.Model):
    pass


class Review(models.Model):
    """Модель текстовых отзывов к произведениям."""
    title = models.ForeignKey(
        Title,
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
        User,
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
    review = models.ForeignKey(
        Review,
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
        User,
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

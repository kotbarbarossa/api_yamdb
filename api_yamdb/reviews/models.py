from django.db import models


class Category:
    """Модель для категорий. Присваевается одна на произведение"""
    title = models.CharField(max_length=48, verbose_name='Название категории')
    slug = models.SlugField(max_length=48, unique=True)

    def __str__(self):
        return self.slug


class Genre:
    """Модель для Жанров. Множественное пристваивание на произведение"""
    title = models.CharField(max_length=48, verbose_name='Название жанра')
    slug = models.SlugField(max_length=48, unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель художественного произведения"""
    title = models.CharField(
        max_length=128,
        verbose_name='Название произведения'
    )
    description = models.TextField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name='Описание')
    year = models.IntegerField(verbose_name='Год выхода')
    categorie = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        related_name='titles',
        verbose_name='Жанр'
    )

    def __str__(self):
        return self.title


class TitleGenre(models.Model):
    """Модель связывающая произведение с жанрами"""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} относится к жанру {self.genre}'

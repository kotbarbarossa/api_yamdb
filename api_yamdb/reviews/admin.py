from django.contrib import admin
from .models import User

from .models import Category, Comment, Genre, Review, Title, TitleGenre


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Админка произведений."""
    list_display = (
        'name',
        'year',
        'category',
    )
    search_fields = ('name',)
    list_filter = ('year',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка категроий."""
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Админка жанров."""
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)


@admin.register(TitleGenre)
class TitleGenreAdmin(admin.ModelAdmin):
    """Админка связей произведений с жанрами."""
    list_display = (
        'title_id',
        'genre_id',
    )
    list_filter = ('genre_id',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админка ревью."""
    list_display = ('pk', 'title_id', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админка комментариев."""
    list_display = ('pk', 'review_id', 'text', 'author', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
    )
    fieldsets = (
        (None, {
            'fields': (
                'username',
                'email',
                'first_name',
                'last_name',
                'role',
                'bio',
            )
        }),
    )

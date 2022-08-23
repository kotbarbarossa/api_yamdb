from django.contrib import admin

from .models import Category, Genre, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Админка произведений."""
    list_display = (
        'title',
        'description',
        'year',
        'categorie',
        'genre',
    )
    search_fields = ('title',)
    list_filter = ('year',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка категроий."""
    list_display = (
        'title',
        'slug',
    )
    search_fields = ('title',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Админка жанров."""
    list_display = (
        'title',
        'slug',
    )
    search_fields = ('title',)

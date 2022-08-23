from django.contrib import admin

from .models import Category, Genre, Title


class TitleAdmin(admin.ModelAdmin):
    """Админка произведений."""
    list_display = (
        'title',
        'description',
        'year',
        'categorie',
        'genre',
    )
    list_editable = ('categorie',)
    search_fields = ('title',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


class CategoriesAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
    )
    search_fields = ('title',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
    )
    search_fields = ('title',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoriesAdmin)
admin.site.register(Genre, GenreAdmin)

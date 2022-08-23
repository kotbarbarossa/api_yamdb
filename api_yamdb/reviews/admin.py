from django.contrib import admin
from .models import User

from .models import Category, Comment, Genre, Review, Title
from import_export import resources
from import_export.admin import ImportExportModelAdmin


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Админка произведений."""
    list_display = (
        'title',
        'description',
        'year',
        'category',
    )
    search_fields = ('title',)
    list_filter = ('year',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка категроий."""
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('title',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Админка жанров."""
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('title',)

from import_export.fields import Field
class ReviewResource(resources.ModelResource):
    title = Field(attribute='title', column_name='title_id')
    class Meta:
        model = Review


@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    """Админка ревью."""
    from_encoding = 'WINDOWS-1251'
    resource_class = ReviewResource
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админка комментариев."""
    list_display = ('pk', 'review', 'text', 'author', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'bio', 'first_name', 'last_name')

@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource
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

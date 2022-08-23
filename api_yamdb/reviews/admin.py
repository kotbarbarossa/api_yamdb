from django.contrib import admin
from .models import User

from .models import Category, Comment, Genre, Review, Title, TitleGenre
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.widgets import DateTimeWidget


@admin.register(Title)
class TitleAdmin(ImportExportModelAdmin):
    """Админка произведений."""
    from_encoding = 'utf-8'
    list_display = (
        'name',
        'year',
        'category',
    )
    search_fields = ('name',)
    list_filter = ('year',)


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    """Админка категроий."""
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(ImportExportModelAdmin):
    """Админка жанров."""
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)


@admin.register(TitleGenre)
class TitleGenreAdmin(ImportExportModelAdmin):
    """Админка связей произведений с жанрами."""
    list_display = (
        'genre_id',
        'title_id'
    )


class ReviewResource(resources.ModelResource):
    widget_datetime = DateTimeWidget(format="%Y-%m-%dT%H:%M:%S%Z")
    pub_date = Field(widget=widget_datetime)

    class Meta:
        model = Review


@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    """Админка ревью."""
    from_encoding = 'utf-8'
    resource_class = ReviewResource
    list_display = ('pk', 'title_id', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)


class CommentResource(resources.ModelResource):
    widget_datetime = DateTimeWidget(format="%Y-%m-%dT%H:%M:%S%Z")
    pub_date = Field(widget=widget_datetime)

    class Meta:
        model = Comment


@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    """Админка комментариев."""
    from_encoding = 'utf-8'
    resource_class = CommentResource
    list_display = ('pk', 'review_id', 'text', 'author', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name'
        )


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

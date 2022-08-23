from django.contrib import admin

from .models import Comment, Review
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ReviewResource(resources.ModelResource):

    class Meta:
        model = Review


@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    from_encoding = 'utf-8'
    resource_class = ReviewResource
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'text', 'author', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)

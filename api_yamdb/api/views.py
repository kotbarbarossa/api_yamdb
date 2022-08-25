from rest_framework import viewsets, mixins
from django.db.models import Avg
from reviews.models import Category, Genre, Title, Review

from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleWriteSerializer,
)


class CategoryGenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Кастомный класс для категорий и жанров."""
    # permission_classes = ()
    search_fields = ('name', 'slug',)


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Класс для модели Title"""
    review = Review.objects.all()
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    # permission_classes = ()
    # pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleWriteSerializer
        return TitleSerializer

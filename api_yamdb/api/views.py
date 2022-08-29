from secrets import token_hex

from django.core.mail import send_mail
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions, viewsets, mixins, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenViewBase

from api_yamdb import settings
from reviews.models import ConfirmationCode, User
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from reviews.models import Category, Genre, Title, Review
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from .serializers import (
    UserSerializer,
    UserMeSerializer,
    MyTokenObtainPairSerializer,
    SignUpSerializer,
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitleWriteSerializer,
)

from .permissions import IsAdminOrReadOnly, ReviewCommentPermission
from .filters import TitleFilter


class SignUpView(APIView):
    """Класс для регистрации."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data.get('username'))
            subject = 'Confirmation code'
            message = token_hex(16)
            ConfirmationCode.objects.create(
                user=user,
                token=message
            )
            send_mail(subject, message, settings.EMAIL_HOST_USER,
                      [request.data.get('email')])

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenViewBase):
    """Класс для получения токена."""
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = (AllowAny,)


class UserViewSet(ModelViewSet):
    """Вьюсет для User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[permissions.IsAuthenticated],
            serializer_class=UserMeSerializer)
    def me(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = UserMeSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            user.username = serializer.validated_data.get('username',
                                                          user.username)
            user.email = serializer.validated_data.get('email', user.email)
            user.first_name = serializer.validated_data.get('first_name',
                                                            user.first_name)
            user.last_name = serializer.validated_data.get('last_name',
                                                           user.last_name)
            user.bio = serializer.validated_data.get('bio', user.bio)
            user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class CategoryGenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Кастомный класс для категорий и жанров."""
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('name', 'slug',)
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Класс для модели Title."""
    review = Review.objects.all()
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    ordering_fields = ('name', 'year',)
    ordering = ('year',)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'PUT',):
            return TitleWriteSerializer
        return TitleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Получение и изменение комментариев."""
    serializer_class = CommentSerializer
    permission_classes = [ReviewCommentPermission]

    def get_queryset(self, *args, **kwargs):
        title_id = self.kwargs.get('title_id')
        get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    """Получение и изменение публикаций."""
    serializer_class = ReviewSerializer
    permission_classes = [ReviewCommentPermission]

    def get_queryset(self, *args, **kwargs):
        title_id = int(self.kwargs.get('title_id'))
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

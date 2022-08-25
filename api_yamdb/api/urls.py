from django.urls import path, include

from .views import CommentViewSet, ReviewViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/review_id/comments/',
    CommentViewSet,
    basename='comment'
)
urlpatterns = [
    path('v1/', include(router.urls)),
]

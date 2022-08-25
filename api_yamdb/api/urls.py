from django.urls import path, include

from .views import ReviewViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')

urlpatterns = [
    path('v1/', include(router.urls)),
]

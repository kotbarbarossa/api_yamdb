from django.urls import path, include

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (SignUpView, UserViewSet,
                    UserMeViewSet, MyTokenObtainPairView)

v1_router = routers.DefaultRouter()
v1_router.register(r'users', UserViewSet)
v1_router.register(r'users/(?P<username>[\w.@+-]+)', UserViewSet)
v1_router.register(r'users/me', UserMeViewSet, basename='user_id')

# (?P<username>[\w.@+-]+)/
urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
]

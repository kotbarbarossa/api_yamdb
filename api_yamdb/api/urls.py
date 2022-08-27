from django.urls import path, include

from rest_framework import routers

from .views import SignUpView, UserViewSet, MyTokenObtainPairView

v1_router = routers.DefaultRouter()
# v1_router.register(r'users/me', UserMeViewSet, basename='user_id')
v1_router.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
]

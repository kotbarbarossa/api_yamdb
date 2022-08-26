from secrets import token_hex

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, mixins, filters, permissions
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.views import TokenViewBase

from api_yamdb import settings
from reviews.models import ConfirmationCode, User
from .serializers import (UserSerializer, UserMeSerializer,
                          MyTokenObtainPairSerializer, SignUpSerializer)


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data.get('username'))
            subject = 'Confirmation code'
            message = token_hex(16)
            ConfirmationCode.objects.create(user=user,
                                 token=message)
            send_mail(subject, message, settings.EMAIL_HOST_USER,
                      [request.data.get('email')])

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenViewBase):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = (AllowAny,)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (permissions.IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class UserMeViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                    GenericViewSet):
    serializer_class = UserMeSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        return user

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.contrib.auth import get_user_model  # Move this import here
from django.contrib.auth.hashers import check_password


class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)

class UserLoginView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(phone_number=phone_number)
        except UserModel.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if check_password(password, user.password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
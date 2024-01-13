from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from django.core.mail import send_mail
from django.conf import settings as st
from django.contrib.auth import authenticate, login
from django.http import HttpResponseBadRequest
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from .models import CustomUser


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    def perform_create(self, serializer):
        # Override perform_create to customize user creation logic if needed
        user = serializer.save()
        user.send_authentication_code()

class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        user = CustomUser.objects.get(email=email)

        if user:
            if not user.is_authentication_code_expired():
                # Code still valid, user tries to login with the code
                entered_code = request.data.get('code', '')
                if entered_code == user.authentication_code:
                    # Generate a new token JWT
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    login(request, user)
                    return Response({'detail': 'Logged in successfully.',
                                     'access_token': access_token,
                                     }, status=status.HTTP_200_OK)
                elif entered_code:
                    return Response({'detail': 'Invalid code.'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'detail': 'Enter a  code.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Code has expired, send a new one
                user.send_authentication_code()
                return Response({'detail': 'Authentication code expired. New code sent.'}, status=status.HTTP_200_OK)
        else:
            return HttpResponseBadRequest({'detail': 'User not found.'})

class GetUsers(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class LogoutView(TokenViewBase, APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh_token")

        if refresh_token:
            try:
                # self.blacklist_token(refresh_token)
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"detail": "Logged Out successfully."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"detail": "Error during disconnection."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"detail": "RefreshTocken required to Disconnection."}, status=status.HTTP_400_BAD_REQUEST)
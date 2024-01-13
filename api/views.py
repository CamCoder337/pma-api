from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from django.core.mail import send_mail
from django.conf import settings as st
from django.contrib.auth import authenticate, login
from django.http import HttpResponseBadRequest
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
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    return Response({'detail': 'Logged in successfully.'}, status=status.HTTP_200_OK)
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

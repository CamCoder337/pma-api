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

class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        user = CustomUser.objects.get(email=email)
        if user:
            # Generate and send the authentication code by email
            authentication_code = "123456"  # Replace with your code generation logic
            send_mail(
                'Authentication Code',
                f'Your authentication code is: {authentication_code}',
                st.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            # Simulate login for demonstration purposes
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            return Response({'detail': 'Authentication code sent successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        

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
                else:
                    return Response({'detail': 'Invalid code.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Code has expired, send a new one
                user.send_authentication_code()
                return Response({'detail': 'Authentication code expired. New code sent.'}, status=status.HTTP_200_OK)
        else:
            return HttpResponseBadRequest({'detail': 'User not found.'})

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from django.core.mail import send_mail
from django.conf import settings as st
from django.contrib.auth import authenticate, login
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

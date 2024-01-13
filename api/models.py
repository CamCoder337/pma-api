from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
import datetime
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be specified.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser should have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser should have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    authentication_code = models.CharField(max_length=8, blank=True)
    code_expiration = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def generate_authentication_code(self):
        # Generate Auth Code
        return '123456'

    def send_authentication_code(self):
        # Send new Auth code by email
        authentication_code = self.generate_authentication_code()
        self.authentication_code = authentication_code
        self.code_expiration = timezone.now() + datetime.timedelta(minutes=5)  #5 min expiration
        self.save()
        send_mail(
                'PMA - Authentication Code',
                f'Your authentication code is: {authentication_code}',
                settings.EMAIL_HOST_USER,
                [self.email],
                fail_silently=False,
            )

    def is_authentication_code_expired(self):
        return timezone.now() > self.code_expiration



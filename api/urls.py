from django.urls import path
from .views import UserRegistrationView, UserLoginView, LogoutView, GetAuthenticatedUserView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('get-authenticated-user/', GetAuthenticatedUserView.as_view(), name='get-authenticated-user'),
]

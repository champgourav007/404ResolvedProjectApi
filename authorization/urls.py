from django.urls import path
from .views import RegisterView, login_user
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', login_user, name="loginUser"),
]
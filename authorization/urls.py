from ssl import CertificateError
from django.urls import path
from .views import RegisterView, login_user, CreatePostView


urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', login_user, name="login_user"),
    path('account/create-post', CreatePostView.as_view(), name='create_post')
]
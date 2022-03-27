from django.urls import path
from .views import MyObtainTokenPairView, RegisterView, login_user
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('temp/', login_user, name="loginUser"),
    # path(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/auth/login'})
]
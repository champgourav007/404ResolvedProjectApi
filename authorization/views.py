from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .models import Users
from .serializers import RegisterSerializer
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import login
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from . import authentication



@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    login_data = (request.data)
    print(login_data)
    
    user = authenticate(username = login_data["username"], password = login_data["password"])
    if user:
        login(request, user)
        data = {}
        data["status"] = 200
        loginedUser = Users.objects.get(user_id = user.id)
        print(loginedUser.email,end="\n\n\n")
        data["id"] = loginedUser.unique_id
        data["email"] = loginedUser.email
        data["first_name"] = loginedUser.first_name
        data["last_name"] = loginedUser.last_name
        data["token"] = authentication.create_access_token(user.id)
        data["refresh_token"] = authentication.create_refresh_token(user.id)
        return Response(data)
    else:
        return Response({"message" : "No account Found"})



class RegisterView(generics.CreateAPIView):
    queryset = Users.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


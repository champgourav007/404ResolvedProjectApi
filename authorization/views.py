import json
from django.forms import ValidationError
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .models import Users
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from . import authentication


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    # return Response(request.data)
    login_data = (request.data)
    print(login_data)
    
    # user = authenticate(username = "g1@g.in", password = "hello@123")
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

# @api_view(["POST"])
# @permission_classes([AllowAny])
# def login_user(request):

#         data = {}
#         reqBody = json.loads(request.body)
#         email1 = reqBody['Email_Address']
#         print(email1)
#         password = reqBody['password']
#         try:

#             Account = User.objects.get(Email_Address=email1)
#         except BaseException as e:
#             raise ValidationError({"400": f'{str(e)}'})

#         token = Token.objects.get_or_create(user=Account)[0].key
#         print(token)
#         if not check_password(password, Account.password):
#             raise ValidationError({"message": "Incorrect Login credentials"})

#         if Account:
#             if Account.is_active:
#                 print(request.user)
#                 login(request, Account)
#                 data["message"] = "user logged in"
#                 data["email_address"] = Account.email

#                 Res = {"data": data, "token": token}

#                 return Response(Res)

#             else:
#                 raise ValidationError({"400": f'Account not active'})

#         else:
#             raise ValidationError({"400": f'Account doesnt exist'})

from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .models import Users, PostModel, PostReplies
from .serializers import RegisterSerializer, CreatePostSerializer, GetPostSerializer, CreatePostRepliesSerializer
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import login
from rest_framework.response import Response
from django.contrib.auth import authenticate
from . import authentication
from authorization import serializers


#login user view
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


#register new user view
class RegisterView(generics.CreateAPIView):
    queryset = Users.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

#create post view
class CreatePostView(generics.CreateAPIView):
    queryset = PostModel.objects.all()
    permission_classes = [AllowAny,]
    serializer_class = CreatePostSerializer

#get all post view
@api_view(["GET"])
@permission_classes([AllowAny,])
def get_all_post(request):
    allpost = PostModel.objects.all()
    serializer = GetPostSerializer(allpost, many = True)
    return Response(serializer.data)


#reply view
class CreatePostRepliesView(generics.CreateAPIView):
    queryset = PostReplies.objects.all()
    permission_classes = [AllowAny,]
    serializer_class = CreatePostRepliesSerializer


#working not completed warning
#get post replies
@api_view(["GET"])
@permission_classes([AllowAny,])
def get_post_replies(request):
    queryset = PostReplies.objects.all()
    serializer = serializers.GetPostRepliesSerializer(queryset).data
    return Response(serializer)



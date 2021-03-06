from wsgiref import validate
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Users, PostModel, PostReplies
from authorization import models
from datetime import datetime


#new user resgister serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = ('password', 'password2', 'email', 'first_name', 'last_name', 'gender')
        extra_kwargs = {
            'first_name': {'required': True},
            'email': {'required': True},
            'password': {'required':True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password'])

        account = Users.objects.create(
            unique_id = validated_data['email'] + str(user.date_joined),
            first_name = user.first_name,
            last_name = user.last_name,
            full_name = user.first_name + " " + user.last_name,
            user_id = user.id,
            gender = validated_data['gender'],
            email = user.email,
        )

        user.save()
        account.save()
        return account

class CreatePostRepliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReplies
        exclude = ["is_selected", "replier_id"]

    def create(self, validated_data):
        print(validated_data,end="\n\n\n")
        post = validated_data["post"]
        post_reply = PostReplies.objects.create(
            replier_name = validated_data["replier_name"],
            message = validated_data["message"],
            post_id = post.id,
            # replier_id = post.email, can we get user email?
        )
        print(post_reply.post_id)
        post_reply.save()
        # print(post_reply.email)
        return post_reply
    

#create a post and add the data into the database
class CreatePostSerializer(serializers.ModelSerializer):
    # post_replies = GetPostRepliesSerializer()
    prices = {
        "Agriculture" : {
            "Skilled" : 495,
            "SemiSkilled" : 455,
            "Unskilled" : 417,
        },

        "Mine_Workers" : {
            "Skilled" : 437,
            "SemiSkilled" : 546,
            "Unskilled" : 654,
        },

        "Road-Workers" : {
            "Skilled" : 795,
            "SemiSkilled" : 724,
            "Unskilled" : 654,
        },

        "Loding-Unloading" : {
            "Skilled" : 654,
            "SemiSkilled" : 654,
            "Unskilled" : 654,
        },
        
        "Sweeping-Cleaning" : {
            "Skilled" : 654,
            "SemiSkilled" : 654,
            "Unskilled" : 654,
        },


    }


    class Meta:
        model = PostModel
        # fields = '__all__'
        exclude = ['post_id', 'is_active']
    
    def create(self, validated_data):
        post = PostModel.objects.create(
            title = validated_data["title"],
            description = validated_data["description"],
            skill_keywords = validated_data["skill_keywords"],
            tags = validated_data["tags"],
            no_of_workers = validated_data["no_of_workers"],
            post_id = self.create_work_id(validated_data["title"]),
            price = self.create_price(validated_data["price"], validated_data["skill_keywords"], validated_data["tags"], validated_data["no_of_workers"]),
        )
        post.post_image1 = validated_data["post_image1"]
        post.save()
        return post

    def create_work_id(self, post_title):
        post_title = ''.join(post_title.split())
        id = post_title + str(''.join(str(datetime.now()).split()))
        return id
    
    def create_price(self, input_price, skill, tags, workers):
        if tags in self.prices:
            total_price = self.prices[tags][skill] + input_price
        else:
            total_price = input_price
        return total_price*workers




#post model serializer
class GetPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = '__all__'

        
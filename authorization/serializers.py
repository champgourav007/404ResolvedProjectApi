import email
from email.policy import default
from random import choices
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Users
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = ('password', 'password2', 'email', 'first_name', 'last_name', 'gender', 'image', 'dob')
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
            image = validated_data['image'],
            dob=validated_data["dob"],
        )

        user.save()
        account.save()
        return account
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Users, PostModel, PostReplies



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


#create a post and add the data into the database
class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        # fields = '__all__'
        exclude = ['work_id', 'is_active']
    
    def create(self, validated_data):
        post = PostModel.objects.create(
            title = validated_data["title"],
            description = validated_data["description"],
            post_image = validated_data["post_image"],
            skill_keywords = validated_data["skill_keywords"],
            tags = validated_data["tags"],
            no_of_workers = validated_data["no_of_workers"],
        )
        post.work_id = 1

        post.save()
        return post


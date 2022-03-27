from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Users(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    unique_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    isEmailVerified = models.IntegerField(default=0, null=True)
    isMobilePhoneVerified = models.IntegerField(default=0, null=True)

    GENDER_CHOOICES = (
        (1,'M'),
        (2,'F')
    )
    gender = models.CharField(max_length=1 ,choices=GENDER_CHOOICES, default=1)
    dob = models.DateField()
    image = models.ImageField(upload_to="images")




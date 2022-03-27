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
    phone_no = models.IntegerField(null=True)

    GENDER_CHOOICES = (
        ('M','M'),
        ('F','F'),
    )
    gender = models.CharField(max_length=1 ,choices=GENDER_CHOOICES, default='M')
    dob = models.DateField(null=True)
    image = models.ImageField(upload_to="images", null=True)


class PostModel(models.Model):
    SKILL_CHOICES = (
        ('Skilled', 'Skilled'),
        ('Unskilled', 'Unskilled'),
        ('Semiskilled', 'Semiskilled'),
    )
    skill_keywords = models.CharField(max_length=20, choices=SKILL_CHOICES, default='Skilled')
    TAGS_CHOICES = (
        ('mason', 'Mason'),
        ('carpenter', 'Carpenter'),
    )
    tags = models.CharField(max_length=20, choices=TAGS_CHOICES, default='mason')
    work_id = models.IntegerField(auto_created=True, unique=True)
    time = models.DateField(auto_now_add=True)
    description = models.TextField()
    no_of_workers = models.IntegerField()

    
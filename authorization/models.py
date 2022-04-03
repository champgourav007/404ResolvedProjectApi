from django.db import models
from django.contrib.auth.models import User


class Users(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    unique_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    isEmailVerified = models.BooleanField(default=0)
    isMobilePhoneVerified = models.BooleanField(default=0)
    phone_no = models.IntegerField(null=True)

    GENDER_CHOOICES = (
        ('M','M'),
        ('F','F'),
    )
    gender = models.CharField(max_length=1 ,choices=GENDER_CHOOICES, default='M')
    dob = models.DateField(null=True)
    image = models.ImageField(upload_to="images", null=True)

    def __str__(self):
        return f"{self.fullname}"


#this is the model for the POST in the app
class PostModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    post_image1 = models.ImageField(upload_to="post_images", blank=True)
    post_id = models.CharField(max_length=255,  blank=True)

    SKILL_CHOICES = (
        ('Skilled', 'Skilled'),
        ('Unskilled', 'Unskilled'),
        ('Semiskilled', 'Semiskilled'),
    )
    skill_keywords = models.CharField(max_length=20, choices=SKILL_CHOICES, default='Skilled')

    TAGS_CHOICES = (
        ('Mason', 'Mason'),
        ('Carpenter', 'Carpenter'),
        ('Electician', 'Electrician'),
        ('Others', 'Others')

    )
    tags = models.CharField(max_length=20, choices=TAGS_CHOICES, default='Mason')

    post_created_on = models.DateTimeField(auto_now=True)
    no_of_workers = models.IntegerField(blank=True)
    is_active = models.BooleanField(default=1, null=True)

    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"{self.post_id}"



#each post has one or more replies
class PostReplies(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    replier_name = models.CharField(max_length=100)
    replier_id = models.EmailField()
    message = models.TextField()
    is_selected = models.BooleanField(default=False)

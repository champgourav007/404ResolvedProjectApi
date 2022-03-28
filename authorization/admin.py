from django.contrib import admin
from .models import PostModel, Users, PostReplies


admin.site.register(PostModel)
admin.site.register(PostReplies)
admin.site.register(Users)


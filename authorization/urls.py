from django.urls import path
from .views import RegisterView, get_post_replies, login_user, CreatePostView, get_all_post,CreatePostRepliesView


urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', login_user, name="login_user"),
    path('account/create-post/', CreatePostView.as_view(), name='create_post'),
    path('account/get-all-post/', get_all_post, name = "all-post"),
    path('account/create-reply-on-post/', CreatePostRepliesView.as_view(), name="creat-post-replies")
]
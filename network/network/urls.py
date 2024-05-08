
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts/new", views.create_post, name="create_post"),
    path("posts/all/<int:page>", views.get_posts, name="get_posts"),
    path("posts/followed/<int:page>", views.get_followed_posts, name="get_followed_posts"),
    path("posts/edit/<int:post_id>", views.edit_post, name="edit_post"),
    path("posts/like/<int:post_id>", views.like_post, name="like_post"),
    path("user/<int:user_id>", views.get_user_profile, name="get_user_profile"),
    path("user/follow/<int:user_id>", views.follow_user, name="follow_user"),
]

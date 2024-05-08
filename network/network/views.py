import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import User, Post, Follow, Like
from .utils import render_posts, get_followed_users_ids, get_followers_amount, is_user_followable, is_user_unfollowable


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/index.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/index.html")


@login_required
def create_post(request):
    if request.method == "POST":
        post = Post()

        data = json.loads(request.body)
        if data.get('content') is not None:
            post.content = data['content']
        post.author = request.user
        post.timestamp = timezone.now()

        post.save()

        return JsonResponse(data=None, status=201, safe=False)
    else:
        return JsonResponse(data=None, status=400, safe=False)


def get_posts(request, page):
    assert page >= 1

    posts = Post.objects.all().order_by('-timestamp')
    rendered_posts = render_posts(posts, page, request.user)

    return JsonResponse({
        'authenticated': request.user.is_authenticated,
        'posts': rendered_posts.get("posts"),
        'hasNext': rendered_posts.get("hasNext"),
        'hasPrevious': rendered_posts.get("hasPrevious"),
    })


@login_required
def get_followed_posts(request, page):
    assert page >= 1

    followed_users_ids = get_followed_users_ids(request.user)
    posts = Post.objects.filter(author_id__in=followed_users_ids).order_by('-timestamp')
    rendered_posts = render_posts(posts, page, request.user)

    return JsonResponse({
        'authenticated': request.user.is_authenticated,
        'posts': rendered_posts.get("posts"),
        'hasNext': rendered_posts.get("hasNext"),
        'hasPrevious': rendered_posts.get("hasPrevious"),
    })


def get_user_profile(request, user_id):
    profile_user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(author_id=user_id).order_by('-timestamp')

    return JsonResponse({
        'username': profile_user.username,
        'followers': get_followers_amount(profile_user),
        'following': get_followed_users_ids(profile_user).count(),
        'followable': is_user_followable(profile_user, request.user),
        'unfollowable': is_user_unfollowable(profile_user, request.user),
        'posts': render_posts(posts, 0, request.user).get("posts"),
        'authenticated': request.user.is_authenticated,
    })


@login_required
def follow_user(request, user_id):
    following = User.objects.get(pk=user_id)

    try:
        follow = Follow.objects.get(follower=request.user, following=following)
        follow.delete()
    except Follow.DoesNotExist:
        Follow.objects.create(follower=request.user, following=following)

    return JsonResponse(data=None, status=200, safe=False)


@login_required
def edit_post(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(pk=post_id)

        if post.author != request.user:
            return JsonResponse(data=None, status=403, safe=False)

        data = json.loads(request.body)
        if data.get('content') is not None:
            post.content = data['content']
            post.save()

        return JsonResponse(data=None, status=200, safe=False)


@login_required
def like_post(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(pk=post_id)

        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()

            return JsonResponse(data={
                'liked': False
            }, status=200)
        except Like.DoesNotExist:
            Like.objects.create(user=request.user, post=post)

            return JsonResponse(data={
                'liked': True
            }, status=200)

import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


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
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
@csrf_exempt
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
    return JsonResponse(data=None, status=400, safe=False)


def get_posts(request, page):
    posts = list(Post.objects.all().values())
    # TODO: GET ALL POSTS

    return JsonResponse({
        "posts": json.parse(posts)
    })


@login_required
def get_followed_posts(request, page):
    pass


def get_user_profile(request, user_id):
    pass


@login_required
def follow_user(request, user_id):
    pass


@login_required
def edit_post(request, post_id):
    pass


@login_required
def like_post(request, post_id):
    pass


def authenticated(request):
    return JsonResponse({
        "authenticated": request.user.is_authenticated
    })

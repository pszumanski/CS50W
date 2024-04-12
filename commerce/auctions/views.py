from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Category, Bid, Comment, AuctionWinner, Watchlist
from .forms import AuctionForm


def index(request):
    bids = {}
    for auction in Auction.objects.all():
        bids[auction] = [auction.starting_bid]
    for bid in Bid.objects.all():
        bids[bid.auction].append(bid)

    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all(),
        "bids": bids
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def new_auction(request):
    if request.method == "POST":
        form = AuctionForm(request.POST)

        if form.is_valid():
            new_auction = Auction(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                seller=request.user,
                starting_bid=form.cleaned_data["starting_bid"],
                category=form.cleaned_data["category"],
                image_url=form.cleaned_data["image_url"],
            )
            new_auction.save()

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/new_auction.html", {
                "form": form
            })
    return render(request, "auctions/new_auction.html", {
        "form": AuctionForm()
    })


def auction(request, auction_id):
    selected_auction = Auction.objects.get(id=auction_id)
    current_bid = Bid.objects.filter(auction=selected_auction).last()
    return render(request, "auctions/auction.html", {
        "user": request.user,
        "auction": selected_auction,
        "comments": Comment.objects.filter(auction=selected_auction),
        "bids_count": len(Bid.objects.filter(auction=selected_auction)),
        "current_bid": current_bid,
        "winner": AuctionWinner.objects.filter(auction=selected_auction).first(),
        "watchlist": Watchlist.objects.filter(user=request.user),
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all(),
    })


def category(request, category_id):
    selected_category = Category.objects.get(pk=category_id)
    return render(request, "auctions/category.html", {
        "category": selected_category,
        "auctions": Auction.objects.filter(category=selected_category),
    })


def watchlist(request):
    auctions = [watchlist_item.auction for watchlist_item in Watchlist.objects.filter(user=request.user)]
    return render(request, "auctions/watchlist.html", {
        "auctions": auctions,
    })

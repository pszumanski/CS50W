from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Category, Bid, Comment, AuctionWinner, Watchlist
from .forms import AuctionForm, BidForm


def index(request):
    bids = {}
    for auction in Auction.objects.all():
        bids[auction] = [auction.starting_bid]
    for bid in Bid.objects.all():
        bids[bid.auction].append(bid)

    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.filter(is_active=True),
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
    message = ""

    if request.method == "POST" and request.user.is_authenticated:
        form = BidForm(request.POST)

        if form.is_valid():
            selected_auction = Auction.objects.get(pk=auction_id)
            current_bid = Bid.objects.filter(auction=selected_auction).last()

            new_bid = Bid(
                bid=form.cleaned_data["bid"],
                bidder=request.user,
                auction=selected_auction,
            )

            if current_bid and not new_bid.bid > current_bid.bid:
                message = "Your bid must be higher than current bid."
            else:
                new_bid.save()
                return HttpResponseRedirect(reverse("auction", args=[auction_id]))
        else:
            message = "Invalid bid."

    watched_auctions = [watchlist_item.auction for watchlist_item in Watchlist.objects.filter(user=request.user)]
    return render(request, "auctions/auction.html", {
        "user": request.user,
        "auction": selected_auction,
        "comments": Comment.objects.filter(auction=selected_auction),
        "bids_count": len(Bid.objects.filter(auction=selected_auction)),
        "current_bid": current_bid,
        "winner": AuctionWinner.objects.filter(auction=selected_auction).first(),
        "watchlist": watched_auctions,
        "message": message,
        "form": BidForm(),
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all(),
    })


def category(request, category_id):
    selected_category = Category.objects.get(pk=category_id)
    return render(request, "auctions/category.html", {
        "category": selected_category,
        "auctions": Auction.objects.filter(active=True ,category=selected_category),
    })


@login_required
def watchlist(request):
    auctions = [watchlist_item.auction for watchlist_item in Watchlist.objects.filter(user=request.user)]
    return render(request, "auctions/watchlist.html", {
        "auctions": auctions,
    })


@login_required
def add_to_watchlist(request, auction_id):
    selected_auction = Auction.objects.get(pk=auction_id)
    auctions = [watchlist_item.auction for watchlist_item in Watchlist.objects.filter(user=request.user)]
    if selected_auction in auctions:
        Watchlist.objects.get(user=request.user, auction=selected_auction).delete()
    else:
        Watchlist.objects.create(user=request.user, auction=selected_auction)
    return HttpResponseRedirect(reverse("auction", args=[auction_id]))


@login_required
def close_auction(request, auction_id):
    selected_auction = Auction.objects.get(pk=auction_id)
    if selected_auction.seller == request.user and selected_auction.is_active:
        current_bid = Bid.objects.filter(auction=selected_auction).last()
        winner = current_bid.bidder
        if winner:
            AuctionWinner.objects.create(auction=selected_auction, winner=winner)
        selected_auction.is_active = False
        selected_auction.save()
    return HttpResponseRedirect(reverse("auction", args=[auction_id]))

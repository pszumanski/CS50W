from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)
    adult_only = models.BooleanField(default=True)


class Auction(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)


class AuctionWinner(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    winner = models.ForeignKey(User, on_delete=models.CASCADE)


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bid = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

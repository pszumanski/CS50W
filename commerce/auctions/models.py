from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)
    is_adult_only = models.BooleanField(default=True)

    def __str__(self):
        return self.category


class Auction(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    starting_bid = models.DecimalField(max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class AuctionWinner(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    winner = models.ForeignKey(User, on_delete=models.CASCADE)


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=7, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.bid)


class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

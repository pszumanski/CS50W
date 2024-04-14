from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auctions/new", views.new_auction, name="new_auction"),
    path("auctions/<int:auction_id>", views.auction, name="auction"),
    path("auctions/watchlist/<int:auction_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("auctions/close/<int:auction_id>", views.close_auction, name="close_auction"),
    path("auctions/comment/<int:auction_id>", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
]

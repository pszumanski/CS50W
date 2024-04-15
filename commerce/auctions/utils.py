from .models import Auction, Bid, Watchlist


def get_bids():
    bids = {}
    for auction in Auction.objects.all():
        bids[auction] = [auction.starting_bid]
    for bid in Bid.objects.all():
        bids[bid.auction].append(bid)
    return bids


def get_watchlist(user):
    if user.is_authenticated:
        return [watchlist_item.auction for watchlist_item in Watchlist.objects.filter(user=user)]
    return []

from django.contrib import admin
from .models import Auction, Bid

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('title', 'starting_price', 'end_time', 'created_by', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')
    list_filter = ('end_time', 'created_at')

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('auction', 'bidder', 'amount', 'bid_time')
    search_fields = ('auction__title', 'bidder__username')
    list_filter = ('bid_time',)

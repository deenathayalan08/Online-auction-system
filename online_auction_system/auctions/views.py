from django.shortcuts import render, redirect, get_object_or_404
from .models import Auction, Bid
from .forms import AuctionForm, BidForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

def auction_list(request):
    auctions = Auction.objects.filter(end_time__gt=timezone.now()).order_by('-created_at')
    return render(request, 'auctions/auction_list.html', {'auctions': auctions})

def auction_detail(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    bids = auction.bids.order_by('-amount')
    current_price = auction.current_price()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to place a bid.")
            return redirect('login')
        form = BidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data['amount']
            if bid_amount <= current_price:
                messages.error(request, f"Your bid must be higher than the current price (${current_price}).")
            else:
                Bid.objects.create(
                    auction=auction,
                    bidder=request.user,
                    amount=bid_amount
                )
                messages.success(request, "Your bid was placed successfully!")
                return redirect('auction_detail', auction_id=auction.id)
    else:
        form = BidForm()
    return render(request, 'auctions/auction_detail.html', {
        'auction': auction,
        'bids': bids,
        'current_price': current_price,
        'form': form
    })

@login_required
def create_auction(request):
    if request.method == 'POST':
        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.created_by = request.user
            auction.save()
            messages.success(request, "Auction created successfully!")
            return redirect('auction_detail', auction_id=auction.id)
    else:
        form = AuctionForm()
    return render(request, 'auctions/create_auction.html', {'form': form})

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('auction_list')
    else:
        form = UserRegisterForm()
    return render(request, 'auctions/register.html', {'form': form})

def user_login_view(request):
    if request.user.is_authenticated:
        return redirect('auction_list')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('auction_list')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'auctions/login.html')

def user_logout_view(request):
    logout(request)
    return redirect('auction_list')

from django import forms
from .models import Auction, Bid
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AuctionForm(forms.ModelForm):
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Auction
        fields = ['title', 'description', 'starting_price', 'image', 'end_time']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'min': '0.01', 'step': '0.01'})
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

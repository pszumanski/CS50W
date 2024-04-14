from django import forms
from .models import Category


class AuctionForm(forms.Form):
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'placeholder': 'Description'}))
    starting_bid = forms.DecimalField(label='Starting bid', decimal_places=2, localize=True,
                                      widget=forms.NumberInput(attrs={'placeholder': 'Starting bid'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    image_url = forms.URLField(label='Image', required=False,
                               widget=forms.URLInput(attrs={
                                'placeholder': 'Image URL'}))


class BidForm(forms.Form):
    bid = forms.DecimalField(label='Bid', decimal_places=2, localize=True,
                             widget=forms.NumberInput(attrs={'placeholder': 'Starting bid'}))

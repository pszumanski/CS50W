from django import forms
from .models import Category


class AuctionForm(forms.Form):
    choices = [category.category for category in Category.objects.all()]

    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'placeholder': 'Description'}))
    starting_bid = forms.IntegerField(label='Starting bid', choices=choices,
                                      widget=forms.NumberInput(attrs={'placeholder': 'Starting bid'}))
    category = forms.ChoiceField(label='Category', widget=forms.Select(attrs={'placeholder': 'Category'}))
    image_url = forms.URLField(label='Image', widget=forms.URLInput(attrs={
        'placeholder': 'Image URL',
        'required': 'false',
    }))

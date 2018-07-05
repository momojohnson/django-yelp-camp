from django import forms
from . models import Campground

class CampgroundForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    description = forms.CharField(
        widget=forms.Textarea(attrs={ 'placeholder': 'Please enter campground review?'}),
        max_length=4500,
        help_text='The max length of the text is 4500.')
    class Meta:
        model = Campground
        fields = ('name', 'price', 'location', 'image', 'description')
        widgets={
            'price': forms.NumberInput(attrs={'step':'0.50', 'min':'0.00'}),
        }
   
class CampgroundEditForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    description = forms.CharField(
        widget=forms.Textarea(attrs={ 'placeholder': 'Please enter campground review?'}),
        max_length=4500,
        help_text='The max length of the text is 4500.')
    class Meta:
        model = Campground
        fields = ('name', 'price', 'location', 'image', 'description')
        widgets={
            'price': forms.NumberInput(attrs={'step':'0.50', 'min':'0.00'}),
        }
    
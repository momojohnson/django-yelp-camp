from django import forms
from . models import Comment



class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={ 'placeholder': 'Please enter campground review?'}),
        max_length=4500,
        help_text='The max length of the text is 4500.')
    class Meta:
        model = Comment
        fields = ['comment']
        
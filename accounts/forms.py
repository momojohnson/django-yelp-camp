from registration.forms import RegistrationForm
from registration.forms import RegistrationFormUniqueEmail
from django.contrib.auth.models import User
from django import forms

class ProfileForm(RegistrationFormUniqueEmail):
    pass

class UserRegistrationForm(ProfileForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
        
        
 
from django.shortcuts import render
from django.views.generic import TemplateView
from registration.backends.default.views import RegistrationView
from .forms import ProfileForm, UserRegistrationForm
from . models import Profile
# Create your views here.
import django


class HomePageView(TemplateView):
    template_name = 'home.html'
    context = None
    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['title'] = 'Home'
        print(context)
        return context


class UserRegistration(RegistrationView):
    form_class = UserRegistrationForm
    def register(self, form_class):
        new_user = super(UserRegistration, self).register(form_class)
        Profile.objects.create(user=new_user)
        return new_user
        
   
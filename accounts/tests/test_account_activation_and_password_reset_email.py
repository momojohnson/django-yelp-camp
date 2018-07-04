from django.core import mail
from django.urls import reverse
from django.test import TestCase
from registration.users import UserModel
from django.apps import apps
from django.test import override_settings
from registration.models import RegistrationProfile

Site = apps.get_model('sites', 'Site')

@override_settings(ACCOUNT_ACTIVATION_DAYS=7,
                   REGISTRATION_DEFAULT_FROM_EMAIL='registration@email.com',
                   REGISTRATION_EMAIL_HTML=True,
                   DEFAULT_FROM_EMAIL='django@email.com')


class AccountActivationEmailTest(TestCase):
    user_info = {'username': 'momo',
                 'first_name': 'Momo',
                 'last_name':'johnson',
                 'email': 'mo@example.com',
                 'password': 'swordfish',
                 }
    registration_profile = RegistrationProfile
    def setUp(self):
        self.response = self.client.post(reverse('registration_register'), {'email':'mo@gmail.com'})
        new_user = UserModel().objects.create_user(**self.user_info)
        profile = self.registration_profile.objects.create_profile(new_user)
        profile.send_activation_email(Site.objects.get_current())
        self.email = mail.outbox[0]
    
    
    

    
    def test_email_subject(self):
          
          self.assertEqual(self.email.subject, "[Yelp Camp] Please activate your account")
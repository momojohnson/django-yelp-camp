from django.test import TestCase
from django.urls import reverse

from .. forms import UserRegistrationForm

class RegistrationFormTest(TestCase):
    def test_form_has_fields(self):
        form = UserRegistrationForm()
        expected = ['username', 'email', 'first_name', 'last_name',  'password1', 'password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
    
    def test_registration_response_status_code(self):
        self.response = self.client.post(reverse('registration_register'), { 'email': 'john@doe.com' })
        
        self.assertEqual(self.response.status_code, 200)
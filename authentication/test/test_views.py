from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import User, Profile
from ..serializers import RegisterSerializer
import json
from django.views.decorators.csrf import csrf_exempt


class AuthenticationAPITest(TestCase):

    def setUp(self):
        self.client = Client()
        user = User.objects.create(email='ronalipanigrahy88@gmail.com',
                                   username='Ronali',
                                   password='heyron',
                                   is_active=True,
                                   is_verified=True)
        Profile.objects.update(user=user)
        self.valid_profile_payload = {
            'DOB': None,
            'image': None
        }
        self.invalid_profile_payload = {
            'DOB': None,
            'image': 'abcdedf'
        }

        self.valid_payload = {
            'email': 'ronalipanigrahy88@gmail.com',
            'username': 'Ronali',
            'password': 'heyron',
        }
        self.invalid_payload = {
            'email': '',
            'username': 'Ron',
            'password': 'Ron',
        }
        self.valid_credentials = {
            'email': 'ronalipanigrahy88@gmail.com',
            'password': 'heyron'
        }
        self.invalid_credentials = {
            'email': 'rrrrrrr@gmail.com',
            'password': 'ron'
        }

    def test_register_user_with_valid_payload(self):
        response = self.client.post(reverse('register'), data=json.dumps(self.valid_payload),
                                    content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_with_invalid_payload(self):
        response = self.client.post(reverse('register'), data=json.dumps(self.invalid_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import User, Profile
from ..serializers import RegisterSerializer
import json
from django.views.decorators.csrf import csrf_exempt

CONTENT_TYPE = 'application/json'


class AuthenticationAPITest(TestCase):
    """ Test module for authentication APIs """

    def setUp(self):
        # initialize the APIClient app
        self.client = Client()
        user = User.objects.create(email='sonalipanigrahi125@gmail.com',
                                   username='SonaP',
                                   firstname='SonaliP',
                                   password='pbkdf2_sha256$216000$jVpAghSmHmIE$DOxGC9JUSflKuMo3SLKndHfR/6L8DU26HYoGbwxGOdg=',
                                   lastname='Panigrahy',
                                   is_active=True, is_verified=True)
        self.valid_payload = {
            'email': 'ronalipanigrahy88@gmail.com',
            'username': 'RonaP',
            'firstname': 'Ronali',
            'password': 'heyron',
            'lastname': 'Panigrahy'

        }
        self.invalid_payload = {
            'email': '',
            'username': 'SonaP',
            'firstname': 'Sonali',
            'password': 'heyron',
            'lastname': 'Panigrahy'
        }

        Profile.objects.update(user=user, DOB="1998-08-03")
        self.valid_profile_payload = {
            'image': None
        }
        self.invalid_profile_payload = {
            'image': None
        }
        self.valid_credentials = {
            'email': 'sonalipanigrahi125@gmail.com',
            'password': 'pbkdf2_sha256$216000$jVpAghSmHmIE$DOxGC9JUSflKuMo3SLKndHfR/6L8DU26HYoGbwxGOdg='
        }
        self.invalid_credentials = {
            'email': 'sonalipanigrahi125@gmail.com@gmail.com',
            'password': '_sha256$216000$jVpAghSmHmIE$DOxGC9JUSflKuMo3SLKndHfR/6L8DU26HYoGbwxGOdg='
        }

    def test_register_user_with_valid_payload(self):
        response = self.client.post(reverse('register'), data=json.dumps(self.valid_payload), content_type=CONTENT_TYPE,
                                    follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_with_invalid_payload(self):
        response = self.client.post(reverse('register'), data=json.dumps(self.invalid_payload),
                                    content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_email_with_valid_token(self):
        response = self.client.post(reverse('register'), data=json.dumps(self.valid_payload), content_type=CONTENT_TYPE)
        token = response.data['token']
        res = self.client.get('http://localhost:8000/authentication/email-verify/?token=' + token, content_type=CONTENT_TYPE)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_verify_email_with_invalid_token(self):
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo3LCJ1c2VybmFtZSI6Im1hbGljaGFuZG5pNUBnbWFpbC5jb20iLCJleHAiOjE2MDk4Njc5NDIsImVtYWlsIjoibWFsaWNoYW5kbmk1QGdtYWlsLmNvbSJ9.anw9BbFTJSjVa4j9Jur8YLQM-CNSVW2O4Zwm7xnBO"
        res = self.client.get('http://localhost:8000/authentication/email-verify/?token='+token, content_type=CONTENT_TYPE)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_valid_credentials(self):
        response = self.client.post(reverse('login'), data=json.dumps(self.valid_credentials), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(reverse('login'), data=json.dumps(self.invalid_credentials),content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_logout(self):
        self.client.post(reverse('login'), data=json.dumps(self.valid_credentials), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('logout'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_with_invalid_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.invalid_credentials), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('logout'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logout_without_login(self):
        response = self.client.get(reverse('logout'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_profile_retrieve(self):
        self.client.post(reverse('login'), data=json.dumps(self.valid_credentials), content_type=CONTENT_TYPE)
        response = self.client.get(reverse('user-profile'), content_type=CONTENT_TYPE)
        self.assertEqual(response.data['DOB'], "1998-08-03")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile_retrieve_without_login(self):
        response = self.client.get(reverse('user-profile'), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_update_its_user_profile_valid_payload(self):
        self.client.post(reverse('login'), data=json.dumps(self.valid_credentials), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('user-profile'), data=json.dumps(self.valid_profile_payload),
                                   content_type=CONTENT_TYPE, secure=False, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_update_its_user_profile_with_invalid_payload(self):
        self.client.post(reverse('login'), data=json.dumps(self.valid_credentials), content_type=CONTENT_TYPE)
        response = self.client.put(reverse('user-profile'), data=json.dumps(self.invalid_profile_payload),
                                   content_type=CONTENT_TYPE, secure=False, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

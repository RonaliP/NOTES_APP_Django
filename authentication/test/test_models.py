from django.test import TestCase
from ..models import User, Profile


class TestForUser(TestCase):
    def setUp(self):
        self.user=User.objects.create(firstname='Sonam',
                                      lastname='Mehta',
                                      email='ronalipanigrahy88@gmail.com',
                                      username='Ronali',
                                      password='heyron')

    def test_createuser(self):
        user = User.objects.get(username='Ronali')
        self.assertEqual(user.get_email(), "ronalipanigrahy88@gmail.com")


    def test_profile(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.get_DOB(), "")



from django.test import TestCase
from ..models import User, Profile


class UserTest(TestCase):
    """ Test module for User and UserProfile models """

    def setUp(self):
        self.user=User.objects.create(email='abhi08as.as@gmail.com',username='RonaliP',
                                      password='heyron')

    def test_create_user(self):
        user = User.objects.get(username='RonaliP')
        self.assertEqual(user.get_email(), "abhi08as.as@gmail.com")

    def test_create_user_profile(self):
        user_profile = Profile.objects.get(user=self.user)
        self.assertEqual(user_profile.get_image(), "default.jpg")

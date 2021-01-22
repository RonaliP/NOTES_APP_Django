from django.test import TestCase
from ..models import Notes, Labels
from authentication.models import User, Profile

class NotesTest(TestCase):
    """ Test module for Notes and Label models """

    def setUp(self):
        self.user = User.objects.create(email='abhi08as.as@gmail.com', username='RonaliP',
                                        password='heyron')
        Labels.objects.create(name='label 1', owner=self.user)
        Notes.objects.create(title='first note', content='this is my first note', owner=self.user)

    def test_create_note(self):
        note = Notes.objects.get(title='first note')
        self.assertEqual(note.get_content(), "this is my first note")

    def test_create_label(self):
        label = Labels.objects.get(owner=self.user)
        self.assertEqual(label.get_name(), "label 1")
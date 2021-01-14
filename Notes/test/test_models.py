from django.test import TestCase
from ..models import Notes, Labels
from authentication.models import User

class NotesAndLabelsTest(TestCase):


    def setUp(self):
        self.user=User.objects.create(firstname='Ronali',
                                      lastname='panigrahy',
                                      email='rpanigrahy.it.2016@nist.edu',
                                      username='Rona',
                                      password='Rona123')
        label = Labels.objects.create(name='FirstLabelOfRonali', owner=self.user)
        note = Notes.objects.create(title='FirstNote', content='HeyRonali......', owner=self.user)

    def test_create_label(self):
        label = Labels.objects.get(owner=self.user)
        self.assertEqual(label.get_name(), "FirstLabelOfRonali")

    def test_create_note(self):
        note = Notes.objects.get(title='')
        self.assertEqual(note.get_content(), "HeyRonali......")


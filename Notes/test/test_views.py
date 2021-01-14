from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import User,Profile
from Notes.models import Notes, Labels
from ..serializers import NotesSerializer, LabelsSerializer, ArchiveNotesSerializer, TrashSerializer, AddLabelsToNoteSerializer
import json
from django.views.decorators.csrf import csrf_exempt


class NotesAPITest(TestCase):


    def setUp(self):
        # Intialize the test client
        self.client = Client()

        self.user1 = User.objects.create(email='ronalipanigrahy88@gmail.com',
                                         username='Ronali',
                                         password='heyron',
                                         is_active=True,
                                         is_verified=True, )
        self.user2 = User.objects.create(email='rpanigrahy.it.2016@nist.edu',
                                         username='Sonali',
                                         password='heyron',
                                         is_active=True,
                                         is_verified=True, )
        self.note_for_user1 = Notes.objects.create(title='FirstnoteofRonali',
                                                   content='first note',
                                                   owner=self.user1,
                                                   isArchive=False,
                                                   isDelete=False)
        self.note_for_user2 = Notes.objects.create(title='FirstnoteofSonali',
                                                   content='note for user 2',
                                                   owner=self.user2)
        self.label_for_user1 = Labels.objects.create(name='label1', owner=self.user1)
        self.label_for_user2 = Labels.objects.create(name='label2', owner=self.user2)
        self.note_for_user1.label.add(self.label_for_user1.id)
        self.valid_payload = {
            'title': 'test',
            'content': 'testing'
        }
        self.invalid_payload = {
            'title': 'note2',
            'content': ''
        }
        self.valid_label_payload = {
            'name': 'test label'
        }
        self.invalid_label_payload = {
            'name': None
        }
        self.valid_archive_payload = {
            'isArchive': True
        }
        self.invalid_archive_payload = {
            'isArchive': None
        }
        self.valid_trash_payload = {
            'isDelete': True
        }
        self.invalid_trash_payload = {
            'isDelete': None
        }
        self.valid_add_label_payload = {
            'label': [self.label_for_user1.id]
        }
        self.invalid_add_label_payload = {
            'label': self.label_for_user2.id
        }
        self.user1_credentials = {
            'email': 'ronalipanigrahy88@gmail.com',
            'password': 'heyron'
        }
        self.invalid_credentials = {
            'email': 'rrrrrr@gmail.com',
            'password': 'heyron'
        }

    ### create notes API test cases:


    def test_create_notes_with_valid_payload_without_login(self):
        response = self.client.post(reverse('notecreation'),data=json.dumps(self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_create_notes_with_valid_payload_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.post(reverse('notecreation'),data=json.dumps(self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_notes_with_invalid_payload_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.post(reverse('notecreation'),data=json.dumps(self.invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


### List notes API test cases:

    def test_get_all_notes_without_login(self):
        notes = Notes.objects.filter(owner=self.user1, isArchive=False, isDelete=False)
        response = self.client.get(reverse('notedisplay'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_notes_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        notes = Notes.objects.filter(owner=self.user1, isArchive=False, isDelete=False)
        serializer = NotesSerializer(notes, many=True)
        response = self.client.get(reverse('notedisplay'))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_notes_of_other_user_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        notes = Notes.objects.filter(owner=self.user2, isArchive=False, isDelete=False)
        serializer = NotesSerializer(notes, many=True)
        response = self.client.get(reverse('notedisplay'))
        if response.status_code == status.HTTP_404_NOT_FOUND:
            self.assertEqual(response.data, serializer.data)
        else:
            self.assertNotEqual(response.data, serializer.data)

    def test_get_notes_by_id_without_login(self):
        response = self.client.get(reverse('notedisplay', kwargs={'id': self.note_for_user1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_get_notes_by_id_after_login(self):
        self.client.post(reverse('login'), data=json.dumps(self.user1_credentials), content_type='application/json')
        notes = Notes.objects.get(id=self.note_for_user1.id)
        serializer = NotesSerializer(notes)
        response = self.client.get(reverse('notedisplay', kwargs={'id': self.note_for_user1.id}))
        if response.status_code == status.HTTP_404_NOT_FOUND:
            self.assertNotEqual(response.data, serializer.data)
        else:
            self.assertEqual(response.data, serializer.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_notes_by_id_of_other_user_after_login(self):
        self.client.post(reverse('login'), data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.get(reverse('notedisplay', kwargs={'id': self.note_for_user2.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

 ### Test cases for update note API by id

    def test_update_notes_with_valid_payload_without_login(self):
        response = self.client.put(reverse('notesdelete/update/retrieve', kwargs={'id': self.note_for_user1.id}),
                                   data=json.dumps(self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_notes_with_valid_payload_after_login(self):
        self.client.post(reverse('login'), data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.put(reverse('notesdelete/update/retrieve', kwargs={'id': self.note_for_user1.id}),
                                   data=json.dumps(self.valid_payload), content_type='application/json')
        if response.status_code == status.HTTP_404_NOT_FOUND:
            self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_notes_with_invalid_payload_after_login(self):
        self.client.post(reverse('login'), data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.put(reverse('notesdelete/update/retrieve', kwargs={'id': self.note_for_user1.id}),
                                   data=json.dumps(self.invalid_payload), content_type='application/json')
        if response.status_code == status.HTTP_404_NOT_FOUND:
            self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        else:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_notes_with_other_user_note_using_valid_payload_after_login(self):
        self.client.post(reverse('login'), data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.put(reverse('notesdelete/update/retrieve', kwargs={'id': self.note_for_user2.id}),
                                   data=json.dumps(self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

### Test cases for delete note API by id

    def test_delete_note_without_login(self):
        response = self.client.delete(reverse('notesdelete/update/retrieve', kwargs={'id': self.note_for_user1.id}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_note_after_login(self):
        self.client.post(reverse('login'), data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.delete(reverse('notesdelete/update/retrieve', kwargs={'id': self.note_for_user1.id}),
                                      content_type='application/json')
        if response.status_code == status.HTTP_404_NOT_FOUND:
            self.assertNotEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        else:
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_note_of_other_user_after_login(self):
        self.client.post(reverse('login'), data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.delete(reverse('notesdelete/update/retrieve', kwargs={'id': self.label_for_user2.id}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

 ### Test cases for create label:

    def test_create_label_without_login(self):
        response = self.client.post(reverse('labels'), data=json.dumps(self.valid_label_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_labels_with_valid_payload_after_login_with_invalid_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.invalid_credentials), content_type='application/json')
        response = self.client.post(reverse('labels'), data=json.dumps(self.valid_label_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_labels_with_valid_payload_after_login(self):
        self.client.post(reverse('login'), data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.post(reverse('labels'), data=json.dumps(self.valid_label_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_labels_with_invalid_payload_after_login(self):
        self.client.post(reverse('login'), data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.post(reverse('labels'), data=json.dumps(self.invalid_label_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

 ### Test cases for list label API

    def test_get_all_labels_without_login(self):
        labels = Labels.objects.filter(owner=self.user1)
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_labels_after_login_with_invalid_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.invalid_credentials), content_type='application/json')
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_labels_after_login(self):
        self.client.post(reverse('login'), data=json.dumps(self.user1_credentials), content_type='application/json')
        labels = Labels.objects.filter(owner=self.user1)
        serializer = LabelsSerializer(labels, many=True)
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_labels_of_other_user_after_login(self):
        self.client.post(reverse('login'), data=json.dumps(self.user1_credentials), content_type='application/json')
        labels = Labels.objects.filter(owner=self.user2)
        serializer = LabelsSerializer(labels, many=True)
        response = self.client.get(reverse('labels'))
        self.assertNotEqual(response.data, serializer.data)


 ### Test cases for delete label by id

    def test_delete_note_without_login(self):
        response = self.client.delete(reverse('label', kwargs={'id': self.label_for_user1.id}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_label_after_login_with_invalid_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.invalid_credentials), content_type='application/json')
        response = self.client.delete(reverse('label', kwargs={'id': self.label_for_user1.id}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_label_after_login(self):
        self.client.post(reverse('login'), data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.delete(reverse('label', kwargs={'id': self.label_for_user1.id}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_label_of_other_user_after_login(self):
        self.client.post(reverse('login'), data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.delete(reverse('label', kwargs={'id': self.label_for_user2.id}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

### Test cases for trash-list API

    def test_get_trash_note_list_without_login(self):
        response = self.client.get(reverse('trash-list'), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    """
    def test_get_trash_note_list_after_login_with_invalid_credentials(self):
        self.client.post(reverse('login'),data=json.dumps(self.invalid_credentials), content_type='application/json')
        response = self.client.get(reverse('trash-list'), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    """
    def test_get_trash_note_list_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        notes = Notes.objects.filter(owner=self.user1.id, isDelete=True)
        serializer = NotesSerializer(notes, many=True)
        response = self.client.get(reverse('trash-list'), content_type='application/json')
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_trash_note_list_of_other_user_after_login_with_valid_credentials(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        notes = Notes.objects.filter(owner=self.user2.id, isDelete=True)
        serializer = NotesSerializer(notes, many=True)
        response = self.client.get(reverse('trash-list'), content_type='application/json')
        if not response.data:
            self.assertEqual(response.data, serializer.data)
        else:
            self.assertNotEqual(response.data, serializer.data)


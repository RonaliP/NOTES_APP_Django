from django.shortcuts import render
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from Notes.serializers import NotesSerializer, LabelsSerializer, \
    ArchiveNotesSerializer, TrashSerializer, AddLabelsToNoteSerializer,Notescollaborator
from Notes.permissions import IsOwner
from Notes.models import Notes, Labels
from django.db.models import Q
from rest_framework import generics, permissions, status
# FOR CACHING
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from django.views.decorators.cache import cache_page
import logging
import json


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
logger = logging.getLogger('django')

# Create your views here.

class CreateNotes(generics.ListCreateAPIView):
    """This Api will create notes for the current user """
    serializer_class = NotesSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    queryset = Notes.objects.all()

    def perform_create(self, serializer):
        owner = self.request.user
        note = serializer.save(owner=owner)
        cache.set(str(owner) + "-notes-" + str(note.id), note)
        if cache.get(str(owner) + "-notes-" + str(note.id)):
            logger.info(str(owner) + "-notes-" + str(note.id))
            logger.info("DATA STORED IN CACHE")
            return Response({'success': 'New note is created!!'}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """ Get notes list owned by current logged in user """
        owner = self.request.user
        return self.queryset.filter(Q(owner=owner) | Q(collaborator=owner), Q(isArchive=False, isDelete=False))


class DisplayNotes(generics.ListAPIView):
    """This Api will list out all the notes of current user from database """
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)


    """
    def get_queryset(self, notes=None):
        if cache.get(notes):
            print("data coming from cache")
            return cache.get(notes)
        else:
            data = self.queryset.filter(owner=self.request.user, isArchive=False, isDelete=False)
            cache.set(notes, data)
            print("data saved in cache")
            return cache.get(notes)
            
    """


class Notesearch(generics.GenericAPIView):
    """This is a search note api which will search for the existing notes"""
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    serializer_class = NotesSerializer

    def get_queryset(self, queryset=None):
        notes = []
        owner = self.request.user
        if queryset:
            searchlist = queryset.split(' ')
            if cache.get(queryset):
                notes = cache.get(queryset)
                logger.info("data is coming from cache")
            else:
                for query in searchlist:
                    notes = Notes.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
                    if notes:
                        cache.set(queryset, notes)
        else:
            notes = Notes.objects.all()
        return notes

    def get(self, request):
        queryset = request.GET.get('search')
        if queryset:
            note = self.get_queryset(queryset)
        else:
            note = self.get_queryset()
        serializer = NotesSerializer(note, many=True)
        return Response({'response_data': serializer.data}, status=status.HTTP_200_OK)

class NoteDetails(generics.RetrieveUpdateDestroyAPIView):
    """API to retrieve, update, and delete note by id """
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field = "id"

    def perform_update(self,serializer):
        """ Save notes model instance with updated data """
        owner = self.request.user
        note = serializer.save(owner=owner)
        updated_data=cache.add(str(owner)+"-notes-"+str(note.id), note)
        logger.info(updated_data)
        logger.info("updated note data is set")
        return note

    def get_queryset(self):
        """ Get note for given id owned by user """
        owner = self.request.user
        if cache.get(str(owner) + "-notes-" + str(self.kwargs[self.lookup_field])):
            queryset = cache.get(str(owner) + "-notes-" + str(self.kwargs[self.lookup_field]))
            logger.info("updated note data is coming from cache")
            return queryset

        else:
            queryset = self.queryset.filter(owner=owner, isDelete=False, id=self.kwargs[self.lookup_field])
            logger.info("updated note data is coming form database")
            cache.set(str(owner) + "-notes-" + str(self.kwargs[self.lookup_field]), queryset)
            return queryset

    def perform_destroy(self, instance):
        owner = self.request.user
        cache.delete(str(owner) + "-notes-" + str(self.kwargs[self.lookup_field]))
        instance.delete()

class CreateAndDisplayLabels(generics.ListCreateAPIView):
    """ API views for list and create labels for logged in user """
    serializer_class = LabelsSerializer
    queryset = Labels.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        owner = self.request.user
        label = serializer.save(owner)
        cache.set(str(owner) + "-labels-" + str(label.id), label)
        if cache.get(str(owner) + "-labels-" + str(label.id)):
            logger.info("Label data is stored in cache")
        return Response({'success': 'New label is added!!'}, status=status.HTTP_201_CREATED)

    """Implemented cache"""

    def get_queryset(self, queryset=None):

        if cache.get(queryset):
            print("label data coming from cache")
            return cache.get(queryset)
        else:
            labels = self.queryset.filter(owner=self.request.user)
            cache.set(queryset, labels)
            print("label data saved in cache")
            return cache.get(queryset)


class LabelDetails(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = LabelsSerializer
    queryset = Labels.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self, queryset=None):

        if cache.get(queryset):
            print("labeldata coming from cache")
            return cache.get(queryset)
        else:
            detailoflabel_id = self.queryset.filter(owner=self.request.user)
            cache.set(queryset, detailoflabel_id)
            print("labeldata saved in cache")
            return cache.get(queryset)


class ArchiveNote(generics.RetrieveUpdateAPIView):
    serializer_class = ArchiveNotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user, isDelete=False)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class NoteToTrash(generics.RetrieveUpdateAPIView):
    serializer_class = TrashSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class ArchiveNotesList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    serializer_class = ArchiveNotesSerializer
    queryset = Notes.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user, isArchive=True, isDelete=False)


class TrashList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    serializer_class = TrashSerializer
    queryset = Notes.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user, isDelete=True)


class AddLabelsToNote(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    serializer_class = AddLabelsToNoteSerializer
    queryset = Notes.objects.all()
    lookup_field = "id"

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class ListNotesInLabel(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    serializer_class = AddLabelsToNoteSerializer
    queryset = Notes.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user, label=self.kwargs[self.lookup_field])

class AddCollaboratorForNotes(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    serializer_class = Notescollaborator
    queryset = Notes.objects.all()
    lookup_field = "id"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return Response({'success':'Your new Collaborator is added'})

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)









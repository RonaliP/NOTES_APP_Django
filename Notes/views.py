from django.shortcuts import render
from Notes.serializers import NotesSerializer, LabelsSerializer, ArchiveNotesSerializer, TrashSerializer, \
    AddLabelsToNoteSerializer
from Notes.permissions import IsOwner
from Notes.models import Notes, Labels
from rest_framework import generics, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response


# Create your views here.

class CreateNotes(generics.CreateAPIView):
    serializer_class = NotesSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class DisplayNotes(generics.ListAPIView):
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user, isArchive=False, isDelete=False)



class NoteDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user, isDelete=False)


class CreateAndDisplayLabels(generics.ListCreateAPIView):
    serializer_class = LabelsSerializer
    queryset = Labels.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class LabelDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LabelsSerializer
    queryset = Labels.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


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
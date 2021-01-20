from rest_framework import serializers
from Notes.models import Notes, Labels
from authentication.models import User
from rest_framework.renderers import JSONRenderer
from datetime import datetime, timedelta
from django_celery_results.models import TaskResult
import time


class NotesSerializer(serializers.ModelSerializer):
    collaborator = serializers.StringRelatedField()

    class Meta:
        model = Notes
        fields = ['title', 'content', 'isArchive', 'isDelete','owner_id', 'collaborator']
        extra_kwargs = {'isDelete': {'read_only': True},
                        'isArchive': {'read_only': True}, 'collaborator': {'read_only': True},
                        'owner_id': {'read_only': True}
                        }

        def validate(self, data):
            title = data.get('title','')
            content = data.get('content','')
            return data





class Notescollaborator(serializers.ModelSerializer):
    collaborator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Notes
        fields = ['title', 'content','owner_id', 'collaborator']
        extra_kwargs = {'owner': {'read_only': True},
                        'title': {'read_only': True},
                        'content': {'read_only': True}}


class LabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labels
        fields = ['name']


class ArchiveNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title', 'content', 'isArchive']
        extra_kwargs = {'title': {'read_only': True}, 'content': {'read_only': True}}


class TrashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title', 'content', 'isDelete', 'isArchive']
        extra_kwargs = {'title': {'read_only': True}, 'content': {'read_only': True}, 'isArchive': {'read_only': True}}


class AddNotesInLabelsSerializer(serializers.PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = Labels
        fields = ['name']


class AddLabelsToNoteSerializer(serializers.ModelSerializer):
    label = AddNotesInLabelsSerializer(many=True, queryset=Labels.objects.all())

    class Meta:
        model = Notes
        fields = ['title', 'content', 'owner', 'label']
        extra_kwargs = {'owner': {'read_only': True}, 'title': {'read_only': True}, 'content': {'read_only': True}}

        def validate(self, attrs):
            labels = attrs.get('label', '')
            owner = attrs.get('owner', '')
            title = attrs.get('title', '')
            content = attrs.get('content', '')
            return attrs


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notes
        fields=['reminder']

        def validate(self,time):
            if time.replace(tzinfo=None)-datetime.now()<timedelta(seconds=10):
                raise serializers.ValidationError('SET THE REMINDER FOR VALID TIME')
            return time


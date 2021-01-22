from rest_framework import serializers
from Notes.models import Notes, Labels
from authentication.models import User
from datetime import datetime, timedelta

class NotesSerializer(serializers.ModelSerializer):
    collaborator = serializers.StringRelatedField(many=True, read_only=True)
    label = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model= Notes
        fields=['title','content','label','collaborator']

        def validate(self, data):
            title = data.get('title','')
            content = data.get('content','')
            return data


class LabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Labels
        fields=['name','owner']
        extra_kwargs = {'owner':{'read_only':True}}



class ListNotesSerializer(serializers.ModelSerializer):
    label = serializers.StringRelatedField(many=True, read_only=True)
    collaborator = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Notes
        fields=['owner','title','content','label','collaborator','reminder']
        extra_kwargs = {'owner': {'read_only': True}, 'title': {'read_only': True}, 'content': {'read_only': True}, 'reminder': {'read_only': True}}


class ArchiveNotesSerializer(serializers.ModelSerializer):
    label = serializers.StringRelatedField(many=True, read_only=True)
    collaborator = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model= Notes
        fields=['owner_id','title','content','isArchive','label','collaborator']
        extra_kwargs = {'title': {'read_only': True},'content': {'read_only': True},'owner_id': {'read_only': True}}


class TrashSerializer(serializers.ModelSerializer):
    label = serializers.StringRelatedField(many=True, read_only=True)
    collaborator = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model= Notes
        fields=['owner_id','title','content','isDelete','isArchive','label','collaborator']
        extra_kwargs = {'title': {'read_only': True},'content': {'read_only': True},'isArchive':{'read_only':True}, 'owner_id': {'read_only': True}}


class AddLabelsToNoteSerializer(serializers.ModelSerializer):
    label = serializers.CharField()
    collaborator = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Notes
        fields=['owner','title','content','label','collaborator']
        extra_kwargs = {'owner': {'read_only': True}, 'title': {'read_only': True},'content': {'read_only': True}}

        def validate(self, attrs):
            label = attrs.get('label','')
            return label


class AddCollaboratorSerializer(serializers.ModelSerializer):
    collaborator = serializers.EmailField()
    label = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Notes
        fields = ['title','content','label','owner','collaborator']
        extra_kwargs = {'owner': {'read_only': True}, 'title': {'read_only': True}, 'content': {'read_only': True}}

        def validate(self, attrs):
            collaborator = attrs.get('collaborator','')
            return attrs


class ReminderSerializer(serializers.ModelSerializer):
    collaborator = serializers.StringRelatedField(read_only=True)
    label = serializers.StringRelatedField(read_only=True)
    reminder = serializers.DateTimeField()
    class Meta:
        model = Notes
        fields = ['title','content','owner','reminder','label','collaborator']
        extra_kwargs = {'owner': {'read_only': True}, 'title': {'read_only': True}, 'content': {'read_only': True}}
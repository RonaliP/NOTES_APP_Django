from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Notes
from datetime import datetime, timedelta
from django_celery_results.models import TaskResult
import time

@shared_task()
def set_reminder():
    notes = Notes.objects.filter(isDelete=False).exclude(reminder=None)
    for note in notes:
        if note.reminder.replace(tzinfo=None) - datetime.now() <= timedelta(seconds=1):
            note.reminder = None
            note.save()
            return note



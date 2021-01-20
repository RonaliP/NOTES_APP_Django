from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Notes
from datetime import datetime, timedelta
from django_celery_results.models import TaskResult
import time

@shared_task()
def set_reminder():
    notes = Notes.objects.filter(is_trash=False).exclude(reminder=None)
    for note in notes:
        reminder_timedelta=note.reminder.replace(tzinfo=None)-datetime.now()
        if reminder_timedelta <= timedelta(minutes=1):
            note.reminder=None
            note.save()
            return f'{note}reminder'
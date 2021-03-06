from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TODO_LIST.settings')
app = Celery('TODO_LIST')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = 'UTC'

app.conf.beat_schedule={
    'check reminder':{
        'task':'Notes.tasks.set_reminder',
        'schedule':3,
    }
}
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
from django.db import models
from authentication.models import User
from django.contrib.postgres.fields import JSONField

# Create your models here.


class Labels(models.Model):
    name = models.TextField(db_index=True)
    owner=models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=False, blank=False)

class Notes(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title=models.TextField()
    content=models.TextField(db_index=True)
    label = models.ManyToManyField(to=Labels)
    isArchive = models.BooleanField(default=False)
    isDelete = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    collaborator = models.ForeignKey(to=User, related_name='user', on_delete=models.CASCADE, blank=True, null=True)
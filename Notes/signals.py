from django.db.models.signals import post_delete
from authentication.models import User
from Notes.models import Notes
from django.dispatch import receiver

@receiver(post_delete,sender=User)
def delete_user(sender, instance, **kwargs):
    notes = Notes.objects.filter(collaborator__contains=instance.id)
    for note in notes:
        note.collaborator=None
        note.save()

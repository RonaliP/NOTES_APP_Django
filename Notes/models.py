from django.db import models
from authentication.models import User

# Create your models here.
class Notes(models.Model):
    title=models.TextField()
    content=models.TextField(db_index=True)
    writer=models.ForeignKey(to=User,on_delete=models.CASCADE)
    date = models.DateTimeField(null=False, blank=False)

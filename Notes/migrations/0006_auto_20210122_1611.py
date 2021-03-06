# Generated by Django 3.1.5 on 2021-01-22 10:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Notes', '0005_notes_reminder'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='trashedAt',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.RemoveField(
            model_name='notes',
            name='collaborator',
        ),
        migrations.AddField(
            model_name='notes',
            name='collaborator',
            field=models.ManyToManyField(related_name='collaborator', to=settings.AUTH_USER_MODEL),
        ),
    ]

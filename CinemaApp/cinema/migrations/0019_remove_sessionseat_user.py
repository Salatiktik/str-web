# Generated by Django 4.2.1 on 2023-05-24 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0018_alter_sessionseat_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sessionseat',
            name='user',
        ),
    ]

# Generated by Django 4.2.1 on 2023-11-21 23:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0032_rotationsettings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rotationsettings',
            name='is_rotation_enabled',
        ),
    ]

# Generated by Django 4.2.1 on 2023-05-24 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0009_profile_session_seat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='session_seat',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='cinema.sessionseat'),
        ),
    ]

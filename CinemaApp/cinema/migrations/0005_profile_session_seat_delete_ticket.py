# Generated by Django 4.2.1 on 2023-05-23 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0004_ticket_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='session_seat',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='cinema.sessionseat'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]

# Generated by Django 4.2.1 on 2023-09-08 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0027_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='photo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]

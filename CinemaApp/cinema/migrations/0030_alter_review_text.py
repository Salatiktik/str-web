# Generated by Django 4.2.1 on 2023-09-11 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0029_faq'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(max_length=2000),
        ),
    ]

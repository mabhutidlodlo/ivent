# Generated by Django 3.1.3 on 2021-01-19 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_writer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='writer',
        ),
    ]

# Generated by Django 5.1.4 on 2024-12-10 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_alter_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
    ]
# Generated by Django 5.1.4 on 2024-12-10 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_alter_user_rated_movies'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Profile',
        ),
    ]

# Generated by Django 4.2.1 on 2023-05-21 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_bankuser_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankuser',
            name='user',
        ),
    ]

# Generated by Django 4.2.1 on 2023-05-27 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_bankuser_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankuser',
            name='counts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bankuser',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]

# Generated by Django 4.2.1 on 2023-05-27 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0005_accountbills_remark_accountbills_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountbills',
            name='money',
            field=models.FloatField(default=0),
        ),
    ]

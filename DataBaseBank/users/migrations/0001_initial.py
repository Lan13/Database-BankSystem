# Generated by Django 4.2.1 on 2023-05-21 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankUser',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('tel', models.CharField(max_length=11)),
                ('address', models.CharField(max_length=100)),
            ],
        ),
    ]

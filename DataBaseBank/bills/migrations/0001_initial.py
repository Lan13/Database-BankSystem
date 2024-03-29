# Generated by Django 4.2.1 on 2023-05-27 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0004_alter_useraccounts_money'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountBills',
            fields=[
                ('bill_id', models.AutoField(primary_key=True, serialize=False)),
                ('changes', models.FloatField()),
                ('update_time', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='AccountBills', to='accounts.useraccounts')),
            ],
        ),
    ]

# Generated by Django 4.2.6 on 2023-10-28 11:29

import accounts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', accounts.models.QIUserManager()),
            ],
        ),
    ]

# Generated by Django 4.2.6 on 2023-11-04 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0019_ordertransaction_check_and_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertransaction',
            name='check_and_reject',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 4.2.6 on 2023-11-01 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0010_rename_gateway_reference_ordertransaction_trxid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertransaction',
            name='gateway',
            field=models.CharField(max_length=50),
        ),
    ]

# Generated by Django 4.2.6 on 2023-10-30 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0008_alter_ordertransaction_gateway_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertransaction',
            name='gateway',
            field=models.CharField(choices=[('bKash', 'bKash'), ('rocket', 'Rocket')], max_length=50),
        ),
    ]

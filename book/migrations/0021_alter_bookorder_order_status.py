# Generated by Django 4.2.6 on 2023-11-04 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0020_ordertransaction_check_and_reject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookorder',
            name='order_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('invoice_initiatd', 'Invoice Initiatd'), ('processing', 'Processing'), ('confirm', 'Confirm'), ('payment_reject', 'Payment Reject'), ('payment_pending', 'Payment Pending'), ('shipped', 'Shipped'), ('completed', 'Completed'), ('canceled', 'Canceled')], max_length=100),
        ),
    ]

# Generated by Django 4.2.6 on 2023-10-30 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_address'),
        ('book', '0005_remove_bookorder_delivery_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookorderitem',
            old_name='num_of_item',
            new_name='quantity',
        ),
        migrations.RenameField(
            model_name='bookorderitem',
            old_name='sale_amount',
            new_name='sale_price',
        ),
        migrations.AlterField(
            model_name='bookorder',
            name='delivery_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order_delivery_address', to='accounts.address'),
        ),
    ]

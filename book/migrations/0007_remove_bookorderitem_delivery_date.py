# Generated by Django 4.2.6 on 2023-10-30 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_rename_num_of_item_bookorderitem_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookorderitem',
            name='delivery_date',
        ),
    ]

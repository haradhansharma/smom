# Generated by Django 4.2.6 on 2023-11-02 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asrams', '0004_asram_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='asram',
            name='about',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.2.6 on 2023-10-29 13:21

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('asrams', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asram',
            name='acharya',
        ),
        migrations.AddField(
            model_name='asram',
            name='asram_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Phone number will be public where vokto will call for any necessity!', max_length=128, null=True, region=None, verbose_name='Ashram Phone'),
        ),
        migrations.AddField(
            model_name='asram',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='asram',
            name='slug',
            field=models.SlugField(default='', unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='asram',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='asram',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to='asrams/banner'),
        ),
        migrations.CreateModel(
            name='Sanyashi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=152)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='sanyashi/avatar')),
                ('is_head', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('asram', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sanyasies', to='asrams.asram')),
            ],
        ),
    ]

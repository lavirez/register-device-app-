# Generated by Django 3.2 on 2022-08-23 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_devicetoken_device_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paidorder',
            name='products',
        ),
    ]

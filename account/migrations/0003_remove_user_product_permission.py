# Generated by Django 3.2 on 2022-07-30 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='product_permission',
        ),
    ]

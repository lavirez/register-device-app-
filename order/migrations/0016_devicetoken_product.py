# Generated by Django 3.2 on 2022-08-30 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20220830_0103'),
        ('order', '0015_remove_paidorder_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicetoken',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product'),
        ),
    ]

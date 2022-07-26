# Generated by Django 3.2 on 2022-08-20 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20220812_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='parent',
            field=models.ForeignKey(blank=True, limit_choices_to={'product_type': 'normal'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product', verbose_name='محصول مربوطه'),
        ),
    ]

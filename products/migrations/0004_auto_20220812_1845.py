# Generated by Django 3.2 on 2022-08-12 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='codes',
            field=models.ManyToManyField(blank=True, to='products.PieceOfCode', verbose_name='کد(ها)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='files',
            field=models.ManyToManyField(blank=True, to='products.ProductFile', verbose_name='فایل(ها)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='permissions',
            field=models.ManyToManyField(blank=True, to='products.ProductPermission', verbose_name='دسترسی ها'),
        ),
    ]

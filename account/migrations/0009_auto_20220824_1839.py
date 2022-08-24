# Generated by Django 3.2 on 2022-08-24 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20220824_1839'),
        ('account', '0008_alter_userapppermission_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userproductpermission',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
        migrations.DeleteModel(
            name='UserAppPermission',
        ),
    ]

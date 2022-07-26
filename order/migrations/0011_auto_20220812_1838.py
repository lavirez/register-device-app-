# Generated by Django 3.2 on 2022-08-12 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_parent'),
        ('order', '0010_auto_20220812_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicetoken',
            name='products',
        ),
        migrations.RemoveField(
            model_name='paidorder',
            name='device_limit',
        ),
        migrations.RemoveField(
            model_name='paidorder',
            name='device_token',
        ),
        migrations.AddField(
            model_name='paidorder',
            name='rose_permission',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='ProductLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.AddField(
            model_name='paidorder',
            name='line_items',
            field=models.ManyToManyField(to='order.ProductLine'),
        ),
    ]

# Generated by Django 3.0.6 on 2020-06-06 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_auto_20200606_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]

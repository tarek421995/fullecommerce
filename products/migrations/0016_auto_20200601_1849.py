# Generated by Django 3.0.6 on 2020-06-01 15:49

import django.core.files.storage
from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20200601_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfile',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\hhhhh\\desktop\\tarek\\static_cdn\\protected_media'), upload_to=products.models.upload_product_file_loc),
        ),
    ]
# Generated by Django 3.0.6 on 2020-06-07 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200530_0003'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_business',
            field=models.BooleanField(default=False),
        ),
    ]

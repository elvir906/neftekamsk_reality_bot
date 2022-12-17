# Generated by Django 4.1.3 on 2022-12-16 08:06

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baza', '0015_alter_apartment_photo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='photo_id',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, default=[], size=None),
        ),
    ]

# Generated by Django 4.1.3 on 2022-12-16 08:02

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baza', '0012_alter_apartment_photo_id_alter_house_photo_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='photo_id',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, default=['AgACAgIAAxkBAAIgfmOa2LfSqhWFbSd3cezejErLCUPQAAIWvzEb1EDYSPq4knc5HwhjAQADAgADeQADLAQ'], size=None),
        ),
    ]
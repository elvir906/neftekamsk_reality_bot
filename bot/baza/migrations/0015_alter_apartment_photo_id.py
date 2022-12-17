# Generated by Django 4.1.3 on 2022-12-16 08:05

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baza', '0014_alter_apartment_photo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='photo_id',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, default=['A', 'g', 'A', 'C', 'A', 'g', 'I', 'A', 'A', 'x', 'k', 'B', 'A', 'A', 'I', 'g', 'f', 'm', 'O', 'a', '2', 'L', 'f', 'S', 'q', 'h', 'W', 'F', 'b', 'S', 'd', '3', 'c', 'e', 'z', 'e', 'j', 'E', 'r', 'L', 'C', 'U', 'P', 'Q', 'A', 'A', 'I', 'W', 'v', 'z', 'E', 'b', '1', 'E', 'D', 'Y', 'S', 'P', 'q', '4', 'k', 'n', 'c', '5', 'H', 'w', 'h', 'j', 'A', 'Q', 'A', 'D', 'A', 'g', 'A', 'D', 'e', 'Q', 'A', 'D', 'L', 'A', 'Q'], size=None),
        ),
    ]

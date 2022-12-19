# Generated by Django 4.1.3 on 2022-12-19 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baza', '0019_alter_apartment_area_alter_house_area_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='house',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='land',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='room',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='townhouse',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, verbose_name='Цена'),
        ),
    ]

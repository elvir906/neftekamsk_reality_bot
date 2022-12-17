# Generated by Django 4.1.3 on 2022-12-15 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baza', '0007_alter_individuals_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='photo_id',
            field=models.CharField(default='AgACAgIAAxkBAAIgfmOa2LfSqhWFbSd3cezejErLCUPQAAIWvzEb1EDYSPq4knc5HwhjAQADAgADeQADLAQ', max_length=500, verbose_name='ID фотографий'),
        ),
        migrations.AddField(
            model_name='house',
            name='photo_id',
            field=models.CharField(default='AgACAgIAAxkBAAIgfmOa2LfSqhWFbSd3cezejErLCUPQAAIWvzEb1EDYSPq4knc5HwhjAQADAgADeQADLAQ', max_length=500, verbose_name='ID фотографий'),
        ),
        migrations.AddField(
            model_name='land',
            name='photo_id',
            field=models.CharField(default='AgACAgIAAxkBAAIgfmOa2LfSqhWFbSd3cezejErLCUPQAAIWvzEb1EDYSPq4knc5HwhjAQADAgADeQADLAQ', max_length=500, verbose_name='ID фотографий'),
        ),
        migrations.AddField(
            model_name='room',
            name='photo_id',
            field=models.CharField(default='AgACAgIAAxkBAAIgfmOa2LfSqhWFbSd3cezejErLCUPQAAIWvzEb1EDYSPq4knc5HwhjAQADAgADeQADLAQ', max_length=500, verbose_name='ID фотографий'),
        ),
        migrations.AddField(
            model_name='townhouse',
            name='photo_id',
            field=models.CharField(default='AgACAgIAAxkBAAIgfmOa2LfSqhWFbSd3cezejErLCUPQAAIWvzEb1EDYSPq4knc5HwhjAQADAgADeQADLAQ', max_length=500, verbose_name='ID фотографий'),
        ),
    ]
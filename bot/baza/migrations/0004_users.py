# Generated by Django 4.1.3 on 2022-12-14 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baza', '0003_land_garage_land_sauna'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=15, verbose_name='Подписчики')),
            ],
        ),
    ]

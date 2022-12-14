# Generated by Django 4.1.3 on 2022-12-26 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baza', '0023_alter_apartment_user_id_alter_house_user_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(verbose_name='id')),
                ('phone_number', models.CharField(max_length=13, verbose_name='Номер телефона')),
                ('category', models.CharField(max_length=100, verbose_name='Категория поиска')),
                ('room_quantity', models.IntegerField(default=10, verbose_name='Количество комнат')),
                ('last_floor', models.BooleanField(default=True, verbose_name='Рассм. кр. этажи')),
                ('limit', models.BigIntegerField(verbose_name='Предел суммы')),
                ('source', models.CharField(max_length=100, verbose_name='Источник оплаты')),
                ('initial_payment', models.BooleanField(default=True, verbose_name='наличие ПВ')),
                ('microregion', models.CharField(max_length=100, verbose_name='микрорайон поиска')),
                ('comment', models.TextField(help_text='Описание', max_length='500', verbose_name='Описание')),
            ],
        ),
    ]

from django.db import models


class Apartment(models.Model):
    room_quantity = models.DecimalField(
        verbose_name='Количество комнат',
        decimal_places=0,
        max_digits=1
    )
    street_name = models.CharField(
        max_length=100,
        verbose_name='Название улицы'
    )
    number_of_house = models.CharField(
        max_length=10,
        verbose_name='Номер дома'
    )
    floor = models.DecimalField(
        decimal_places=0,
        max_digits=2,
        verbose_name='Этаж'
    )
    number_of_floors = models.DecimalField(
        decimal_places=0,
        max_digits=2,
        verbose_name='Этажность дома'
    )
    area = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        verbose_name='площадь квартиры'
    )
    description = models.TextField(
        max_length='1000',
        help_text='Описание',
        verbose_name='Описание квартиры'
    )
    price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name='Цена',
        blank=True
    )
    author = models.CharField(
        verbose_name='Автор',
        blank=True,
        max_length=200
    )
    phone_number = models.CharField(
        max_length=13,
        verbose_name='Номер телефона',
        blank=True
    )
    agency = models.CharField(
        max_length=100,
        verbose_name='Название агентства',
        blank=True
    )
    encumbrance = models.BooleanField(
        verbose_name='Обременение',
        default='False'
    )
    children = models.BooleanField(
        verbose_name='Дети в доле',
        default='False'
    )
    mortage = models.BooleanField(
        verbose_name='Ипотека',
        default='False'
    )
    pub_date = models.DateTimeField(
        auto_now_add=False,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'


class Room(models.Model):
    street_name = models.CharField(
        max_length=100,
        verbose_name='Название улицы'
    )
    number_of_house = models.CharField(
        max_length=10,
        verbose_name='Номер дома'
    )
    floor = models.DecimalField(
        decimal_places=0,
        max_digits=2,
        verbose_name='Этаж'
    )
    number_of_floors = models.DecimalField(
        decimal_places=0,
        max_digits=2,
        verbose_name='Этажность дома'
    )
    area = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        verbose_name='площадь комнаты'
    )
    description = models.TextField(
        max_length='1000',
        help_text='Описание',
        verbose_name='Описание комнаты'
    )
    price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name='Цена',
        blank=True
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    author = models.CharField(
        verbose_name='Автор',
        blank=True,
        max_length=200
    )
    phone_number = models.CharField(
        max_length=13,
        verbose_name='Номер телефона'
    )
    agency_name = models.CharField(
        max_length=200,
        verbose_name='Название агентства'
    )
    encumbrance = models.BooleanField(
        verbose_name='Обременение'
    )
    children = models.BooleanField(
        verbose_name='Дети в доле'
    )
    mortage = models.BooleanField(
        verbose_name='Ипотека'
    )

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'


class House(models.Model):
    street_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Название улицы'
    )
    area = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        verbose_name='Площадь дома'
    )
    description = models.TextField(
        max_length='1000',
        help_text='Описание',
        verbose_name='Описание дома'
    )
    price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name='Цена',
        blank=True
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    author = models.CharField(
        verbose_name='Автор',
        blank=True,
        max_length=200
    )
    phone_number = models.CharField(
        max_length=13,
        verbose_name='Номер телефона'
    )
    agency_name = models.CharField(
        max_length=200,
        verbose_name='Название агентства'
    )
    encumbrance = models.BooleanField(
        verbose_name='Обременение'
    )
    children = models.BooleanField(
        verbose_name='Дети в доле'
    )
    mortage = models.BooleanField(
        verbose_name='Ипотека'
    )
    microregion = models.CharField(
        max_length=200,
        verbose_name='Микрорайон'
    )
    gaz = models.CharField(
        max_length=200,
        verbose_name='Степень газификации'
    )
    water = models.CharField(
        max_length=200,
        verbose_name='Водоснабжение'
    )
    road = models.CharField(
        max_length=200,
        verbose_name='Подъезд к участку'
    )
    area_of_land = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        verbose_name='Площадь участка'
    )
    material = models.CharField(
        max_length=200,
        verbose_name='Материал изготовления'
    )
    finish = models.CharField(
        max_length=200,
        verbose_name='Степень завершённости'
    )
    purpose = models.CharField(
        max_length=200,
        verbose_name='Назначение участка'
    )
    sauna = models.CharField(
        max_length=200,
        verbose_name='Наличие бани'
    )
    garage = models.CharField(
        max_length=200,
        verbose_name='Наличие гаража'
    )
    fence = models.CharField(
        max_length=200,
        verbose_name='Ограждение'
    )

    class Meta:
        verbose_name = 'дом'
        verbose_name_plural = 'Дома'


class TownHouse(models.Model):
    street_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Название улицы'
    )
    area = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        verbose_name='Площадь дома'
    )
    description = models.TextField(
        max_length='1000',
        help_text='Описание',
        verbose_name='Описание дома'
    )
    price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name='Цена',
        blank=True
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    author = models.CharField(
        verbose_name='Автор',
        blank=True,
        max_length=200
    )
    phone_number = models.CharField(
        max_length=13,
        verbose_name='Номер телефона'
    )
    agency_name = models.CharField(
        max_length=200,
        verbose_name='Название агентства'
    )
    encumbrance = models.BooleanField(
        verbose_name='Обременение'
    )
    children = models.BooleanField(
        verbose_name='Дети в доле'
    )
    mortage = models.BooleanField(
        verbose_name='Ипотека'
    )
    microregion = models.CharField(
        max_length=200,
        verbose_name='Микрорайон'
    )
    gaz = models.CharField(
        max_length=200,
        verbose_name='Степень газификации'
    )
    water = models.CharField(
        max_length=200,
        verbose_name='Водоснабжение'
    )
    road = models.CharField(
        max_length=200,
        verbose_name='Подъезд к участку'
    )
    area_of_land = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        verbose_name='Площадь участка'
    )
    material = models.CharField(
        max_length=200,
        verbose_name='Материал изготовления'
    )
    finish = models.CharField(
        max_length=200,
        verbose_name='Степень завершённости'
    )
    purpose = models.CharField(
        max_length=200,
        verbose_name='Назначение участка'
    )
    sauna = models.CharField(
        max_length=200,
        verbose_name='Наличие бани'
    )
    garage = models.CharField(
        max_length=200,
        verbose_name='Наличие гаража'
    )
    fence = models.CharField(
        max_length=200,
        verbose_name='Ограждение'
    )

    class Meta:
        verbose_name = 'Таунхаус'
        verbose_name_plural = 'Таунхаусы'


class Land(models.Model):
    street_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Название улицы'
    )
    number_of_land = models.CharField(
        max_length=10,
        verbose_name='Номер дома'
    )
    description = models.TextField(
        max_length='1000',
        help_text='Описание',
        verbose_name='Описание'
    )
    price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name='Цена',
        blank=True
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    author = models.CharField(
        verbose_name='Автор',
        blank=True,
        max_length=200
    )
    phone_number = models.CharField(
        max_length=13,
        verbose_name='Номер телефона'
    )
    agency_name = models.CharField(
        max_length=200,
        verbose_name='Название агентства'
    )
    encumbrance = models.BooleanField(
        verbose_name='Обременение'
    )
    children = models.BooleanField(
        verbose_name='Дети в доле'
    )
    mortage = models.BooleanField(
        verbose_name='Ипотека'
    )
    microregion = models.CharField(
        max_length=200,
        verbose_name='Микрорайон'
    )
    gaz = models.CharField(
        max_length=200,
        verbose_name='Степень газификации'
    )
    water = models.CharField(
        max_length=200,
        verbose_name='Водоснабжение'
    )
    road = models.CharField(
        max_length=200,
        verbose_name='Подъезд к участку'
    )
    area_of_land = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        verbose_name='Площадь участка'
    )
    purpose = models.CharField(
        max_length=200,
        verbose_name='Назначение участка'
    )
    fence = models.CharField(
        max_length=200,
        verbose_name='Ограждение'
    )
    sauna = models.CharField(
        max_length=200,
        verbose_name='Наличие бани',
        default='Нет'
    )
    garage = models.CharField(
        max_length=200,
        verbose_name='Наличие гаража',
        default='Нет'
    )

    class Meta:
        verbose_name = 'Участок'
        verbose_name_plural = 'Участки'

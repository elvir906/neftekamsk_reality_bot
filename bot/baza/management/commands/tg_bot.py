import datetime as dt
import os
import logging

import psycopg2
from baza.about_text import about_text
from baza.models import Apartment, House, Land, Room, TownHouse
from baza.users import users
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.settings import DATABASES

DB_NAME = DATABASES.get('default').get('NAME')
POSTGRES_USER = DATABASES.get('default').get('USER')
POSTGRES_PASSWORD = DATABASES.get('default').get('PASSWORD')
DB_HOST = DATABASES.get('default').get('HOST')
DB_PORT = DATABASES.get('default').get('PORT')

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

bot = TeleBot(TELEGRAM_TOKEN)

logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    filemode='w',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

room_quantity = 0
street_name = ''
number_of_house = 0
floor = 0
number_of_floors = 0
area = 0
price = 0
description = ''
encumbrance = False
children = False
mortage = True

microregion = ''
gaz = ''
water = ''
road = ''
area_of_land = 0
material = ''
finish = ''
purpose = ''
sauna = ''
garage = ''
fence = ''

phone_number = ''
rieltor_name = ''
agency_name = ''

# objects_group = ''

db_connection = psycopg2.connect(
        database=DB_NAME,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


def apartment_description_result():
    if encumbrance is True:
        encumbrance_text = 'Есть'
    else:
        encumbrance_text = 'Нет'

    if children is True:
        children_text = 'Есть'
    else:
        children_text = 'Нет'

    if mortage is True:
        mortage_text = 'Можно'
    else:
        mortage_text = 'Нельзя'

    if reality == 'квартир':
        text = [
            '🥳 _Поздравляю! Вы только что внесли объект в базу_ ❤️💪🙌:',
            'Категория недвижимости: *Квартира*',
            f'*Количество комнат:* {room_quantity}',
            f'*Название улицы:* {street_name}',
            f'*Номер дома:* {number_of_house}',
            f'*Этаж:* {floor}/{number_of_floors}',
            f'*Площадь:* {area} кв.м.',
            f'*Краткое описание:* {description}',
            f'*Обременение:* {encumbrance_text}',
            f'*Дети в собственности:* {children_text}',
            f'*Оформить в ипотеку:* {mortage_text}',
            f'*Цена:* {price} ₽',
            f'*Имя риелтора:* {rieltor_name}',
            f'*Название агентства:* {agency_name}',
            f'*Контактный телефон:* {phone_number}',
            '',
            '❎ Изменить цену в случае необходимости можно через пункт меню. '
            + 'Если надо удалить объект или изменить другую информацию, пишите @davletelvir'
        ]
    if reality == 'комнат':
        text = [
            '🥳 _Поздравляю! Вы только что внесли объект в базу_ ❤️💪🙌:',
            'Категория недвижимости: *Комната*',
            f'*Название улицы:* {street_name}',
            f'*Номер дома:* {number_of_house}',
            f'*Этаж:* {floor}/{number_of_floors}',
            f'*Площадь:* {area} кв.м.',
            f'*Краткое описание:* {description}',
            f'*Обременение:* {encumbrance_text}',
            f'*Дети в собственности:* {children_text}',
            f'*Оформить в ипотеку:* {mortage_text}',
            f'*Цена:* {price} ₽',
            f'*Имя риелтора:* {rieltor_name}',
            f'*Название агентства:* {agency_name}',
            f'*Контактный телефон:* {phone_number}',
            '',
            '❎ Изменить цену в случае необходимости можно через пункт меню. '
            + 'Если надо удалить объект или изменить другую информацию, пишите @davletelvir'
        ]
    if reality == 'дом' or reality == 'таунхаус':
        text = [
            '🥳 _Поздравляю! Вы только что внесли объект в базу_ ❤️💪🙌:',
            f'Категория недвижимости: *{reality}*',
            f'*Микрорайон/село:* {microregion}',
            f'*Название улицы:* {street_name}',
            f'*Материал постройки:* {material}',
            f'*Площадь дома:* {area} кв.м.',
            f'*Площадь участка:* {area_of_land} сот.',
            f'*Назначение земли под домом:* {purpose}',
            f'*Степень завершённости строительства:* {finish}',
            f'*Степень газификации:* {gaz}',
            f'*Водоснабжение:* {water}',
            f'*Подъезд к дому:* {road}',
            f'*Наличие ограждения:* {fence}',
            f'*Наличие бани:* {sauna}',
            f'*Наличие гаража:* {garage}',
            f'*Краткое описание:* {description}',
            f'*Обременение:* {encumbrance_text}',
            f'*Дети в собственности:* {children_text}',
            f'*Оформить в ипотеку:* {mortage_text}',
            f'*Цена:* {price} ₽',
            f'*Имя риелтора:* {rieltor_name}',
            f'*Название агентства:* {agency_name}',
            f'*Контактный телефон:* {phone_number}',
            '',
            '❎ Изменить цену в случае необходимости можно через пункт меню. '
            + 'Если надо удалить объект или изменить другую информацию, пишите @davletelvir'
        ]
    if reality == 'участок':
        text = [
            '🥳 _Поздравляю! Вы только что внесли объект в базу_ ❤️💪🙌:',
            'Категория недвижимости: *Участок*',
            f'*Микрорайон/село:* {microregion}',
            f'*Назначение земли под домом:* {purpose}',
            f'*Название улицы:* {land_street_name}',
            f'*Номер участка:* {number_of_land}',
            f'*Площадь участка:* {area_of_land} сот.',
            f'*Степень газификации:* {gaz}',
            f'*Водоснабжение:* {water}',
            f'*Подъезд к дому:* {road}',
            f'*Наличие ограждения:* {fence}',
            f'*Краткое описание:* {description}',
            f'*Обременение:* {encumbrance_text}',
            f'*Дети в собственности:* {children_text}',
            f'*Оформить в ипотеку:* {mortage_text}',
            f'*Цена:* {price} ₽',
            f'*Имя риелтора:* {rieltor_name}',
            f'*Название агентства:* {agency_name}',
            f'*Контактный телефон:* {phone_number}',
            '',
            '❎ Изменить цену в случае необходимости можно через пункт меню. '
            + 'Если надо удалить объект или изменить другую информацию, пишите @davletelvir'
        ]
    return text


# @bot.message_handler(func=lambda message: message.chat.id not in users)
# def some(message):
#     bot.send_message(
#         message.chat.id,
#         'Чтобы пользоваться ботом, оплатите подписку: 390₽ за месяц пользования ботом.'
#         # + '\n1 месяц - 390₽,\n3 месяца - 1050₽,\n6 месяцев - 1990₽.'
#         + '\nНапишите разработчику @davletelvir и ждите ответа.'
#     )


@bot.message_handler(commands=['deleteobject'])
def delete_object(message):
    bot.send_message(
        message.chat.id,
        '❗ Внимание! Удаление объектов производится в ручном режиме '
        + 'разработчиками, да бы избежать несанкционированных удалений. Напишите @davletelvir в произвольной '
        + 'форме, что именно хотите удалить и его id - можно посмотреть в /myobjects. '
        + 'Например, так: "Здравствуйте, '
        + 'хочу удалить 2х, Ленина 7, id 45."'
    )


@bot.message_handler(commands=['myobjects'])
def enter_phone_number_my_objects(message):
    bot.send_message(
        message.chat.id,
        'Напишите свой номер телефона в формате 89ххххххххх'
    )
    bot.register_next_step_handler(message, get_phone_number_my_objects)


def get_phone_number_my_objects(message):
    apartment_queryset = Apartment.objects.filter(phone_number=message.text)
    room_queryset = Room.objects.filter(phone_number=message.text)
    house_queryset = House.objects.filter(phone_number=message.text)
    townhouse_queryset = TownHouse.objects.filter(phone_number=message.text)
    land_queryset = Land.objects.filter(phone_number=message.text)

    apartment_count = apartment_queryset.count()
    room_count = room_queryset.count()
    house_count = house_queryset.count()
    townhouse_count = townhouse_queryset.count()
    land_count = land_queryset.count()

    total_count = apartment_count + room_count + house_count + townhouse_count + land_count

    bot.send_message(
        message.chat.id,
        f'У вас *{total_count}* объекта (-ов):\n'
        + f'квартир - {apartment_count},\n'
        + f'комнат - {room_count},\n'
        + f'домов - {house_count},\n'
        + f'таунхаусов - {townhouse_count},\n'
        + f'участков - {land_count}',
        parse_mode="Markdown"
    )
    for item in apartment_queryset:
        bot.send_message(
            message.chat.id,
            f'id {item.pk}, *{item.room_quantity} к.кв.* '
            + f'{item.street_name} д.{item.number_of_house}, '
            + f'{item.floor} этаж - *{int(item.price)} ₽*'
        )

    for item in room_queryset:
        bot.send_message(
            message.chat.id,
            f'id {item.pk}, *комн.* {item.street_name} '
            + f'д.{item.number_of_house}, {item.floor} этаж - *{int(item.price)} ₽*'
        )

    for item in house_queryset:
        bot.send_message(
            message.chat.id,
            f'id {item.pk}, *Дом* {item.microregion}, {item.street_name} - *{int(item.price)} ₽*'
        )

    for item in townhouse_queryset:
        bot.send_message(
            message.chat.id,
            f'id {item.pk}, *Таунхаус* {item.microregion}, {item.street_name} - *{int(item.price)} ₽*'
        )

    for item in land_queryset:
        bot.send_message(
            message.chat.id,
            f'id {item.pk}, *Участок* {item.microregion}, {item.street_name} - {int(item.price)} ₽'
        )

    # if total_count <= 5:
    #     bot.send_message(
    #         message.chat.id,
    #         'Да... маловато будет 🙈. Надо ещё объектов наработать и в базу!\n'
    #         + 'Ведь чем больше объектов, тем больше зарабатывает риелтор!\n'
    #         + 'В агентстве "Регион" есть такой мастер Рауф 👴. Можешь у него спросить, как много объектов затащить 😅'
    #     )

    # if (total_count > 5) and (total_count <= 10):
    #     bot.send_message(
    #         message.chat.id,
    #         'Ну... как сказать... Нормально, но ещё бы объектов для работы.\n'
    #         + 'Ведь чем больше объектов, тем больше зарабатывает риелтор!\n'
    #         + 'Спорим, у тебя всё равно меньше объектов, чем у мастера Димы Граменицкого 👴 с "Проспекта"? 😅'
    #     )

    # if (total_count > 15):
    #     bot.send_message(
    #         message.chat.id,
    #         'Эй, полегче, ты  же не один риелтор в городе, оставь объектов и другим! 😅'
    #     )


@bot.message_handler(commands=['editprice'])
def enter_phone_number_edit_price(message):
    bot.send_message(
        message.chat.id,
        'Напишите свой номер телефона в формате 89ххххххххх'
    )
    bot.register_next_step_handler(message, get_phone_number_edit_price)


def get_phone_number_edit_price(message):
    global phone_number
    phone_number = message.text
    _keyboard = InlineKeyboardMarkup()
    buttons = ['1к.кв.', '2к.кв.', '3к.кв.', '4к.кв.', '5к.кв.', 'Комната', 'Дом', 'Таунхаус', 'Участок']

    for i in range(0, len(buttons)):
        _keyboard.add(
            InlineKeyboardButton(
                buttons[i], callback_data=f'edit_{buttons[i]}'
                )
        )
    bot.send_message(
        message.from_user.id,
        '🔻 Укажите к какой категории относится объект, цену которого вы желаете исправить',
        reply_markup=_keyboard
    )


def get_pk_edit_price(message):
    global pk
    if message.text == '/myobjects':
        bot.send_message(
            message.from_user.id,
            'Нажмите  /myobjects'
        )
    else:
        pk = message.text
        bot.send_message(
            message.from_user.id,
            '🔻 Введите новую цену. Просто полную цену цифрами, '
            + 'не сокращая, и без знаков Р, р, ₽, руб. и т.п. Если недвижимость '
            + 'стоит 3400000 рублей, значит так и пишите 3400000'
        )
        bot.register_next_step_handler(message, edit_price)


def edit_price(message):
    if objects_group == 'Apartment':
        try:
            queryset = Apartment.objects.get(pk=pk, phone_number=phone_number)
            queryset.price = int(message.text)
            queryset.save()
            bot.send_message(
                message.from_user.id,
                'Сделано!'
            )
        except (ValueError):
            bot.send_message(
                message.from_user.id,
                '🧐 Ошибка! Проверьте правильность ввода id и начните снова командой /editprice.'
            )
        except Exception as e:
            bot.send_message(
                message.from_user.id,
                '🧐 Ошибка! Проверьте правильность ввода id или '
                + 'номера телефона и начните снова командой /editprice.\n'
            )
            logging.error(f'{e}')

    if objects_group == 'Room':
        try:
            queryset = Room.objects.get(pk=pk, phone_number=phone_number)
            queryset.price = int(message.text)
            queryset.save()
            bot.send_message(
                message.from_user.id,
                'Сделано!'
            )
        except (ValueError):
            bot.send_message(
                message.from_user.id,
                '🧐 Ошибка! Проверьте правильность ввода id и начните снова командой /editprice.'
            )
        except Exception as e:
            bot.send_message(
                message.from_user.id,
                '🧐 Ошибка! Проверьте правильность ввода id или '
                + 'номера телефона и начните снова командой /editprice.\n'
            )
            logging.error(f'{e}')

    if objects_group == 'House':
        try:
            queryset = House.objects.get(pk=pk, phone_number=phone_number)
            queryset.price = int(message.text)
            queryset.save()
            bot.send_message(
                message.from_user.id,
                'Сделано!'
            )
        except (ValueError):
            bot.send_message(
                message.from_user.id,
                '🧐 Ошибка! Проверьте правильность ввода id и начните снова командой /editprice.'
            )
        except Exception as e:
            bot.send_message(
                message.from_user.id,
                '🧐 Ошибка! Проверьте правильность ввода id или номера '
                + 'телефона и начните снова командой /editprice.\n'
            )
            logging.error(f'{e}')

    if objects_group == 'TownHouse':
        try:
            queryset = TownHouse.objects.get(pk=pk, phone_number=phone_number)
            queryset.price = int(message.text)
            queryset.save()
            bot.send_message(
                message.from_user.id,
                'Сделано!'
            )
        except (ValueError):
            bot.send_message(
                message.from_user.id,
                '🧐 Ошибка! Проверьте правильность ввода id и начните снова командой /editprice.'
            )
        except Exception as e:
            bot.send_message(
                message.from_user.id,
                '🧐 Ошибка! Проверьте правильность ввода id или номера '
                + 'телефона и начните снова командой /editprice.\n'
            )
            logging.error(f'{e}')

    if objects_group == 'Land':
        try:
            queryset = Land.objects.get(pk=pk, phone_number=phone_number)
            queryset.price = int(message.text)
            queryset.save()
            bot.send_message(
                message.from_user.id,
                'Сделано!'
            )
        except (ValueError):
            bot.send_message(
                message.from_user.id,
                '🧐 Ошибка! Проверьте правильность ввода id и начните снова командой /editprice.'
            )
        except Exception as e:
            bot.send_message(
                message.from_user.id,
                '🧐 Ошибка! Проверьте правильность ввода id или номера '
                + 'телефона и начните снова командой /editprice.\n'
            )
            logging.error(f'{e}')


@bot.message_handler(commands=['getstatistics'])
def get_statistics(message):
    bot.send_message(message.from_user.id, 'Раздел на стадии разработки')


@bot.message_handler(commands=['about'])
def about(message):
    bot.send_message(message.from_user.id, '\n'.join(about_text), parse_mode="Markdown")


@bot.message_handler(commands=['searchobjects'])
def search_objects(message):

    mc_quantity = Room.objects.count()
    house_quantity = House.objects.count()
    townhouse_quantity = TownHouse.objects.count()
    land_quantity = Land.objects.count()
    apartment_quantity = Apartment.objects.count()

    category_keyboard = InlineKeyboardMarkup()
    buttons = ['Квартиры', 'Комнаты', 'Дома', 'Таунхаусы', 'Участки']
    quantity = [
        apartment_quantity,
        mc_quantity,
        house_quantity,
        townhouse_quantity,
        land_quantity
    ]

    for i in range(0, len(buttons)):
        category_keyboard.add(
            InlineKeyboardButton(
                buttons[i]+' ('+str(quantity[i])+')',
                callback_data=f'{buttons[i]}'
                )
        )

    bot.send_message(
        message.from_user.id,
        '🔻 Выберите категорию объектов для поиска',
        reply_markup=category_keyboard
    )


@bot.message_handler(commands=['addobject'])
def add_object(message):
    category_keyboard = InlineKeyboardMarkup()
    buttons = ['Квартиру', 'Комнату', 'Дом', 'Таунхаус', 'Участок']

    for i in range(0, len(buttons)):
        category_keyboard.add(
            InlineKeyboardButton(
                buttons[i], callback_data=f'{buttons[i]}'
                )
        )

    bot.send_message(
        message.from_user.id,
        '🔻 Что желаете добавить?', reply_markup=category_keyboard
    )


def get_street_name(message):
    global street_name
    street_name = message.text
    bot.send_message(
        message.from_user.id,
        '🔻 Введите номер дома в формате _5, 5А, 91 корп.3_',
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, get_number_of_house)


def get_land_street_name(message):
    global land_street_name
    land_street_name = message.text
    bot.send_message(
        message.from_user.id,
        '🔻 Введите номер участка в формате _5, 5А_',
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, get_number_of_land)


def get_number_of_land(message):
    global number_of_land
    number_of_land = message.text
    bot.send_message(
        message.from_user.id,
        '🔻 Введите площадь участка в сотках. Используйте '
        + 'разделитель "." (точку) для целой и десятичной части'
    )
    bot.register_next_step_handler(message, get_land_area)


def get_number_of_house(message):
    global number_of_house
    number_of_house = message.text

    """Генерация названий кнопок и коллбэк_дат. Количество кнопок = 18"""
    keyboard = InlineKeyboardMarkup()
    buttons_text = [str(i) for i in range(1, 19)]
    _callback_data = [str(i) + 'floor' for i in range(1, 19)]

    """Генерация кнопок 18 этажей, шесть в три ряда."""
    for j in range(0, 3):
        _button = [InlineKeyboardButton(text=buttons_text[i], callback_data=_callback_data[i]) for i in range(j * 6, 6 + 6 * j)]
        keyboard.row(*_button)

    bot.send_message(message.from_user.id, '🔻 Укажите этаж', reply_markup=keyboard)


def get_area(message):
    global area
    try:
        area = float(message.text)
        bot.send_message(
            message.from_user.id, '🔻 Напишите цену. Просто полную цену цифрами, '
            + 'не сокращая, и без знаков Р, р, ₽, руб. и т.п. Если недвижимость '
            + 'стоит 3400000 рублей, значит так и пишите 3400000'
        )
        bot.register_next_step_handler(message, get_price)
    except (ValueError) as e:
        bot.send_message(
            message.from_user.id, '🤔 Вы ошиблись при вводе значения площади. Площадь'
            + ' следует вводить цифрами и использовать разделитель "." для '
            + 'дробных значений. Так же НЕ указывайтье единицы измерения. '
            + ''
            + 'Попробуйте ввести значение заново /addobject'
        )
        logging.error(f'{e}')


def get_home_street_name(message):
    global street_name
    street_name = message.text
    bot.send_message(
        message.from_user.id,
        '🔻 Введите площадь дома в кв.м. '
        + 'Используйте разделитель "." (точку) для целой и десятичной части'
    )
    bot.register_next_step_handler(message, get_home_area)


def get_home_area(message):
    global area
    try:
        area = float(message.text)
        bot.send_message(
            message.from_user.id,
            '🔻 Введите площадь участка в сотках. Используйте разделитель '
            + '"." (точку) для целой и десятичной части'
        )
        bot.register_next_step_handler(message, get_land_area)
    except ValueError as e:
        bot.send_message(
            message.from_user.id, '🤔 Вы ошиблись при вводе значения площади. Площадь'
            + ' следует вводить цифрами и использовать разделитель "." для'
            + 'дробных значений. Так же НЕ указывайтье единицы измерения. '
            + ''
            + 'Попробуйте ввести значение заново /addobject'
        )
        logging.error(f'{e}')


def get_land_area(message):
    global area_of_land
    try:
        area_of_land = float(message.text)
        bot.send_message(
            message.from_user.id, '🔻 Напишите цену. Просто полную цену цифрами, '
            + 'не сокращая, и без знаков Р, р, ₽, руб. и т.п. Если недвижимость '
            + 'стоит 3400000 рублей, значит так и пишите 3400000'
        )
        bot.register_next_step_handler(message, get_price)
    except ValueError as e:
        bot.send_message(
            message.from_user.id, '🤔 Вы ошиблись при вводе значения площади. Площадь'
            + ' следует вводить цифрами и использовать разделитель "." для'
            + 'дробных значений. Так же НЕ указывайте единицы измерения. '
            + '' 
            + 'Попробуйте ввести значение заново /addobject'
        )
        logging.error(f'{e}')


def get_price(message):
    global price
    try:
        price = int(message.text)
        bot.send_message(
            message.from_user.id, '🔻 Добавьте небольшое описание.\n'
            + 'Для квартир: окна, двери и т.п.\n'
            + 'Для комнат: Вода в комнате, саунзел на сколько, письма готовы нет.\n'
            + 'Для участков - ровный или нет, есть ли гараж/баня или фундамент'
        )
        bot.register_next_step_handler(message, get_description)

    except ValueError as e:
        bot.send_message(
            message.from_user.id, '🤔 Вы ошиблись при вводе значения цены. Цену'
            + ' следует вводить цифрами без разделителя "." и без указания единицы измерения. '
            + '' 
            + 'Попробуйте ввести значение заново /addobject'
        )
        logging.error(f'{e}')


def get_description(message):
    global description
    description = message.text

    keyboard = InlineKeyboardMarkup()
    key_1 = InlineKeyboardButton(text='Да', callback_data='yes_encumbrance')
    key_2 = InlineKeyboardButton(text='Нет', callback_data='no_encumbrance')
    keyboard.row(key_1, key_2)
    if reality == 'дом' or reality == 'таунхаус' or reality == 'участок':
        bot.send_message(message.from_user.id, f'🔻 {reality} в обременении?', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, f'🔻 {reality}а в обременении?', reply_markup=keyboard)


def get_phone_number(message):
    global phone_number
    phone_number = message.text
    bot.send_message(message.from_user.id, '🔻 Напишите своё имя')
    bot.register_next_step_handler(message, get_rieltor_name)


def get_rieltor_name(message):
    global rieltor_name
    rieltor_name = message.text
    bot.send_message(
        message.from_user.id,
        '🔻 В каком агентстве вы трудитесь? Если вы частный риелтор, то напишите "Частный"'
    )
    bot.register_next_step_handler(message, get_agency_name)


def get_agency_name(message):
    global agency_name
    agency_name = message.text
    result_text = apartment_description_result()

    pub_date = dt.datetime.now()

    cursor = db_connection.cursor()
    if reality == 'квартир':
        try:
            data = (
                room_quantity, street_name, number_of_house, floor,
                number_of_floors, area, description, pub_date,
                rieltor_name, agency_name, children, encumbrance,
                mortage, phone_number, price
            )
            query = 'INSERT INTO baza_apartment (room_quantity, street_name, number_of_house, floor, number_of_floors, area, description, pub_date, author, agency, children, encumbrance, mortage, phone_number, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(query, data)
            db_connection.commit()

            bot.send_message(message.from_user.id, '\n'.join(result_text), parse_mode="Markdown")
        except Exception as e:
            bot.send_message(
                message.from_user.id,
                'Извините, в работе бота произошла ошибка. Попробуйте заново. '
                + 'Если ошибка повторится, напишите /davletelvir'
            )
            logging.error(f'{e}')
        finally:
            cursor.close()

    if reality == 'комнат':
        try:
            data = (
                street_name, number_of_house, floor, number_of_floors,
                area, description, pub_date, rieltor_name,
                agency_name, children, encumbrance,
                mortage, phone_number, price
            )
            query = 'INSERT INTO baza_room (street_name, number_of_house, floor, number_of_floors, area, description, pub_date, author, agency_name, children, encumbrance, mortage, phone_number, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(query, data)
            db_connection.commit()
            cursor.close()

            bot.send_message(message.from_user.id, '\n'.join(result_text), parse_mode="Markdown")

        except Exception as e:
            bot.send_message(
                message.from_user.id,
                'Извините, в работе бота произошла ошибка. Попробуйте заново. '
                + 'Если ошибка повторится, напишите /davletelvir'
            )
            logging.error(f'{e}')
        finally:
            cursor.close()

    if reality == 'дом':
        try:
            data = (
                street_name,
                area, description, price, pub_date, rieltor_name,
                phone_number, agency_name, children, encumbrance,
                mortage, microregion, gaz, water, road, area_of_land,
                material, finish, purpose, sauna, garage, fence
            )
            query = 'INSERT INTO baza_house (street_name, area, description, price, pub_date, author, phone_number, agency_name, children, encumbrance, mortage, microregion, gaz, water, road, area_of_land, material, finish, purpose, sauna, garage, fence) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(query, data)
            db_connection.commit()
            cursor.close()

            bot.send_message(message.from_user.id, '\n'.join(result_text), parse_mode="Markdown")

        except Exception as e:
            bot.send_message(
                message.from_user.id,
                'Извините, в работе бота произошла ошибка. Попробуйте заново. '
                + 'Если ошибка повторится, напишите /davletelvir'
            )
            logging.error(f'{e}')
        finally:
            cursor.close()

    if reality == 'таунхаус':
        try:
            data = (
                street_name,
                area, description, price, pub_date, rieltor_name,
                phone_number, agency_name, children, encumbrance,
                mortage, microregion, gaz, water, road, area_of_land,
                material, finish, purpose, sauna, garage, fence
            )
            query = 'INSERT INTO baza_townhouse (street_name, area, description, price, pub_date, author, phone_number, agency_name, children, encumbrance, mortage, microregion, gaz, water, road, area_of_land, material, finish, purpose, sauna, garage, fence) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(query, data)
            db_connection.commit()
            cursor.close()

            bot.send_message(message.from_user.id, '\n'.join(result_text), parse_mode="Markdown")

        except Exception as e:
            bot.send_message(
                message.from_user.id,
                'Извините, в работе бота произошла ошибка. '
                + ''
                + 'Попробуйте заново. Если ошибка повторится, напишите /davletelvir'
            )
            logging.error(f'{e}')
        finally:
            cursor.close()

    if reality == 'участок':
        try:
            data = (
                land_street_name, number_of_land,
                description, price, pub_date, rieltor_name,
                phone_number, agency_name, children, encumbrance,
                mortage, microregion, gaz, water, road, area_of_land,
                purpose, fence
            )
            query = 'INSERT INTO baza_land (street_name, number_of_land, description, price, pub_date, author, phone_number, agency_name, children, encumbrance, mortage, microregion, gaz, water, road, area_of_land, purpose, fence) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(query, data)
            db_connection.commit()
            cursor.close()

            bot.send_message(message.from_user.id, '\n'.join(result_text), parse_mode="Markdown")

        except Exception as e:
            bot.send_message(
                message.from_user.id,
                'Извините, в работе бота произошла ошибка. '
                + ''
                + 'Попробуйте заново. Если ошибка повторится, напишите /davletelvir'
            )
            logging.error(f'{e}')
        finally:
            cursor.close()


@bot.callback_query_handler(func=lambda callback: callback.data)
def callback_worker(callback):

    one_room_quantity = Apartment.objects.filter(room_quantity=1).count()
    two_room_quantity = Apartment.objects.filter(room_quantity=2).count()
    three_room_quantity = Apartment.objects.filter(room_quantity=3).count()
    four_room_quantity = Apartment.objects.filter(room_quantity=4).count()
    five_room_quantity = Apartment.objects.filter(room_quantity=5).count()

    apartament_keyboard = InlineKeyboardMarkup()
    if callback.data == 'Квартиры':
        buttons = ['1-комнатные', '2-комнатные', '3-комнатные', '4-комнатные', '5-комнатные', '⏪ Назад']
        quantity = [one_room_quantity, two_room_quantity, three_room_quantity, four_room_quantity, five_room_quantity]

        for i in range(0, len(buttons)-1):
            apartament_keyboard.add(InlineKeyboardButton(buttons[i]+' ('+str(quantity[i])+')', callback_data=f'{buttons[i]}'))
        apartament_keyboard.add(InlineKeyboardButton(buttons[len(buttons)-1], callback_data=f'{buttons[len(buttons)-1]}'))

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text='🔻 Выберите по количеству комнат',
            reply_markup=apartament_keyboard
        )

    elif callback.data == 'Комнаты':
        query_set = Room.objects.order_by('-pub_date')

        bot.send_message(
            callback.from_user.id, '✳ Вот, что я нашёл по *комнатам*:', parse_mode="Markdown"
        )
        for item in query_set:
            if item.children is True:
                ch_text = 'Есть'
            else:
                ch_text = 'Нет'

            if item.mortage is True:
                mor_text = 'Есть'
            else:
                mor_text = 'Нет'

            if item.encumbrance is True:
                enc_text = 'Есть'
            else:
                enc_text = 'Нет'

            bot.send_message(
                callback.from_user.id,
                f'🔸 _Комната {item.street_name} д.{item.number_of_house}_'
                + f'\n*Этаж:* {item.floor}/{item.number_of_floors}'
                + f'\n*Площадь комнаты:* {item.area} кв.м.'
                + f'\n*Описание:* {item.description} '
                + f'\n*Обременение:* {enc_text} '
                + f'\n*Несовершеннолетние в собственности:* {ch_text}'
                + f'\n*Возможность приобрести в ипотеку:* {mor_text}'
                + f'\n*Цена:* {int(item.price)} ₽'
                + f'\n*Агентство:* {item.agency_name}'
                + f'\n*Имя риелтора:* {item.author}'
                + f'\n*Номер телефона:* {item.phone_number}'
                + f'\n*Дата публикации:* {item.pub_date.date()}',
                parse_mode="Markdown"
            )

    elif callback.data == 'Дома':
        query_set = House.objects.order_by('-pub_date')

        bot.send_message(
            callback.from_user.id, '✳ Вот, что я нашёл по *домам*:', parse_mode="Markdown"
        )
        for item in query_set:
            if item.children is True:
                ch_text = 'Есть'
            else:
                ch_text = 'Нет'

            if item.mortage is True:
                mor_text = 'Есть'
            else:
                mor_text = 'Нет'

            if item.encumbrance is True:
                enc_text = 'Есть'
            else:
                enc_text = 'Нет'

            bot.send_message(
                callback.from_user.id,
                f'🔸 _Дом {item.microregion}, {item.street_name}_'
                + f'\n*Площадь дома:* {item.area} кв.м.'
                + f'\n*Площадь участка:* {item.area_of_land} сот.'
                + f'\n*Назначение участка:* {item.purpose}'
                + f'\n*Материал стен:* {item.material}'
                + f'\n*Степень завершённости:* {item.finish}'
                + f'\n*Степень газификации:* {item.gaz}'
                + f'\n*Вода:* {item.water}'
                + f'\n*Подъезд к участку:* {item.road}'
                + f'\n*Наличие бани/сауны:* {item.sauna}'
                + f'\n*Наличие гаража:* {item.garage}'
                + f'\n*Наличие ограждения:* {item.fence}'
                + f'\n*Описание:* {item.description}'
                + f'\n*Обременение:* {enc_text}'
                + f'\n*Дети в собственности:* {ch_text}'
                + f'\n*Возможность приобрести в ипотеку:* {mor_text}'
                + f'\n*Цена:* {int(item.price)} ₽'
                + f'\n*Агентство:* {item.agency_name}'
                + f'\n*Имя риелтора:* {item.author}'
                + f'\n*Номер телефона:* {item.phone_number}'
                + f'\n*Дата публикации:* {item.pub_date.date()}',
                parse_mode="Markdown"
            )

    elif callback.data == 'Таунхаусы':
        query_set = TownHouse.objects.order_by('-pub_date')

        bot.send_message(
            callback.from_user.id, '✳ Вот, что я нашёл по *таунхаусам*:', parse_mode="Markdown"
        )
        for item in query_set:
            if item.children is True:
                ch_text = 'Есть'
            else:
                ch_text = 'Нет'

            if item.mortage is True:
                mor_text = 'Есть'
            else:
                mor_text = 'Нет'

            if item.encumbrance is True:
                enc_text = 'Есть'
            else:
                enc_text = 'Нет'

            bot.send_message(
                callback.from_user.id,
                f'🔸 _Таунхаус {item.microregion}, {item.street_name}_'
                + f'\n*Площадь дома:* {item.area} кв.м.'
                + f'\n*Площадь участка:* {item.area_of_land} сот.'
                + f'\n*Назначение участка:* {item.purpose}'
                + f'\n*Материал стен:* {item.material}'
                + f'\n*Степень завершённости:* {item.finish}'
                + f'\n*Степень газификации:* {item.gaz}'
                + f'\n*Вода:* {item.water}'
                + f'\n*Подъезд к участку:* {item.road}'
                + f'\n*Наличие бани/сауны:* {item.sauna}'
                + f'\n*Наличие гаража:* {item.garage}'
                + f'\n*Наличие ограждения:* {item.fence}'
                + f'\n*Описание:* {item.description}'
                + f'\n*Обременение:* {enc_text}'
                + f'\n*Дети в собственности:* {ch_text}'
                + f'\n*Возможность приобрести в ипотеку:* {mor_text}'
                + f'\n*Цена:* {int(item.price)} ₽'
                + f'\n*Агентство:* {item.agency_name}'
                + f'\n*Имя риелтора:* {item.author}'
                + f'\n*Номер телефона:* {item.phone_number}'
                f'\n*Дата публикации:* {item.pub_date.date()}',
                parse_mode="Markdown"
            )

    elif callback.data == 'Участки':
        query_set = Land.objects.order_by('-pub_date')

        bot.send_message(
            callback.from_user.id, '✳ Вот, что я нашёл по *участкам*:', parse_mode="Markdown"
        )
        for item in query_set:
            if item.children is True:
                ch_text = 'Есть'
            else:
                ch_text = 'Нет'

            if item.mortage is True:
                mor_text = 'Есть'
            else:
                mor_text = 'Нет'

            if item.encumbrance is True:
                enc_text = 'Есть'
            else:
                enc_text = 'Нет'

            bot.send_message(
                callback.from_user.id,
                f'🔸 _Участок {item.microregion}, {item.street_name} уч.{item.number_of_land} _'
                + f'\n*Площадь участка:* {item.area_of_land} сот.'
                + f'\n*Назначение участка:* {item.purpose}'
                + f'\n*Степень газификации:* {item.gaz}'
                + f'\n*Вода:* {item.water}'
                + f'\n*Подъезд к участку:* {item.road}'
                + f'\n*Наличие ограждения:* {item.fence}'
                + f'\n*Описание:* {item.description}'
                + f'\n*Обременение:* {enc_text}'
                + f'\n*Дети в собственности:* {ch_text}'
                + f'\n*Возможность приобрести в ипотеку:* {mor_text}'
                + f'\n*Цена:* {int(item.price)} ₽'
                + f'\n*Агентство:* {item.agency_name}'
                + f'\n*Имя риелтора:* {item.author}'
                + f'\n*Номер телефона:* {item.phone_number}'
                + f'\n*Дата публикации:* {item.pub_date.date()}',
                parse_mode="Markdown"
            )

    elif callback.data == '1-комнатные':
        query = Apartment.objects.filter(room_quantity=1).order_by('-pub_date')

        bot.send_message(
            callback.from_user.id, '✳ Вот, что я нашёл по *1-комнатным* квартирам:', parse_mode="Markdown"
        )
        for item in query:
            if item.children is True:
                ch_text = 'Есть'
            else:
                ch_text = 'Нет'

            if item.mortage is True:
                mor_text = 'Есть'
            else:
                mor_text = 'Нет'

            if item.encumbrance is True:
                enc_text = 'Есть'
            else:
                enc_text = 'Нет'

            bot.send_message(
                callback.from_user.id,
                f'🔸 _1к.кв. {item.street_name} д.{item.number_of_house}_'
                + f'\n*Этаж:* {item.floor}/{item.number_of_floors} '
                + f'\n*Площадь квартиры:* {item.area} кв.м.'
                + f'\n*Описание:* {item.description}'
                + f'\n*Обременение:* {enc_text}'
                + f'\n*Дети в собственности:* {ch_text}'
                + f'\n*Возможность приобрести в ипотеку:* {mor_text}'
                + f'\n*Цена:* {int(item.price)} ₽'
                + f'\n*Агентство:* {item.agency}'
                + f'\n*Имя риелтора:* {item.author}'
                + f'\n*Номер телефона:* {item.phone_number}'
                + f'\n*Дата публикации:* {item.pub_date.date()}',
                parse_mode="Markdown"
            )

    elif callback.data == '2-комнатные':
        query = Apartment.objects.filter(room_quantity=2).order_by('-pub_date')

        bot.send_message(
            callback.from_user.id, '✳ Вот, что я нашёл по *2-комнатным* квартирам:', parse_mode="Markdown"
        )
        for item in query:
            if item.children is True:
                ch_text = 'Есть'
            else:
                ch_text = 'Нет'

            if item.mortage is True:
                mor_text = 'Есть'
            else:
                mor_text = 'Нет'

            if item.encumbrance is True:
                enc_text = 'Есть'
            else:
                enc_text = 'Нет'

            bot.send_message(
                callback.from_user.id,
                f'🔸 _2к.кв. {item.street_name} д.{item.number_of_house}_'
                + f'\n*Этаж:* {item.floor}/{item.number_of_floors}'
                + f'\n*Площадь квартиры:* {item.area} кв.м.'
                + f'\n*Описание:* {item.description},'
                + f'\n*Обременение:* {enc_text}'
                + f'\n*Дети в собственности:* {ch_text}'
                + f'\n*Возможность приобрести в ипотеку:* {mor_text}'
                + f'\n*Цена:* {int(item.price)} ₽'
                + f'\n*Агентство:* {item.agency} '
                + f'\n*Имя риелтора:* {item.author}'
                + f'\n*Номер телефона:* {item.phone_number}'
                + f'\n*Дата публикации:* {item.pub_date.date()}',
                parse_mode="Markdown"
            )

    elif callback.data == '3-комнатные':
        query = Apartment.objects.filter(room_quantity=3).order_by('-pub_date')

        bot.send_message(
            callback.from_user.id, '✳ Вот, что я нашёл по *3-комнатным* квартирам:', parse_mode="Markdown"
        )
        for item in query:
            if item.children is True:
                ch_text = 'Есть'
            else:
                ch_text = 'Нет'

            if item.mortage is True:
                mor_text = 'Есть'
            else:
                mor_text = 'Нет'

            if item.encumbrance is True:
                enc_text = 'Есть'
            else:
                enc_text = 'Нет'

            bot.send_message(
                callback.from_user.id,
                f'🔸 _3к.кв. {item.street_name} д.{item.number_of_house}_'
                + f'\n*Этаж:* {item.floor}/{item.number_of_floors} '
                + f'\n*Площадь квартиры:* {item.area} кв.м.'
                + f'\n*Описание:* {item.description}, '
                + f'\n*Обременение:* {enc_text} '
                + f'\n*Дети в собственности:* {ch_text} '
                + f'\n*Возможность приобрести в ипотеку:* {mor_text} '
                + f'\n*Цена:* {int(item.price)} ₽'
                + f'\n*Агентство:* {item.agency} '
                + f'\n*Имя риелтора:* {item.author}'
                + f'\n*Номер телефона:* {item.phone_number}'
                + f'\n*Дата публикации:* {item.pub_date.date()}',
                parse_mode="Markdown"
            )

    elif callback.data == '4-комнатные':
        query = Apartment.objects.filter(room_quantity=4).order_by('-pub_date')

        bot.send_message(
            callback.from_user.id, '✳ Вот, что я нашёл по *4-комнатным* квартирам:', parse_mode="Markdown"
        )
        for item in query:
            if item.children is True:
                ch_text = 'Есть'
            else:
                ch_text = 'Нет'

            if item.mortage is True:
                mor_text = 'Есть'
            else:
                mor_text = 'Нет'

            if item.encumbrance is True:
                enc_text = 'Есть'
            else:
                enc_text = 'Нет'

            bot.send_message(
                callback.from_user.id,
                f'🔸 _4к.кв. {item.street_name} д.{item.number_of_house}_'
                + f'\n*Этаж:* {item.floor}/{item.number_of_floors}'
                + f'\n*Площадь квартиры:* {item.area} кв.м.'
                + f'\n*Описание:* {item.description}, '
                + f'\n*Обременение:* {enc_text}'
                + f'\n*Дети в собственности:* {ch_text}'
                + f'\n*Возможность приобрести в ипотеку:* {mor_text}'
                + f'\n*Цена:* {int(item.price)} ₽'
                + f'\n*Агентство:* {item.agency}'
                + f'\n*Имя риелтора:* {item.author}'
                + f'\n*Номер телефона:* {item.phone_number}'
                + f'\n*Дата публикации:* {item.pub_date.date()}',
                parse_mode="Markdown"
            )

    elif callback.data == '5-комнатные':
        query = Apartment.objects.filter(room_quantity=5).order_by('-pub_date')

        bot.send_message(
            callback.from_user.id, '✳ Вот, что я нашёл по *5-комнатным* квартирам:', parse_mode="Markdown"
        )
        for item in query:
            if item.children is True:
                ch_text = 'Есть'
            else:
                ch_text = 'Нет'

            if item.mortage is True:
                mor_text = 'Есть'
            else:
                mor_text = 'Нет'

            if item.encumbrance is True:
                enc_text = 'Есть'
            else:
                enc_text = 'Нет'

            bot.send_message(
                callback.from_user.id,
                f'🔸_5к.кв. {item.street_name} д.{item.number_of_house}_'
                + f'\n*Этаж:* {item.floor}/{item.number_of_floors} '
                + f'\n*Площадь квартиры:* {item.area} кв.м.'
                + f'\n*Описание:* {item.description},'
                + f'\n*Обременение:* {enc_text}'
                + f'\n*Дети в собственности:* {ch_text} '
                + f'\n*Возможность приобрести в ипотеку:* {mor_text} '
                + f'\n*Цена:* {int(item.price)} ₽'
                + f'\n*Агентство:* {item.agency}'
                + f'\n*Имя риелтора:* {item.author}'
                + f'\n*Номер телефона:* {item.phone_number}'
                + f'\n*Дата публикации:* {item.pub_date.date()}',
                parse_mode="Markdown"
            )

    elif callback.data == '⏪ Назад':

        mc_quantity = Room.objects.count()
        house_quantity = House.objects.count()
        townhouse_quantity = TownHouse.objects.count()
        land_quantity = Land.objects.count()
        apartment_quantity = Apartment.objects.count()

        category_keyboard = InlineKeyboardMarkup()
        buttons = ['Квартиры', 'Комнаты', 'Дома', 'Таунхаусы', 'Участки']
        quantity = [apartment_quantity, mc_quantity, house_quantity, townhouse_quantity, land_quantity]

        for i in range(0, len(buttons)):
            category_keyboard.add(InlineKeyboardButton(buttons[i]+' ('+str(quantity[i])+')', callback_data=f'{buttons[i]}'))

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text='🔻 Выберите категорию объектов для поиска',
            reply_markup=category_keyboard
        )

    elif callback.data == 'Квартиру':
        keyboard = InlineKeyboardMarkup()
        """Генерация кнопок с указанием этажей 1-5"""
        _buttons = [InlineKeyboardButton(text=str(i), callback_data=str(i) + 'r') for i in range(1, 6)]
        keyboard.row(*_buttons)

        bot.send_message(
            callback.from_user.id,
            'Приготовьтесь ответить на 14 вопросов про ваш объект '
            + 'недвижимости. Отвечайте вдумчиво и внимательно.'
            + '😏 Это займёт не более 2-3х минут.'
            + '\n🔻 Укажите количество комнат',
            reply_markup=keyboard
        )

    elif callback.data in ['1r', '2r', '3r', '4r', '5r'] or callback.data == 'Комнату':
        if callback.data == 'Комнату':
            global reality
            reality = 'комнат'
            bot.send_message(
                callback.from_user.id,
                'Приготовьтесь ответить на 13 вопросов про ваш объект '
                + 'недвижимости. Отвечайте вдумчиво и внимательно.'
                + '😏 Это займёт не более 2-3х минут.'
            )

        else:
            reality = 'квартир'
            global room_quantity
            room_quantity = int(callback.data[0])
        bot.send_message(callback.from_user.id, '🔻 Введите назавание улицы c заглавной буквы')
        bot.register_next_step_handler(callback.message, get_street_name)

    elif callback.data in ['Дом', 'Таунхаус', 'Участок']:
        questions = 0
        if callback.data == 'Дом':
            reality = 'дом'
            questions = 21
        elif callback.data == 'Таунхаус':
            questions = 21
            reality = 'таунхаус'
        else:
            reality = 'участок'
            questions = 19

        keyboard = InlineKeyboardMarkup()

        microregion_buttons_text = [
            'Касёво', 'Восточный 1,2,3,4,5', 'Ротково',
            'Марино', 'Телевышка', 'Лесная поляна',
            'Михайловка', 'Ташкиново', 'Николо-Берёзовка',
            'Кутлинка', 'Новонагаево', 'Актанышбаш',
            'Амзя', 'Карманово', 'Можары', 'Арлан'
        ]

        _buttons = [
            InlineKeyboardButton(
                text=microregion_buttons_text[i],
                callback_data=microregion_buttons_text[i]
                ) for i in range(0, len(microregion_buttons_text) - 1)
        ]

        keyboard.row(_buttons[0], _buttons[2])
        keyboard.row(_buttons[7], _buttons[5])
        keyboard.row(_buttons[3], _buttons[4], _buttons[6])
        keyboard.row(_buttons[8], _buttons[1])
        keyboard.row(_buttons[9], _buttons[10], _buttons[11])
        keyboard.row(_buttons[12], _buttons[13], _buttons[14])

        bot.send_message(
            callback.from_user.id,
            f'Приготовьтесь ответить на {questions} вопрос про ваш объект'
            + 'недвижимости. Читайте внимательно, отвечайте вдумчиво.'
            + '😏 Это займёт не более 2-3х минут.'
            + '\n🔻 Укажите район расположения дома',
            reply_markup=keyboard
        )

    elif callback.data in [
            'Касёво', 'Восточный 1,2,3,4,5', 'Ротково',
            'Марино', 'Телевышка', 'Лесная поляна',
            'Михайловка', 'Ташкиново', 'Николо-Берёзовка',
            'Кутлинка', 'Новонагаево', 'Актанышбаш',
            'Амзя', 'Карманово', 'Можары', 'Арлан'
    ]:
        global microregion
        microregion = callback.data
        keyboard = InlineKeyboardMarkup()
        key_1 = InlineKeyboardButton(text='ИЖС', callback_data='ИЖС')
        key_2 = InlineKeyboardButton(text='СНТ, ДНТ', callback_data='СНТ, ДНТ')
        key_3 = InlineKeyboardButton(text='ЛПХ', callback_data='ЛПХ')

        keyboard.row(key_1, key_2, key_3)

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text='🔻 Укажите назначение участка',
            reply_markup=keyboard
        )

    elif (callback.data in ['ИЖС', 'СНТ, ДНТ', 'ЛПХ']) and (reality in ['дом', 'таунхаус']):
        global purpose
        purpose = callback.data
        keyboard = InlineKeyboardMarkup()
        key_1 = InlineKeyboardButton(text='Да', callback_data='Завершённое строительство')
        key_2 = InlineKeyboardButton(text='Нет', callback_data='Незавершённое строительство')

        keyboard.row(key_1, key_2)

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text='🔻 Это завершённое строительство?',
            reply_markup=keyboard
        )

    elif callback.data in ['ИЖС', 'СНТ, ДНТ', 'ЛПХ'] and (reality == 'участок'):
        purpose = callback.data
        keyboard = InlineKeyboardMarkup()
        key_1 = InlineKeyboardButton(text='Да', callback_data='По улице проходит газ')
        key_2 = InlineKeyboardButton(text='Нет', callback_data='По улице НЕ проходит газ')

        keyboard.row(key_1, key_2)

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text='🔻 Газ проходит по улице?',
            reply_markup=keyboard
        )

    elif callback.data in ['Завершённое строительство', 'Незавершённое строительство']:
        global finish
        finish = callback.data
        keyboard = InlineKeyboardMarkup()
        key_1 = InlineKeyboardButton(text='Газифицирован, дом отапливается', callback_data='Газифицирован, дом отапливается')
        key_3 = InlineKeyboardButton(text='Улица газифицировна, дом - нет', callback_data='Улица газифицировна, дом - нет')
        key_4 = InlineKeyboardButton(text='Улица не газифицирована', callback_data='Улица не газифицирована')

        keyboard.row(key_1)
        keyboard.row(key_3)
        keyboard.row(key_4)

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text='🔻 Укажите степень газификации дома',
            reply_markup=keyboard
        )

    elif callback.data in ['По улице проходит газ', 'По улице НЕ проходит газ']:
        global gaz
        gaz = callback.data
        keyboard = InlineKeyboardMarkup()
        key_1 = InlineKeyboardButton(text='Да', callback_data='По улице проходит водопровод')
        key_2 = InlineKeyboardButton(text='Нет', callback_data='По улице водопровод НЕ проходит')

        keyboard.row(key_1, key_2)

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text='🔻 Водопровод проходит по улице?',
            reply_markup=keyboard
        )

    elif callback.data in [
        'Газифицирован, дом отапливается',
        'Улица газифицировна, дом - нет',
        'Улица не газифицирована',
    ]:
        gaz = callback.data
        keyboard = InlineKeyboardMarkup()
        material_buttons_text = [
            'Кирпич',
            'Заливной',
            'Блок, облицованный кирпичом',
            'Дерево',
            'Дерево, облицованное кирпичом',
            'Другое'
        ]
        _buttons = [
            InlineKeyboardButton(
                text=material_buttons_text[i], callback_data=material_buttons_text[i]
                ) for i in range(0, len(material_buttons_text) - 1)
        ]

        for i in range(0, len(_buttons)):
            keyboard.row(_buttons[i])

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text='🔻 Укажите материал стен',
            reply_markup=keyboard
        )

    elif callback.data in [
            'Кирпич',
            'Заливной',
            'Блок, облицованный кирпичом',
            'Дерево',
            'Дерево, облицованное кирпичом',
            'Другое'
    ]:
        global material
        material = callback.data
        keyboard = InlineKeyboardMarkup()
        key_1 = InlineKeyboardButton(text='Да, центральное водоснабжение', callback_data='Водоснабжение центральное')
        key_2 = InlineKeyboardButton(text='На участке есть колодец', callback_data='Колодец')
        key_3 = InlineKeyboardButton(text='Вода проходит по улице, в дом - нет', callback_data='Вода есть, её надо подводить')
        key_4 = InlineKeyboardButton(text='Воды нет', callback_data='Воды нет')

        keyboard.row(key_1)
        keyboard.row(key_2)
        keyboard.row(key_3)
        keyboard.row(key_4)

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text='🔻 В доме есть вода?',
            reply_markup=keyboard
        )

    elif callback.data in [
        'Водоснабжение центральное',
        'Колодец',
        'Вода есть, её надо подводить',
        'Воды нет'
    ]:
        global water
        water = callback.data
        keyboard = InlineKeyboardMarkup()
        key_1 = InlineKeyboardButton(text='Да', callback_data='Есть баня')
        key_2 = InlineKeyboardButton(text='Нет', callback_data='Бани нет')

        keyboard.row(key_1)
        keyboard.row(key_2)

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text='🔻 На териитории участка есть баня?',
            reply_markup=keyboard
        )

    elif callback.data in [
        'Есть баня',
        'Бани нет'
    ]:
        global sauna
        sauna = callback.data
        keyboard = InlineKeyboardMarkup()
        key_1 = InlineKeyboardButton(text='Да', callback_data='Есть гараж')
        key_2 = InlineKeyboardButton(text='Нет', callback_data='Гаража нет')

        keyboard.row(key_1)
        keyboard.row(key_2)

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text='🔻 На териитории участка есть гараж?',
            reply_markup=keyboard
        )

    elif callback.data in [
        'Есть гараж',
        'Гаража нет',
        'По улице проходит водопровод',
        'По улице водопровод НЕ проходит'
    ]:
        global garage
        garage = callback.data

        if reality == 'участок':
            water = callback.data

        keyboard = InlineKeyboardMarkup()
        key_1 = InlineKeyboardButton(text='Да', callback_data='Участок огорожен')
        key_2 = InlineKeyboardButton(text='Нет', callback_data='Участок не огорожен')

        keyboard.row(key_1)
        keyboard.row(key_2)

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text='🔻 Участок огорожен?',
            reply_markup=keyboard
        )

    elif callback.data in [
        'Участок огорожен',
        'Участок не огорожен'
    ]:
        global fence
        fence = callback.data
        keyboard = InlineKeyboardMarkup()
        key_1 = InlineKeyboardButton(text='Да, асфальт', callback_data='Асфальт')
        key_2 = InlineKeyboardButton(text='Да, неплохая насыпная дорога', callback_data='Неплохая насыпная дорога')
        key_3 = InlineKeyboardButton(text='Да, неплохая грунтовая дорога', callback_data='Неплохая грунтовая дорога')
        key_4 = InlineKeyboardButton(text='Движение к дому затруднено', callback_data='Бездорожье, затрудняющее проезд')

        keyboard.row(key_1)
        keyboard.row(key_2)
        keyboard.row(key_3)
        keyboard.row(key_4)

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text='🔻 К участку есть проезд?',
            reply_markup=keyboard
        )

    elif callback.data in [
        'Асфальт',
        'Неплохая насыпная дорога',
        'Неплохая грунтовая дорога',
        'Бездорожье, затрудняющее проезд'
    ]:
        global road
        road = callback.data

        if reality == 'участок':
            bot.send_message(
                callback.from_user.id,
                '🔻 Напишите название улицы c заглавной буквы'
            )
            bot.register_next_step_handler(callback.message, get_land_street_name)
        else:
            bot.send_message(
                callback.from_user.id,
                '🔻 При желании, напишите название улицы c заглавной буквы. Иначе - напишите цифру "0")'
            )
            bot.register_next_step_handler(callback.message, get_home_street_name)

    elif callback.data in [
        '1floor', '2floor', '3floor',
        '4floor', '5floor', '6floor',
        '7floor', '8floor', '9floor',
    ]:
        global floor
        floor = int(callback.data[0])

        keyboard = InlineKeyboardMarkup()
        buttons_text = [str(i) for i in range(1, 19)]
        _callback_data = [str(i) + 'floors' for i in range(1, 19)]

        for j in range(0, 3):
            _button = [InlineKeyboardButton(text=buttons_text[i], callback_data=_callback_data[i]) for i in range(j * 6, 6 + 6 * j)]
            keyboard.row(*_button)

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text='🔻 Укажите этажность дома',
            reply_markup=keyboard
        )

    elif callback.data in [
        '10floor', '11floor', '12floor',
        '13floor', '14floor', '15floor',
        '16floor', '17floor', '18floor',
    ]:
        floor = int(callback.data[0] + callback.data[1])

        keyboard = InlineKeyboardMarkup()
        buttons_text = [str(i) for i in range(1, 19)]
        _callback_data = [str(i) + 'floors' for i in range(1, 19)]

        for j in range(0, 3):
            _button = [InlineKeyboardButton(text=buttons_text[i], callback_data=_callback_data[i]) for i in range(j * 6, 6 + 6 * j)]
            keyboard.row(*_button)

        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text='🔻 Укажите этажность дома',
            reply_markup=keyboard
        )

    elif callback.data in [
        '1floors', '2floors', '3floors',
        '4floors', '5floors', '6floors',
        '7floors', '8floors', '9floors',
    ]:
        global number_of_floors
        number_of_floors = int(callback.data[0])

        bot.send_message(
            callback.from_user.id,
            f'🔻 Введите площадь {reality}. Используйте разделитель "." (точку) для целой и десятичной части'
        )
        bot.register_next_step_handler(callback.message, get_area)

    elif callback.data in [
        '11floors', '12floors', '13floors',
        '14floors', '15floors', '16floors',
        '17floors', '18floors', '10floors',
    ]:
        number_of_floors = int(callback.data[0] + callback.data[1])

        bot.send_message(
            callback.from_user.id,
            f'🔻 Введите площадь {reality}ы. Используйте разделитель "." (точку) для целой и десятичной части'
        )
        bot.register_next_step_handler(callback.message, get_area)

    elif callback.data == 'yes_encumbrance':
        global encumbrance
        encumbrance = True
        keyboard = InlineKeyboardMarkup()
        key_1 = InlineKeyboardButton(text='Да', callback_data='yes_children')
        key_2 = InlineKeyboardButton(text='Нет', callback_data='no_children')
        keyboard.add(key_1, key_2)
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text='🔻 В собственности есть несовершеннолетние?',
            reply_markup=keyboard
        )

    elif callback.data == 'no_encumbrance':
        encumbrance = False
        keyboard = InlineKeyboardMarkup()
        key_1 = InlineKeyboardButton(text='Да', callback_data='yes_children')
        key_2 = InlineKeyboardButton(text='Нет', callback_data='no_children')
        keyboard.add(key_1, key_2)
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text='🔻 В собственности есть несовершеннолетние?',
            reply_markup=keyboard
        )

    elif callback.data == 'yes_children':
        global children
        children = True
        keyboard = InlineKeyboardMarkup()
        key_1 = InlineKeyboardButton(text='Да', callback_data='yes_mortage')
        key_2 = InlineKeyboardButton(text='Нет', callback_data='no_mortage')
        keyboard.add(key_1, key_2)
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text=f'🔻 {reality}у можно купить по программе ипотечного кредитования?',
            reply_markup=keyboard
        )

    elif callback.data == 'no_children':
        children = False
        keyboard = InlineKeyboardMarkup()
        key_1 = InlineKeyboardButton(text='Да', callback_data='yes_mortage')
        key_2 = InlineKeyboardButton(text='Нет', callback_data='no_mortage')
        keyboard.add(key_1, key_2)
        if reality == 'дом' or reality == 'таунхаус' or reality == 'участок':
            bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.id,
                text=f'🔻 {reality} можно купить по программе ипотечного кредитования?',
                reply_markup=keyboard
            )
        else:
            bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.id,
                text=f'🔻 {reality}у можно купить по программе ипотечного кредитования?',
                reply_markup=keyboard
            )

    elif callback.data == 'yes_mortage':
        global mortage
        mortage = True
        bot.send_message(
            callback.from_user.id,
            '🔻 Ведите свой номер '
            + 'телефона в формате 89ххххххххх, по которому с'
            + 'вами можно будет связаться'
        )
        bot.register_next_step_handler(callback.message, get_phone_number)

    elif callback.data == 'no_mortage':
        mortage = False
        bot.send_message(
            callback.from_user.id,
            '🔻 Ведите свой номер '
            + 'телефона в формате 89ххххххххх, по которому с'
            + 'вами можно будет связаться'
        )
        bot.register_next_step_handler(callback.message, get_phone_number)

    elif callback.data in [
        'edit_1к.кв.', 'edit_2к.кв.',
        'edit_3к.кв.', 'edit_4к.кв.',
        'edit_5к.кв.'
    ]:
        global objects_group
        objects_group = 'Apartment'
        bot.send_message(
            callback.from_user.id,
            'Напишите id объекта, цену которго желаете изменить. id можно узнать в /myobjects'
        )
        bot.register_next_step_handler(callback.message, get_pk_edit_price)

    elif callback.data == 'edit_Комната':
        objects_group = 'Room'
        bot.send_message(
            callback.from_user.id,
            'Напишите id объекта, цену которго желаете изменить. id можно узнать в /myobjects'
        )
        bot.register_next_step_handler(callback.message, get_pk_edit_price)

    elif callback.data == 'edit_Дом':
        objects_group = 'House'
        bot.send_message(
            callback.from_user.id,
            'Напишите id объекта, цену которго желаете изменить. id можно узнать в /myobjects'
        )
        bot.register_next_step_handler(callback.message, get_pk_edit_price)

    elif callback.data == 'edit_Таунхаус':
        objects_group = 'TownHouse'
        bot.send_message(
            callback.from_user.id,
            'Напишите id объекта, цену которго желаете изменить. id можно узнать в /myobjects'
        )
        bot.register_next_step_handler(callback.message, get_pk_edit_price)

    elif callback.data == 'edit_Участок':
        objects_group = 'Land'
        bot.send_message(
            callback.from_user.id,
            'Напишите id объекта, цену которго желаете изменить. id можно узнать /myobjects'
        )
        bot.register_next_step_handler(callback.message, get_pk_edit_price)

# bot.polling(none_stop=True, interval=0)
bot.infinity_polling()

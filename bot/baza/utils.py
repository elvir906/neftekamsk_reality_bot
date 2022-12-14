import sys

from aiogram.types import InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardButton
from baza.models import Apartment, House, Land, Room, TownHouse


class keyboards():
    def get_category_keyboard():
        """генерация клавиатуры выбора по категориям"""

        mc_count = Room.objects.count()
        house_count = House.objects.count()
        townhouse_count = TownHouse.objects.count()
        land_count = Land.objects.count()
        apartment_count = Apartment.objects.count()

        buttons_names = ['Квартиры', 'Комнаты', 'Дома', 'Таунхаусы', 'Участки']
        quantitative_indicator = [
            apartment_count,
            mc_count,
            house_count,
            townhouse_count,
            land_count
        ]
        keyboard = InlineKeyboardMarkup()

        for i in range(0, len(buttons_names)):
            keyboard.add(
                InlineKeyboardButton(
                    buttons_names[i]+' ('+str(quantitative_indicator[i])+')',
                    callback_data=f'{buttons_names[i]}'
                    )
            )
        return keyboard

    def get_rooms_count_keyboard():
        """Генерация клавиатуры выбора по количеству комнат квартир"""

        one_room_quantity = Apartment.objects.filter(room_quantity=1).count()
        two_room_quantity = Apartment.objects.filter(room_quantity=2).count()
        three_room_quantity = Apartment.objects.filter(room_quantity=3).count()
        four_room_quantity = Apartment.objects.filter(room_quantity=4).count()
        five_room_quantity = Apartment.objects.filter(room_quantity=5).count()

        keyboard = InlineKeyboardMarkup()

        buttons = [
            '1-комнатные', '2-комнатные', '3-комнатные',
            '4-комнатные', '5-комнатные', '⏪ Назад'
        ]

        quantity = [
            one_room_quantity, two_room_quantity,
            three_room_quantity, four_room_quantity, five_room_quantity
        ]

        for i in range(0, len(buttons)-1):
            keyboard.add(
                InlineKeyboardButton(
                    buttons[i]+' ('+str(quantity[i])+')',
                    callback_data=f'{buttons[i]}'
                )
            )

        keyboard.add(
            InlineKeyboardButton(
                buttons[len(buttons)-1],
                callback_data=f'{buttons[len(buttons)-1]}'
            )
        )

        return keyboard

    def add_category_keyboard():
        """Генерация клавиатуры для добавления объекта"""

        keyboard = InlineKeyboardMarkup()
        buttons = ['Квартиру', 'Комнату', 'Дом', 'Таунхаус', 'Участок']

        for i in range(0, len(buttons)):
            keyboard.add(
                InlineKeyboardButton(
                    buttons[i], callback_data=f'{buttons[i]}'
                    )
            )
        return keyboard

    def add_rooms_count_keyboard():
        """
        Генерация клавиатуры на выбор количества
        комнат при добавления квартиры.
        """

        keyboard = InlineKeyboardMarkup()
        # Генерация кнопок с указанием этажей 1-5
        buttons = [InlineKeyboardButton(
            text=str(i),
            callback_data=f'add_{str(i)}_room'
        ) for i in range(1, 6)]
        keyboard.row(*buttons)
        return keyboard

    def floor_number_or_count_keyboard(object: str):
        """Генерация клавиатуры на выбор этажа или этажности дома"""

        #  Генерация названий кнопок и коллбэк_дат. Количество кнопок = 18
        keyboard = InlineKeyboardMarkup()
        buttons_text = [str(i) for i in range(1, 19)]
        if object == 'apartment_floor':
            callback_data = [str(i) + '_afloor' for i in range(1, 19)]
        if object == 'apartment_house_floors':
            callback_data = [str(i) + '_afloors' for i in range(1, 19)]
        if object == 'room_floor':
            callback_data = [str(i) + '_rfloor' for i in range(1, 19)]
        if object == 'room_house_floors':
            callback_data = [str(i) + '_rfloors' for i in range(1, 19)]

        # Генерация кнопок 18 этажей, шесть в три ряда.
        for j in range(0, 3):
            buttons = [InlineKeyboardButton(
                text=buttons_text[i],
                callback_data=callback_data[i]
            ) for i in range(j * 6, 6 + 6 * j)]
            keyboard.row(*buttons)
        return keyboard

    def yes_no_keyboard(item: str):
        """Генерация клавиатуры на да/нет по различным вопросам"""

        keyboard = InlineKeyboardMarkup()
        key_1 = InlineKeyboardButton(
            text='Да', callback_data=f'yes_{item}'
        )
        key_2 = InlineKeyboardButton(
            text='Нет', callback_data=f'no_{item}'
        )
        keyboard.row(key_1, key_2)
        return keyboard

    def microregion_keyboard():
        """Генерация клавиатуры на выбор микрорайона"""

        keyboard = InlineKeyboardMarkup()
        microregion_buttons_text = [
            'Касёво', 'Восточный 1,2,3,4,5', 'Ротково',
            'Марино', 'Телевышка', 'Лесная поляна',
            'Михайловка', 'Ташкиново', 'Николо-Берёзовка',
            'Кутлинка', 'Новонагаево', 'Актанышбаш',
            'Амзя', 'Карманово', 'Можары', 'Арлан',
            'Зубовка', 'Кариево'
        ]
        buttons = [
            InlineKeyboardButton(
                text=microregion_buttons_text[i],
                callback_data=microregion_buttons_text[i]
                ) for i in range(0, len(microregion_buttons_text) - 1)
        ]
        keyboard.row(buttons[0], buttons[2])
        keyboard.row(buttons[7], buttons[5])
        keyboard.row(buttons[3], buttons[4], buttons[6])
        keyboard.row(buttons[8], buttons[1])
        keyboard.row(buttons[9], buttons[10], buttons[11])
        keyboard.row(buttons[12], buttons[13], buttons[14])
        keyboard.row(buttons[15], buttons[16])

        return keyboard

    def purpose_choise_keyboard():
        keyboard = InlineKeyboardMarkup()
        key_1 = InlineKeyboardButton(text='ИЖС', callback_data='ИЖС')
        key_2 = InlineKeyboardButton(text='СНТ, ДНТ', callback_data='СНТ, ДНТ')
        key_3 = InlineKeyboardButton(text='ЛПХ', callback_data='ЛПХ')

        keyboard.row(key_1, key_2, key_3)
        return keyboard

    def gaz_choise_keyboard():
        keyboard = InlineKeyboardMarkup()
        key_1 = InlineKeyboardButton(
            text='Газифицирован, дом отапливается',
            callback_data='Газифицирован, дом отапливается'
        )
        key_3 = InlineKeyboardButton(
            text='Улица газифицировна, дом - нет',
            callback_data='Улица газифицировна, дом - нет'
        )
        key_4 = InlineKeyboardButton(
            text='Улица не газифицирована',
            callback_data='Улица не газифицирована'
        )

        keyboard.row(key_1)
        keyboard.row(key_3)
        keyboard.row(key_4)
        return keyboard

    def material_choice_keyboard():
        keyboard = InlineKeyboardMarkup()
        material_buttons_text = [
            'Кирпич',
            'Заливной',
            'Блок, облицованный кирпичом',
            'Дерево',
            'Дерево, облицованное кирпичом',
            'Другое'
        ]
        buttons = [
            InlineKeyboardButton(
                text=material_buttons_text[i],
                callback_data=material_buttons_text[i]
                ) for i in range(0, len(material_buttons_text) - 1)
        ]

        for i in range(0, len(buttons)):
            keyboard.row(buttons[i])
        return keyboard

    def water_choice_keyboard():
        keyboard = InlineKeyboardMarkup()
        key_1 = InlineKeyboardButton(
            text='Да, центральное водоснабжение',
            callback_data='Водоснабжение центральное'
        )
        key_2 = InlineKeyboardButton(
            text='На участке есть колодец',
            callback_data='Колодец'
        )
        key_3 = InlineKeyboardButton(
            text='Вода проходит по улице, в дом - нет',
            callback_data='Вода по улице'
        )
        key_4 = InlineKeyboardButton(text='Воды нет', callback_data='Воды нет')

        keyboard.row(key_1)
        keyboard.row(key_2)
        keyboard.row(key_3)
        keyboard.row(key_4)
        return keyboard

    def road_choice_keyboard():
        keyboard = InlineKeyboardMarkup()
        key_1 = InlineKeyboardButton(
            text='Да, асфальт',
            callback_data='Асфальт'
        )
        key_2 = InlineKeyboardButton(
            text='Да, неплохая насыпная дорога',
            callback_data='Неплохая насыпная дорога'
        )
        key_3 = InlineKeyboardButton(
            text='Да, неплохая грунтовая дорога',
            callback_data='Неплохая грунтовая дорога'
        )
        key_4 = InlineKeyboardButton(
            text='Движение к дому затруднено',
            callback_data='Бездорожье, затрудняющее проезд'
        )
        keyboard.row(key_1)
        keyboard.row(key_2)
        keyboard.row(key_3)
        keyboard.row(key_4)
        return keyboard

    # def price_editing_keyboard():
    #     keyboard = InlineKeyboardMarkup()
    #     buttons = [
    #         '1к.кв.', '2к.кв.', '3к.кв.', '4к.кв.', '5к.кв.',
    #         'Комната', 'Дом', 'Таунхаус', 'Участок'
    #     ]
    #     for i in range(0, len(buttons)):
    #         keyboard.add(
    #            InlineKeyboardButton(
    #               buttons[i], callback_data=f'edit_{buttons[i]}'
    #               )
    #         )
    #     return keyboard

    def objects_list_keyboard(searching_phone_number: str):
        keyboard = InlineKeyboardMarkup()

        apartment_queryset = Apartment.objects.filter(
            phone_number=searching_phone_number
        )
        room_queryset = Room.objects.filter(
            phone_number=searching_phone_number
        )
        house_queryset = House.objects.filter(
            phone_number=searching_phone_number
        )
        townhouse_queryset = TownHouse.objects.filter(
            phone_number=searching_phone_number
        )
        land_queryset = Land.objects.filter(
            phone_number=searching_phone_number
        )

        buttons = []
        callback_data_string = []

        for item in apartment_queryset:
            buttons.append(f'ID {item.pk} {item.room_quantity}к.кв. '
                           + f'{item.street_name} {item.number_of_house} '
                           + f'- {int(item.price)} ₽')
            callback_data_string.append([item.pk, 'apartment'])

        for item in room_queryset:
            buttons.append(f'ID {item.pk} Комната {item.street_name} '
                           + f'{item.number_of_house} - {int(item.price)} ₽')
            callback_data_string.append([item.pk, 'room'])

        for item in house_queryset:
            buttons.append(f'ID {item.pk}  Дом {item.microregion} '
                           + f'{item.street_name} - {int(item.price)} ₽')
            callback_data_string.append([item.pk, 'house'])

        for item in townhouse_queryset:
            buttons.append(f'ID {item.pk}  Дом {item.microregion} '
                           + f'{item.street_name} - {int(item.price)} ₽')
            callback_data_string.append([item.pk, 'townhouse'])

        for item in land_queryset:
            buttons.append(f'ID {item.pk}  Дом {item.microregion} '
                           + f'{item.street_name} {item.number_of_land} - '
                           + f'{int(item.price)} ₽')
            callback_data_string.append([item.pk, 'land'])

        for i in range(0, len(buttons)):
            keyboard.row(
                InlineKeyboardButton(
                    buttons[i],
                    callback_data=f'{callback_data_string[i][0]} '
                    + f'{callback_data_string[i][1]}'
                )
            )
        # print(callback_data_string)
        return keyboard


class Output():
    def false_or_true(item: bool) -> str:
        if item:
            return 'Есть'
        return 'Нет'

# Строку в название класса
    def str_to_class(str):
        return getattr(sys.modules[__name__], str)

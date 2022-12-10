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

    def yes_no_keyboard(restriction: str):
        keyboard = InlineKeyboardMarkup()
        key_1 = InlineKeyboardButton(
            text='Да', callback_data=f'yes_{restriction}'
        )
        key_2 = InlineKeyboardButton(
            text='Нет', callback_data=f'no_{restriction}'
        )
        keyboard.row(key_1, key_2)
        return keyboard


class Output():
    def c_m_e(item):
        """Дети. Ипотека. Обременение"""
        result = ['Нет', 'Нет', 'Нет']

        if item.children:
            result[0] = 'Есть'

        if item.mortage:
            result[1] = 'Есть'

        if item.encumbrance:
            result[2] = 'Есть'

        return result

    def false_or_true(item: bool) -> str:
        if item:
            return 'Есть'
        return 'Нет'

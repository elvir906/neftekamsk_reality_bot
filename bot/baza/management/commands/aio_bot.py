import logging
import os
import re

import django
# import psycopg2
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from baza.answer_messages import message_texts
from baza.db_worker import DB_Worker
from baza.models import Apartment, House, Land, Room, TownHouse
from baza.states import (CallbackOnStart, HouseCallbackStates,
                         LandCallbackStates, MyObjectsCallbackStates,
                         PriceEditCallbackStates, RoomCallbackStates,
                         TownHouseCallbackStates)
# from baza.users import users
from baza.utils import keyboards
from decouple import config
from django.core.management.base import BaseCommand

from baza.utils import Output

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

DB_NAME = config('DB_NAME')
POSTGRES_USER = config('POSTGRES_USER')
POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')

bot = Bot(token=config('TELEGRAM_TOKEN'))

dp = Dispatcher(bot, storage=MemoryStorage())


class Command(BaseCommand):
    def handle(self, *args, **options):
        executor.start_polling(dp, skip_updates=True)


@dp.message_handler(commands=['deleteobject'])
async def delete_object(message: types.Message):
    """Ответ на кнопку удаления объекта."""

    await message.answer(message_texts.on.get('delete'))


@dp.message_handler(commands=['about'])
async def about(message: types.Message):
    """Ответ на кнопку информации о боте."""

    await message.answer(
        '\n'.join(message_texts.on.get('about')),
        parse_mode='markdown'
    )


@dp.message_handler(commands=['getstatistics'])
async def get_statistics(message: types.Message):
    """Ответ на кнопку просмотра статистики."""

    await message.answer(message_texts.on.get('statistics'))


@dp.message_handler(commands=['searchobjects'])
async def search_objects(message: types.Message):
    """Ответ на кнопку просмотра базы"""

    await message.answer(
        '🔻 Выберите категорию объектов для поиска',
        reply_markup=keyboards.get_category_keyboard()
    )


@dp.message_handler(commands=['addobject'])
async def add_object(message: types.Message):
    """Ответ на кнопку обавления объекта"""

    await message.answer(
        '🔻 Что желаете добавить?',
        reply_markup=keyboards.add_category_keyboard()
    )


@dp.callback_query_handler(text="Квартиры")
async def apartments(callback: types.CallbackQuery):
    """Ответ на кнопку поиска по квартирам"""

    await callback.message.edit_text(
        '🔻 Выберите по количеству комнат',
        reply_markup=keyboards.get_rooms_count_keyboard()
    )


@dp.callback_query_handler(text='Комнаты')
async def rooms(callback: types.CallbackQuery):
    """Ответ на кнопку поиска по комнатам"""

    await callback.message.answer(
        '✳ Вот, что я нашёл по *комнатам*:',
        parse_mode="MarkdownV2"
    )
    query_set = Room.objects.order_by('-pub_date')
    for item in query_set:
        await callback.message.answer(
            message_texts.room_search_result_text(item),
            parse_mode='Markdown'
        )


@dp.callback_query_handler(text='Дома')
async def houses(callback: types.CallbackQuery):
    """Ответ на кнопку поиска по домам"""

    await callback.message.answer(
        '✳ Вот, что я нашёл по *домам*:',
        parse_mode="MarkdownV2",
    )
    query_set = House.objects.order_by('-pub_date')
    for item in query_set:
        await callback.message.answer(
            message_texts.house_search_result_text(item),
            parse_mode='Markdown'
        )


@dp.callback_query_handler(text='Таунхаусы')
async def townhouses(callback: types.CallbackQuery):
    """Ответ на кнопку поиска по таунхаусам"""

    await callback.message.answer(
        '✳ Вот, что я нашёл по *таунхаусам*:',
        parse_mode="MarkdownV2",
    )
    query_set = TownHouse.objects.order_by('-pub_date')
    for item in query_set:
        await callback.message.answer(
            message_texts.townhouse_search_result_text(item),
            parse_mode='Markdown'
        )


@dp.callback_query_handler(text='Участки')
async def lands(callback: types.CallbackQuery):
    """Ответ на кнопку поиска по участкам"""

    await callback.message.answer(
        '✳ Вот, что я нашёл по *участкам*:',
        parse_mode="MarkdownV2",
    )
    query_set = Land.objects.order_by('-pub_date')
    for item in query_set:
        await callback.message.answer(
            message_texts.lands_search_result_text(item),
            parse_mode='Markdown'
        )


@dp.callback_query_handler(text='⏪ Назад')
async def back_button_action(callback: types.CallbackQuery):
    """Ответ на кнопку НАЗАД при просмотре категорий"""

    await callback.message.edit_text(
        '🔻 Выберите категорию объектов для поиска',
        reply_markup=keyboards.get_category_keyboard()
    )


@dp.callback_query_handler(text=[
    '1-комнатные', '2-комнатные',
    '3-комнатные', '4-комнатные',
    '5-комнатные'
])
async def apartment_search_result(callback: types.CallbackQuery):
    """Ответ на кнопку просмотра квартир"""

    room_count = callback.data.removesuffix('-комнатные')
    await callback.message.answer(
        f'✳ Вот, что я нашёл по *{room_count}-комнатным*:',
        parse_mode="Markdown",
    )
    query_set = Apartment.objects.filter(
        room_quantity=int(room_count)
    ).order_by('-pub_date')
    for item in query_set:
        await callback.message.answer(
            message_texts.apartments_search_result_text(int(room_count), item),
            parse_mode='Markdown'
        )


#   с этого места опрос по квартире
@dp.callback_query_handler(text='Квартиру')
async def add_apartment(callback: types.CallbackQuery, state: FSMContext):
    """Ответ на кнопку добавления квартиры"""

    await state.update_data(reality_category=callback.data)
    await callback.message.edit_text(
        'Приготовьтесь ответить на 13 вопросов про ваш объект '
        + 'недвижимости. 😏 Это займёт не более 2-3х минут.'
        + '\n'
        + '\n🔻 Введите количество комнат',
        reply_markup=keyboards.add_rooms_count_keyboard()
    )


# С ЭТОГО МЕСТА ОПРОС ПО КВАРТИРЕ
@dp.callback_query_handler(text=[
    'add_1_room', 'add_2_room',
    'add_3_room', 'add_4_room',
    'add_5_room'
])
async def entering_room_count(callback: types.CallbackQuery, state: FSMContext):
    """Ответ на нажатие выбора количества комнат при добавлении кв."""

    await state.update_data(room_count=callback.data[4])
    await callback.message.edit_text(
        '🔻 Напишите назавание улицы c заглавной буквы'
    )
    await CallbackOnStart.Q1.set()


@dp.message_handler(state=CallbackOnStart.Q1)
async def entering_street_name(message: types.Message, state: FSMContext):
    """Запись названия улицы, следующий вопрос """

    answer = message.text.title()
    await state.update_data(street_name=answer)

    await message.answer(
        '🔻 Напишите номер дома в формате "5", "5А" или "91 корп.1'
    )
    await CallbackOnStart.next()


@dp.message_handler(state=CallbackOnStart.Q2)
async def entering_house_number(message: types.Message, state: FSMContext):
    """Запись номера дома. Следующий вопрос """

    answer = message.text.upper()
    await state.update_data(house_number=answer)
    await message.answer(
        '🔻 Введите этаж квартиры',
        reply_markup=keyboards.floor_number_or_count_keyboard('apartment_floor')
    )
    await CallbackOnStart.next()


@dp.callback_query_handler(state=CallbackOnStart.Q3, text=[
    '1_afloor', '2_afloor', '3_afloor', '4_afloor', '5_afloor', '6_afloor',
    '7_afloor', '8_afloor', '9_afloor', '10_afloor', '11_afloor', '12_afloor',
    '13_afloor', '14_afloor', '15_afloor', '16_afloor', '17_afloor', '18_afloor',
])
async def entering_floor(callback: types.CallbackQuery, state: FSMContext):
    """Ответ на кнопку выбора этажа квартиры"""

    await state.update_data(floor=callback.data.removesuffix('_afloor'))
    await callback.message.edit_text(
        '🔻 Введите количество этажей',
        reply_markup=keyboards.floor_number_or_count_keyboard('apartment_house_floors')
    )
    await CallbackOnStart.next()


@dp.callback_query_handler(state=CallbackOnStart.Q4, text=[
    '1_afloors', '2_afloors', '3_afloors', '4_afloors', '5_afloors', '6_afloors',
    '7_afloors', '8_afloors', '9_afloors', '10_afloors', '11_afloors', '12_afloors',
    '13_afloors', '14_afloors', '15_afloors', '16_afloors', '17_afloors', '18_afloors',
])
async def entering_floors(callback: types.CallbackQuery, state: FSMContext):
    """Ответ на кнопку выбора этажности дома"""

    await state.update_data(floors=callback.data.removesuffix('_afloors'))

    await callback.message.edit_text(
        '🔻 Введите площадь квартиры, как в указано в свидетельстве или выписке'
    )
    await CallbackOnStart.next()


@dp.message_handler(state=CallbackOnStart.Q5)
async def entering_area(message: types.Message, state: FSMContext):
    """Запись площади квартиры"""

    try:
        answer = float(message.text)
        await state.update_data(area=answer)
        await message.answer(
            '🔻 Напишите цену.\n\nПросто полную цену цифрами, '
            + 'не сокращая, и без знаков Р, р, ₽, руб. и т.п.\n\nЕсли недвижимость '
            + 'стоит 3400000 рублей, значит так и пишите 3400000'
        )
        await CallbackOnStart.next()

    except (ValueError) as e:
        await CallbackOnStart.Q5.set()
        await message.answer(
            '🤔 Вы ошиблись при вводе значения площади.\n\nПлощадь'
            + ' следует вводить цифрами и использовать разделитель "." для '
            + 'дробных значений. Так же НЕ указывайтье единицы измерения. '
            + ''
            + 'Попробуйте ввести значение заново:'
        )
        logging.error(f'{e}')


@dp.message_handler(state=CallbackOnStart.Q6)
async def entering_price(message: types.Message, state: FSMContext):
    """Запись цены"""

    try:
        answer = int(message.text)
        await state.update_data(price=answer)
        await message.answer(
            '🔻 Добавьте небольшое описание квартиры.\n\nПожалуйста, '
            + ' руководствуйтесь принципом "Краткость - сестра таланта" '
            + ' и не дублируйте '
            + 'в описании информацию о квартире, такие как этаж, цена и др. '
            + '\n\nТолько кратко, самую суть - состояние.'
        )
        await CallbackOnStart.next()

    except (ValueError) as e:
        await CallbackOnStart.Q6.set()
        await message.answer(
            '🤔 🤔 Вы ошиблись при вводе значения цены. Цену'
            + ' следует вводить цифрами без разделителя "." '
            + 'и без указания единицы измерения.'
            + ''
            + 'Попробуйте ввести значение заново:'
        )
        logging.error(f'{e}')


@dp.message_handler(state=CallbackOnStart.Q7)
async def entering_description(message: types.Message, state: FSMContext):
    """Запись состояния"""

    answer = message.text
    await state.update_data(description=answer)
    await message.answer(
        '🔻 На недвижимости есть обременение?',
        reply_markup=keyboards.yes_no_keyboard('encumbrance')
    )
    await CallbackOnStart.next()


@dp.callback_query_handler(
    state=CallbackOnStart.Q8,
    text=['yes_encumbrance', 'no_encumbrance']
)
async def entering_encumbrance(callback: types.CallbackQuery, state: FSMContext):
    """Запись наличия обременения"""

    if callback.data == 'yes_encumbrance':
        await state.update_data(encumbrance=True)
    if callback.data == 'no_encumbrance':
        await state.update_data(encumbrance=False)
    await callback.message.edit_text(
        '🔻 В собственности есть дети?',
        reply_markup=keyboards.yes_no_keyboard('children')
    )
    await CallbackOnStart.next()


@dp.callback_query_handler(
    state=CallbackOnStart.Q9,
    text=['yes_children', 'no_children']
)
async def entering_children(callback: types.CallbackQuery, state: FSMContext):
    """Запись наличия детей"""

    if callback.data == 'yes_children':
        await state.update_data(children=True)
    if callback.data == 'no_children':
        await state.update_data(children=False)
    await callback.message.edit_text(
        '🔻 Недвижимость возможно купить по иптоеке?',
        reply_markup=keyboards.yes_no_keyboard('mortage')
    )
    await CallbackOnStart.next()


@dp.callback_query_handler(
    state=CallbackOnStart.Q10,
    text=['yes_mortage', 'no_mortage']
)
async def entering_mortage(callback: types.CallbackQuery, state: FSMContext):
    """Запись возможности покупки в ипотеку"""

    if callback.data == 'yes_mortage':
        await state.update_data(mortage=True)
    if callback.data == 'no_mortage':
        await state.update_data(mortage=False)
    await callback.message.edit_text(
        '🔻 Напишите свой номер '
        + 'телефона в формате 89ххххххххх, по которому с'
        + 'вами можно будет связаться'
    )
    await CallbackOnStart.next()


@dp.message_handler(state=CallbackOnStart.Q11)
async def entering_phone_number(message: types.Message, state: FSMContext):
    """Запись номера телефона"""

    if re.match(r"^[0-9]+$", message.text):
        await state.update_data(phone_number=message.text)
        await message.answer(
            '🔻 В каком агентстве вы трудитесь?\n\n'
            + 'Если вы частный риелтор, то напишите "Частный"'
        )
        await CallbackOnStart.next()
    else:
        await message.answer(
            '🔻 Вы ошиблись с вводом номера телефона. '
            + f'Введённый вами номер телефона {message.text} '
            + 'не соответствует формату "89ххххххххх". '
            + '\n'
            + 'Введите просто 11 цифр номера, начиная с 8.'
        )
        logging.error('Ошибка при вводе номера телефона')
        await CallbackOnStart.Q11.set()


@dp.message_handler(state=CallbackOnStart.Q12)
async def entering_agency_name(message: types.Message, state: FSMContext):
    """Запись названия агентства"""

    answer = message.text.title()
    await state.update_data(agency_name=answer)
    await message.answer(
        '🔻 Напишите своё имя'
    )
    await CallbackOnStart.next()


@dp.message_handler(state=CallbackOnStart.Q13)
async def entering_rialtor_name(message: types.Message, state: FSMContext):
    """Запись имени риелтора и вывод результирующего текста"""

    answer = message.text.title()
    await state.update_data(rieltor_name=answer)
    data = await state.get_data()

    # ЗАПИСЬ В БАЗУ
    if not DB_Worker.apartment_to_db(data):
        await message.answer(
            'К сожаления, в работе бота произошла ошибка. Попробуйте еще раз. '
            + 'Если ошибка повторится, напишите об этом @davletelvir'
        )
    else:
        await message.answer(
            '\n'.join(
                message_texts.apartment_adding_result_text(data)
            ),
            parse_mode="Markdown"
        )
    await state.finish()


# С ЭТОГО МЕСТА ОПРОС ПО КОМНАТЕ
@dp.callback_query_handler(text='Комнату')
async def add_room(callback: types.CallbackQuery, state: FSMContext):
    """Ответ на кнопку добавления квартиры"""

    await state.update_data(room_reality_category=callback.data)
    await callback.message.edit_text(
        'Приготовьтесь ответить на несколько вопросов про ваш объект '
        + 'недвижимости. 😏 Это займёт не более 2-3х минут.'
        + '\n'
        + '\n🔻 Напишите название улицы'
    )
    await RoomCallbackStates.R1.set()


@dp.message_handler(state=RoomCallbackStates.R1)
async def enetering_rooms_street_name(
    message: types.Message, state: FSMContext
):
    """Запись названия улицы комнаты"""

    await state.update_data(room_street_name=message.text.title())
    await message.answer(
        '🔻 Напишите номер дома в формате "5", "5А" или "91 корп.1'
    )
    await RoomCallbackStates.next()


@dp.message_handler(state=RoomCallbackStates.R2)
async def enetering_rooms_house_number(
    message: types.Message, state: FSMContext
):
    """Запись номера дома"""

    await state.update_data(room_house_number=message.text.upper())
    await message.answer(
        '🔻 Введите этаж комнаты',
        reply_markup=keyboards.floor_number_or_count_keyboard('room_floor')
    )
    await RoomCallbackStates.next()


@dp.callback_query_handler(state=RoomCallbackStates.R3, text=[
    '1_rfloor', '2_rfloor', '3_rfloor', '4_rfloor', '5_rfloor', '6_rfloor',
    '7_rfloor', '8_rfloor', '9_rfloor', '10_rfloor', '11_rfloor', '12_rfloor',
    '13_rfloor', '14_rfloor', '15_rfloor', '16_rfloor', '17_rfloor', '18_rfloor',
])
async def entering_room_floor(callback: types.CallbackQuery, state: FSMContext):
    """Ответ на кнопку выбора этажа комнаты"""

    await state.update_data(room_floor=callback.data.removesuffix('_rfloor'))
    await callback.message.edit_text(
        '🔻 Введите количество этажей',
        reply_markup=keyboards.floor_number_or_count_keyboard('room_house_floors')
    )
    await RoomCallbackStates.next()


@dp.callback_query_handler(state=RoomCallbackStates.R4, text=[
    '1_rfloors', '2_rfloors', '3_rfloors', '4_rfloors', '5_rfloors', '6_rfloors',
    '7_rfloors', '8_rfloors', '9_rfloors', '10_rfloors', '11_rfloors', '12_rfloors',
    '13_rfloors', '14_rfloors', '15_rfloors', '16_rfloors', '17_rfloors', '18_rfloors',
])
async def entering_room_floors(
    callback: types.CallbackQuery, state: FSMContext
):
    """Ответ на кнопку выбора этажности дома"""

    await state.update_data(room_floors=callback.data.removesuffix('_rfloors'))
    await callback.message.edit_text(
        '🔻 Введите площадь комнаты, как в указано в свидетельстве или выписке'
    )
    await RoomCallbackStates.next()


@dp.message_handler(state=RoomCallbackStates.R5)
async def enetering_rooms_area(
    message: types.Message, state: FSMContext
):
    """Запись площади комнаты"""

    try:
        answer = float(message.text)
        await state.update_data(room_area=answer)
        await message.answer(
            '🔻 Напишите цену.\n\nПросто полную цену цифрами, '
            + 'не сокращая, и без знаков Р, р, ₽, руб. и т.п.\n\nЕсли недвижимость '
            + 'стоит 3400000 рублей, значит так и пишите 3400000'
        )
        await RoomCallbackStates.next()

    except (ValueError) as e:
        await RoomCallbackStates.R5.set()
        await message.answer(
            '🤔 Вы ошиблись при вводе значения площади.\n\nПлощадь'
            + ' следует вводить цифрами и использовать разделитель "." для '
            + 'дробных значений. Так же НЕ указывайтье единицы измерения. '
            + ''
            + 'Попробуйте ввести значение заново:'
        )
        logging.error(f'{e}')


@dp.message_handler(state=RoomCallbackStates.R6)
async def entering_room_price(message: types.Message, state: FSMContext):
    """Запись цены"""

    try:
        answer = int(message.text)
        await state.update_data(room_price=answer)
        await message.answer(
            '🔻 Добавьте небольшое описание комнаты.\n\nПожалуйста, '
            + ' руководствуйтесь принципом "Краткость - сестра таланта" '
            + ' и не дублируйте '
            + 'в описании информацию о квартире, такие как этаж, цена и др. '
            + '\n\nТолько кратко, самую суть - состояние.'
        )
        await RoomCallbackStates.next()

    except (ValueError) as e:
        await RoomCallbackStates.R6.set()
        await message.answer(
            '🤔 🤔 Вы ошиблись при вводе значения цены. Цену'
            + ' следует вводить цифрами без разделителя "." '
            + 'и без указания единицы измерения.'
            + ''
            + 'Попробуйте ввести значение заново:'
        )
        logging.error(f'{e}')


@dp.message_handler(state=RoomCallbackStates.R7)
async def entering_room_description(message: types.Message, state: FSMContext):
    """Запись состояния"""

    answer = message.text
    await state.update_data(room_description=answer)
    await message.answer(
        '🔻 На недвижимости есть обременение?',
        reply_markup=keyboards.yes_no_keyboard('room_encumbrance')
    )
    await RoomCallbackStates.next()


@dp.callback_query_handler(
    state=RoomCallbackStates.R8,
    text=['yes_room_encumbrance', 'no_room_encumbrance']
)
async def entering_room_encumbrance(
    callback: types.CallbackQuery, state: FSMContext
):
    """Запись наличия обременения"""

    if callback.data == 'yes_room_encumbrance':
        await state.update_data(room_encumbrance=True)
    if callback.data == 'no_room_encumbrance':
        await state.update_data(room_encumbrance=False)
    await callback.message.edit_text(
        '🔻 В собственности есть дети?',
        reply_markup=keyboards.yes_no_keyboard('room_children')
    )
    await RoomCallbackStates.next()


@dp.callback_query_handler(
    state=RoomCallbackStates.R9,
    text=['yes_room_children', 'no_room_children']
)
async def entering_room_children(callback: types.CallbackQuery, state: FSMContext):
    """Запись наличия детей"""

    if callback.data == 'yes_room_children':
        await state.update_data(room_children=True)
    if callback.data == 'no_room_children':
        await state.update_data(room_children=False)
    await callback.message.edit_text(
        '🔻 Недвижимость возможно купить по иптоеке?',
        reply_markup=keyboards.yes_no_keyboard('room_mortage')
    )
    await RoomCallbackStates.next()


@dp.callback_query_handler(
    state=RoomCallbackStates.R10,
    text=['yes_room_mortage', 'no_room_mortage']
)
async def entering_room_mortage(callback: types.CallbackQuery, state: FSMContext):
    """Запись возможности покупки в ипотеку"""

    if callback.data == 'yes_room_mortage':
        await state.update_data(room_mortage=True)
    if callback.data == 'no_room_mortage':
        await state.update_data(room_mortage=False)
    await callback.message.edit_text(
        '🔻 Напишите свой номер '
        + 'телефона в формате 89ххххххххх, по которому с'
        + 'вами можно будет связаться'
    )
    await RoomCallbackStates.next()


@dp.message_handler(state=RoomCallbackStates.R11)
async def entering_room_phone_number(message: types.Message, state: FSMContext):
    """Запись номера телефона"""

    if re.match(r"^[0-9]+$", message.text):
        await state.update_data(room_phone_number=message.text)
        await message.answer(
            '🔻 В каком агентстве вы трудитесь?\n\n'
            + 'Если вы частный риелтор, то напишите "Частный"'
        )
        await RoomCallbackStates.next()
    else:
        await message.answer(
            '🔻 Вы ошиблись с вводом номера телефона. '
            + f'Введённый вами номер телефона {message.text} '
            + 'не соответствует формату "89ххххххххх". '
            + '\n'
            + 'Введите просто 11 цифр номера, начиная с 8'
        )
        logging.error("Ошибка при вводе номера телефона")
        await RoomCallbackStates.R11.set()


@dp.message_handler(state=RoomCallbackStates.R12)
async def entering_room_agency_name(message: types.Message, state: FSMContext):
    """Запись названия агентства"""

    answer = message.text.title()
    await state.update_data(room_agency_name=answer)
    await message.answer(
        '🔻 Напишите своё имя'
    )
    await RoomCallbackStates.next()


@dp.message_handler(state=RoomCallbackStates.R13)
async def entering_room_rialtor_name(message: types.Message, state: FSMContext):
    """Запись имени риелтора и вывод результирующего текста"""

    answer = message.text.title()
    await state.update_data(room_rieltor_name=answer)
    data = await state.get_data()

    # ЗАПИСЬ В БАЗУ
    if not DB_Worker.room_to_db(data):
        await message.answer(
            'К сожаления, в работе бота произошла ошибка. Попробуйте еще раз. '
            + 'Если ошибка повторится, напишите об этом @davletelvir'
        )
    else:
        await message.answer(
            '\n'.join(
                message_texts.room_adding_result_text(data)
            ),
            parse_mode="Markdown"
        )
    await state.finish()


# С ЭТОГО МЕСТА ОПРОС ПО ДОМУ
@dp.callback_query_handler(text='Дом')
async def add_house(callback: types.CallbackQuery, state: FSMContext):
    """Ответ на кнопку добавления дома"""

    await state.update_data(house_reality_category=callback.data)
    await callback.message.edit_text(
        'Приготовьтесь ответить на несколько вопросов про ваш объект '
        + 'недвижимости. 😏 Это займёт не более 2-3х минут.'
        + '\n'
        + '\n🔻 Укажите микрорайон расположения дома:'
        + ''
        + '\n🔻 Если нужного микрорайона/села/деревни нет, напишите @davletelvir, добавлю.',
        reply_markup=keyboards.microregion_keyboard()
    )
    await HouseCallbackStates.H1.set()


@dp.callback_query_handler(
    state=HouseCallbackStates.H1,
    text=[
        'Касёво', 'Восточный 1,2,3,4,5', 'Ротково',
        'Марино', 'Телевышка', 'Лесная поляна',
        'Михайловка', 'Ташкиново', 'Николо-Берёзовка',
        'Кутлинка', 'Новонагаево', 'Актанышбаш',
        'Амзя', 'Карманово', 'Можары', 'Арлан', 'Зубовка',
        'Кариево'
    ]
)
async def entering_house_street_name(
    callback: types.CallbackQuery, state: FSMContext
):
    """Ответ на кнопку выбора мирорайона"""

    await state.update_data(house_microregion=callback.data)
    await callback.message.edit_text(
        '🔻 Напишите название улицы и номер дома (номер - по желанию)'
    )
    await HouseCallbackStates.next()


@dp.message_handler(state=HouseCallbackStates.H2)
async def entering_house_purpose(message: types.Message, state: FSMContext):
    """Ответ на написание названия улицы"""

    answer = message.text.title()
    await state.update_data(house_street_name=answer)
    await message.answer(
        '🔻 Укажите назначение участка',
        reply_markup=keyboards.purpose_choise_keyboard()
    )
    await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H3, text=['ИЖС', 'СНТ, ДНТ', 'ЛПХ']
)
async def entering_house_finish(
    callback: types.CallbackQuery, state: FSMContext
):
    """Ответ на ввод назначения"""

    await state.update_data(house_purpose=callback.data)
    await callback.message.edit_text(
        '🔻 Это завершённое строительство',
        reply_markup=keyboards.yes_no_keyboard(item='house_finish')
    )
    await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H4, text=['yes_house_finish', 'no_house_finish']
)
async def entering_house_material(
    callback: types.CallbackQuery, state: FSMContext
):
    """Ответ на ввод завершённости строительства"""

    if callback.data == 'yes_house_finish':
        await state.update_data(house_finish='Да')
    if callback.data == 'no_house_finish':
        await state.update_data(house_finish='Нет')

    await callback.message.edit_text(
        '🔻 Укажите материал стен дома',
        reply_markup=keyboards.material_choice_keyboard()
    )
    await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H5, text=[
        'Кирпич',
        'Заливной',
        'Блок, облицованный кирпичом',
        'Дерево',
        'Дерево, облицованное кирпичом',
        'Другое'
    ]
)
async def entering_house_gas(
    callback: types.CallbackQuery, state: FSMContext
):
    await state.update_data(house_material=callback.data)
    await callback.message.edit_text(
        '🔻 Укажите степень газификации дома',
        reply_markup=keyboards.gaz_choise_keyboard()
    )
    await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H6, text=[
        'Газифицирован, дом отапливается',
        'Улица газифицировна, дом - нет',
        'Улица не газифицирована'
    ]
)
async def entering_house_waters(
    callback: types.CallbackQuery, state: FSMContext
):
    await state.update_data(house_gaz=callback.data)
    await callback.message.edit_text(
        '🔻 В дома есть вода?',
        reply_markup=keyboards.water_choice_keyboard()
    )
    await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H7, text=[
        'Водоснабжение центральное',
        'Колодец',
        'Вода по улице',
        'Воды нет'
    ]
)
async def entering_house_sauna(
    callback: types.CallbackQuery, state: FSMContext
):
    await state.update_data(house_water=callback.data)
    await callback.message.edit_text(
        '🔻 На териитории участка/в доме есть баня или сауна',
        reply_markup=keyboards.yes_no_keyboard(item='house_sauna')
    )
    await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H8, text=[
        'yes_house_sauna',
        'no_house_sauna'
    ]
)
async def entering_house_garage(
    callback: types.CallbackQuery, state: FSMContext
):
    if callback.data == 'yes_house_sauna':
        await state.update_data(house_sauna='Есть')
    if callback.data == 'no_house_sauna':
        await state.update_data(house_sauna='Нет')

    await callback.message.edit_text(
        '🔻 На териитории участка есть гараж?',
        reply_markup=keyboards.yes_no_keyboard(item='house_garage')
    )
    await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H9, text=[
        'yes_house_garage',
        'no_house_garage'
    ]
)
async def entering_house_fence(
    callback: types.CallbackQuery, state: FSMContext
):
    if callback.data == 'yes_house_garage':
        await state.update_data(house_garage='Есть')
    if callback.data == 'no_house_garage':
        await state.update_data(house_garage='Нет')
    await callback.message.edit_text(
        '🔻 Участок огорожен?',
        reply_markup=keyboards.yes_no_keyboard(item='house_fence')
    )
    await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H10, text=[
        'yes_house_fence',
        'no_house_fence'
    ]
)
async def entering_house_road(
    callback: types.CallbackQuery, state: FSMContext
):
    if callback.data == 'yes_house_fence':
        await state.update_data(house_fence='Есть')
    if callback.data == 'no_house_fence':
        await state.update_data(house_fence='Нет')
    await callback.message.edit_text(
        '🔻 К участку есть проезд?',
        reply_markup=keyboards.road_choice_keyboard()
    )
    await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H11, text=[
        'Асфальт',
        'Неплохая насыпная дорога',
        'Неплохая грунтовая дорога',
        'Бездорожье, затрудняющее проезд'
    ]
)
async def entering_house_area(
    callback: types.CallbackQuery, state: FSMContext
):
    await state.update_data(house_road=callback.data)
    await callback.message.edit_text(
        '🔻 Введите площадь дома, как в указано в свидетельстве или выписке. '
        + 'Используйте разделитель "." для дробной и целой частей.'
    )
    await HouseCallbackStates.next()


@dp.message_handler(state=HouseCallbackStates.H12)
async def entering_house_land_area(message: types.Message, state: FSMContext):
    try:
        answer = float(message.text)
        await state.update_data(house_area=answer)
        await message.answer(
            '🔻 Введите площадь участка в сотках. '
            + '(Цифру в документах умножьте на 100) '
            + 'Используйте разделитель "." для дробной и целой частей.'
        )
        await HouseCallbackStates.next()

    except (ValueError) as e:
        await HouseCallbackStates.H12.set()
        await message.answer(
            '🤔 Вы ошиблись при вводе значения площади.\n\nПлощадь'
            + ' следует вводить цифрами и использовать разделитель "." для '
            + 'дробных значений. Так же НЕ указывайтье единицы измерения. '
            + ''
            + 'Попробуйте ввести значение заново:'
        )
        logging.error(f'{e}')


@dp.message_handler(state=HouseCallbackStates.H13)
async def entering_house_price(message: types.Message, state: FSMContext):
    try:
        answer = float(message.text)
        await state.update_data(house_land_area=answer)
        await message.answer(
            '🔻 Напишите цену.\n\nПросто полную цену цифрами, '
            + 'не сокращая, и без знаков Р, р, ₽, руб. и т.п.\n\nЕсли недвижимость '
            + 'стоит 3400000 рублей, значит так и пишите 3400000'
        )
        await HouseCallbackStates.next()

    except (ValueError) as e:
        await HouseCallbackStates.H13.set()
        await message.answer(
            '🤔 Вы ошиблись при вводе значения площади.\n\nПлощадь'
            + ' следует вводить цифрами и использовать разделитель "." для '
            + 'дробных значений. Так же НЕ указывайтье единицы измерения. '
            + ''
            + 'Попробуйте ввести значение заново:'
        )
        logging.error(f'{e}')


@dp.message_handler(state=HouseCallbackStates.H14)
async def entering_house_description(message: types.Message, state: FSMContext):
    try:
        answer = int(message.text)
        await state.update_data(house_price=answer)
        await message.answer(
            '🔻 Добавьте небольшое описание дома.\n\nПожалуйста, '
            + ' руководствуйтесь принципом "Краткость - сестра таланта" '
            + ' и не дублируйте '
            + 'в описании информацию о доме, такие как площадь, цена и др. '
            + '\n\nТолько кратко, самую суть - состояние.'
        )
        await HouseCallbackStates.next()

    except (ValueError) as e:
        await HouseCallbackStates.H14.set()
        await message.answer(
            '🤔 🤔 Вы ошиблись при вводе значения цены. Цену'
            + ' следует вводить цифрами без разделителя "." '
            + 'и без указания единицы измерения.'
            + ''
            + 'Попробуйте ввести значение заново:'
        )
        logging.error(f'{e}')


@dp.message_handler(state=HouseCallbackStates.H15)
async def entering_house_encumbrance(
    message: types.Message, state: FSMContext
):
    answer = message.text
    await state.update_data(house_description=answer)
    await message.answer(
        '🔻 На доме есть обременение?',
        reply_markup=keyboards.yes_no_keyboard('house_encumbrance')
    )
    await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H16,
    text=['yes_house_encumbrance', 'no_house_encumbrance']
)
async def entering_house_children(
    callback: types.CallbackQuery, state: FSMContext
):
    if callback.data == 'yes_house_encumbrance':
        await state.update_data(house_encumbrance=True)
    if callback.data == 'no_house_encumbrance':
        await state.update_data(house_encumbrance=False)
    await callback.message.edit_text(
        '🔻 В собственности есть дети?',
        reply_markup=keyboards.yes_no_keyboard('house_children')
    )
    await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H17,
    text=['yes_house_children', 'no_house_children']
)
async def entering_house_mortage(
    callback: types.CallbackQuery, state: FSMContext
):
    if callback.data == 'yes_house_children':
        await state.update_data(house_children=True)
    if callback.data == 'no_house_children':
        await state.update_data(house_children=False)
    await callback.message.edit_text(
        '🔻 Дом возможно купить по иптоеке?',
        reply_markup=keyboards.yes_no_keyboard('house_mortage')
    )
    await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H18,
    text=['yes_house_mortage', 'no_house_mortage']
)
async def entering_house_phone_number(
    callback: types.CallbackQuery, state: FSMContext
):
    if callback.data == 'yes_house_mortage':
        await state.update_data(house_mortage=True)
    if callback.data == 'no_house_mortage':
        await state.update_data(house_mortage=False)
    await callback.message.edit_text(
        '🔻 Напишите свой номер '
        + 'телефона в формате 89ххххххххх, по которому с'
        + 'вами можно будет связаться'
    )
    await HouseCallbackStates.next()


@dp.message_handler(state=HouseCallbackStates.H19)
async def entering_house_agency_name(
    message: types.Message, state: FSMContext
):
    if re.match(r"^[0-9]+$", message.text):
        await state.update_data(house_phone_number=message.text)
        await message.answer(
            '🔻 В каком агентстве вы трудитесь?\n\n'
            + 'Если вы частный риелтор, то напишите "Частный"'
        )
        await HouseCallbackStates.next()
    else:
        await message.answer(
            '🔻 Вы ошиблись с вводом номера телефона. '
            + f'Введённый вами номер телефона {message.text} '
            + 'не соответствует формату "89ххххххххх". '
            + '\n'
            + 'Введите просто 11 цифр номера, начиная с 8'
        )
        logging.error('Ошибка при вводе номера телефона')
        await HouseCallbackStates.H19.set()


@dp.message_handler(state=HouseCallbackStates.H20)
async def entering_house_rieltor_name(
    message: types.Message, state: FSMContext
):
    answer = message.text.title()
    await state.update_data(house_agency_name=answer)
    await message.answer(
        '🔻 Напишите своё имя'
    )
    await HouseCallbackStates.next()


@dp.message_handler(state=HouseCallbackStates.H21)
async def house_result_text(message: types.Message, state: FSMContext):
    answer = message.text.title()
    await state.update_data(house_rieltor_name=answer)
    data = await state.get_data()

    # запись в базу
    if not DB_Worker.house_to_db(data):
        await message.answer(
            'К сожаления, в работе бота произошла ошибка. Попробуйте еще раз. '
            + 'Если ошибка повторится, напишите об этом @davletelvir'
        )
    else:
        await message.answer(
            '\n'.join(
                message_texts.house_adding_result_text(data)
            ),
            parse_mode="Markdown"
        )
    await state.finish()


# С ЭТОГО МЕСТА ОПРОС ПО ТАУНХАУСУ
@dp.callback_query_handler(text='Таунхаус')
async def add_townhouse(callback: types.CallbackQuery, state: FSMContext):
    """Ответ на кнопку добавления таунхауса"""

    await state.update_data(townhouse_reality_category=callback.data)
    await callback.message.edit_text(
        'Приготовьтесь ответить на несколько вопросов про ваш объект '
        + 'недвижимости. 😏 Это займёт не более 2-3х минут.'
        + '\n'
        + '\n🔻 Укажите микрорайон расположения таунхауса:'
        + ''
        + '\n🔻 Если нужного микрорайона/села/деревни нет, напишите @davletelvir, добавлю.',
        reply_markup=keyboards.microregion_keyboard()
    )
    await TownHouseCallbackStates.T1.set()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T1,
    text=[
        'Касёво', 'Восточный 1,2,3,4,5', 'Ротково',
        'Марино', 'Телевышка', 'Лесная поляна',
        'Михайловка', 'Ташкиново', 'Николо-Берёзовка',
        'Кутлинка', 'Новонагаево', 'Актанышбаш',
        'Амзя', 'Карманово', 'Можары', 'Арлан', 'Зубовка',
        'Кариево'
    ]
)
async def entering_townhouse_street_name(
    callback: types.CallbackQuery, state: FSMContext
):
    """Ответ на кнопку выбора мирорайона"""

    await state.update_data(townhouse_microregion=callback.data)
    await callback.message.edit_text(
        '🔻 Напишите название улицы и номер дома (номер - по желанию)'
    )
    await TownHouseCallbackStates.next()


@dp.message_handler(state=TownHouseCallbackStates.T2)
async def entering_townhouse_purpose(message: types.Message, state: FSMContext):
    """Ответ на написание названия улицы"""

    answer = message.text.title()
    await state.update_data(townhouse_street_name=answer)
    await message.answer(
        '🔻 Укажите назначение участка',
        reply_markup=keyboards.purpose_choise_keyboard()
    )
    await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T3, text=['ИЖС', 'СНТ, ДНТ', 'ЛПХ']
)
async def entering_townhouse_finish(
    callback: types.CallbackQuery, state: FSMContext
):
    """Ответ на ввод назначения"""

    await state.update_data(townhouse_purpose=callback.data)
    await callback.message.edit_text(
        '🔻 Это завершённое строительство',
        reply_markup=keyboards.yes_no_keyboard(item='townhouse_finish')
    )
    await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T4, text=[
        'yes_townhouse_finish', 'no_townhouse_finish'
    ]
)
async def entering_townhouse_material(
    callback: types.CallbackQuery, state: FSMContext
):
    """Ответ на ввод завершённости строительства"""

    if callback.data == 'yes_townhouse_finish':
        await state.update_data(townhouse_finish='Да')
    if callback.data == 'no_townhouse_finish':
        await state.update_data(townhouse_finish='Нет')

    await callback.message.edit_text(
        '🔻 Укажите материал стен',
        reply_markup=keyboards.material_choice_keyboard()
    )
    await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T5, text=[
        'Кирпич',
        'Заливной',
        'Блок, облицованный кирпичом',
        'Дерево',
        'Дерево, облицованное кирпичом',
        'Другое'
    ]
)
async def entering_townhouse_gas(
    callback: types.CallbackQuery, state: FSMContext
):
    await state.update_data(townhouse_material=callback.data)
    await callback.message.edit_text(
        '🔻 Укажите степень газификации',
        reply_markup=keyboards.gaz_choise_keyboard()
    )
    await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T6, text=[
        'Газифицирован, дом отапливается',
        'Улица газифицировна, дом - нет',
        'Улица не газифицирована'
    ]
)
async def entering_townhouse_waters(
    callback: types.CallbackQuery, state: FSMContext
):
    await state.update_data(townhouse_gaz=callback.data)
    await callback.message.edit_text(
        '🔻 В таунхаус проведена вода?',
        reply_markup=keyboards.water_choice_keyboard()
    )
    await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T7, text=[
        'Водоснабжение центральное',
        'Колодец',
        'Вода по улице',
        'Воды нет'
    ]
)
async def entering_townhouse_sauna(
    callback: types.CallbackQuery, state: FSMContext
):
    await state.update_data(townhouse_water=callback.data)
    await callback.message.edit_text(
        '🔻 На териитории участка или внутри есть баня или сауна',
        reply_markup=keyboards.yes_no_keyboard(item='townhouse_sauna')
    )
    await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T8, text=[
        'yes_townhouse_sauna',
        'no_townhouse_sauna'
    ]
)
async def entering_townhouse_garage(
    callback: types.CallbackQuery, state: FSMContext
):
    if callback.data == 'yes_townhouse_sauna':
        await state.update_data(townhouse_sauna='Есть')
    if callback.data == 'no_townhouse_sauna':
        await state.update_data(townhouse_sauna='Нет')

    await callback.message.edit_text(
        '🔻 На териитории участка есть гараж?',
        reply_markup=keyboards.yes_no_keyboard(item='townhouse_garage')
    )
    await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T9, text=[
        'yes_townhouse_garage',
        'no_townhouse_garage'
    ]
)
async def entering_townhouse_fence(
    callback: types.CallbackQuery, state: FSMContext
):
    if callback.data == 'yes_townhouse_garage':
        await state.update_data(townhouse_garage='Есть')
    if callback.data == 'no_townhouse_garage':
        await state.update_data(townhouse_garage='Нет')
    await callback.message.edit_text(
        '🔻 Участок огорожен?',
        reply_markup=keyboards.yes_no_keyboard(item='townhouse_fence')
    )
    await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T10, text=[
        'yes_townhouse_fence',
        'no_townhouse_fence'
    ]
)
async def entering_townhouse_road(
    callback: types.CallbackQuery, state: FSMContext
):
    if callback.data == 'yes_townhouse_fence':
        await state.update_data(townhouse_fence='Есть')
    if callback.data == 'no_townhouse_fence':
        await state.update_data(townhouse_fence='Нет')
    await callback.message.edit_text(
        '🔻 К участку есть проезд?',
        reply_markup=keyboards.road_choice_keyboard()
    )
    await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T11, text=[
        'Асфальт',
        'Неплохая насыпная дорога',
        'Неплохая грунтовая дорога',
        'Бездорожье, затрудняющее проезд'
    ]
)
async def entering_townhouse_area(
    callback: types.CallbackQuery, state: FSMContext
):
    await state.update_data(townhouse_road=callback.data)
    await callback.message.edit_text(
        '🔻 Введите площадь, как в указано в свидетельстве или выписке. '
        + 'Используйте разделитель "." для дробной и целой частей.'
    )
    await TownHouseCallbackStates.next()


@dp.message_handler(state=TownHouseCallbackStates.T12)
async def entering_townhouse_land_area(message: types.Message, state: FSMContext):
    try:
        answer = float(message.text)
        await state.update_data(townhouse_area=answer)
        await message.answer(
            '🔻 Введите площадь участка в сотках. '
            + '(Цифру в документах умножьте на 100) '
            + 'Используйте разделитель "." для дробной и целой частей.'
        )
        await TownHouseCallbackStates.next()

    except (ValueError) as e:
        await TownHouseCallbackStates.T12.set()
        await message.answer(
            '🤔 Вы ошиблись при вводе значения площади.\n\nПлощадь'
            + ' следует вводить цифрами и использовать разделитель "." для '
            + 'дробных значений. Так же НЕ указывайтье единицы измерения. '
            + ''
            + 'Попробуйте ввести значение заново:'
        )
        logging.error(f'{e}')


@dp.message_handler(state=TownHouseCallbackStates.T13)
async def entering_townhouse_price(message: types.Message, state: FSMContext):
    try:
        answer = float(message.text)
        await state.update_data(townhouse_land_area=answer)
        await message.answer(
            '🔻 Напишите цену.\n\nПросто полную цену цифрами, '
            + 'не сокращая, и без знаков Р, р, ₽, руб. и т.п.\n\nЕсли недвижимость '
            + 'стоит 3400000 рублей, значит так и пишите 3400000'
        )
        await TownHouseCallbackStates.next()

    except (ValueError) as e:
        await TownHouseCallbackStates.T13.set()
        await message.answer(
            '🤔 Вы ошиблись при вводе значения площади.\n\nПлощадь'
            + ' следует вводить цифрами и использовать разделитель "." для '
            + 'дробных значений. Так же НЕ указывайтье единицы измерения. '
            + ''
            + 'Попробуйте ввести значение заново:'
        )
        logging.error(f'{e}')


@dp.message_handler(state=TownHouseCallbackStates.T14)
async def entering_townhouse_description(message: types.Message, state: FSMContext):
    try:
        answer = int(message.text)
        await state.update_data(townhouse_price=answer)
        await message.answer(
            '🔻 Добавьте небольшое описание таунхауса.\n\nПожалуйста, '
            + ' руководствуйтесь принципом "Краткость - сестра таланта" '
            + ' и не дублируйте '
            + 'в описании информацию о таунхаусе, такие как площадь, цена и др. '
            + '\n\nТолько кратко, самую суть - состояние.'
        )
        await TownHouseCallbackStates.next()

    except (ValueError) as e:
        await TownHouseCallbackStates.T14.set()
        await message.answer(
            '🤔 🤔 Вы ошиблись при вводе значения цены. Цену'
            + ' следует вводить цифрами без разделителя "." '
            + 'и без указания единицы измерения.'
            + ''
            + 'Попробуйте ввести значение заново:'
        )
        logging.error(f'{e}')


@dp.message_handler(state=TownHouseCallbackStates.T15)
async def entering_townhouse_encumbrance(
    message: types.Message, state: FSMContext
):
    answer = message.text
    await state.update_data(townhouse_description=answer)
    await message.answer(
        '🔻 На таунхаусе есть обременение?',
        reply_markup=keyboards.yes_no_keyboard('townhouse_encumbrance')
    )
    await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T16,
    text=['yes_townhouse_encumbrance', 'no_townhouse_encumbrance']
)
async def entering_townhouse_children(
    callback: types.CallbackQuery, state: FSMContext
):
    if callback.data == 'yes_townhouse_encumbrance':
        await state.update_data(townhouse_encumbrance=True)
    if callback.data == 'no_townhouse_encumbrance':
        await state.update_data(townhouse_encumbrance=False)
    await callback.message.edit_text(
        '🔻 В собственности есть дети?',
        reply_markup=keyboards.yes_no_keyboard('townhouse_children')
    )
    await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T17,
    text=['yes_townhouse_children', 'no_townhouse_children']
)
async def entering_townhouse_mortage(
    callback: types.CallbackQuery, state: FSMContext
):
    if callback.data == 'yes_townhouse_children':
        await state.update_data(townhouse_children=True)
    if callback.data == 'no_townhouse_children':
        await state.update_data(townhouse_children=False)
    await callback.message.edit_text(
        '🔻 Таунхаусы возможно купить по иптоеке?',
        reply_markup=keyboards.yes_no_keyboard('townhouse_mortage')
    )
    await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T18,
    text=['yes_townhouse_mortage', 'no_townhouse_mortage']
)
async def entering_townhouse_phone_number(
    callback: types.CallbackQuery, state: FSMContext
):
    if callback.data == 'yes_townhouse_mortage':
        await state.update_data(townhouse_mortage=True)
    if callback.data == 'no_townhouse_mortage':
        await state.update_data(townhouse_mortage=False)
    await callback.message.edit_text(
        '🔻 Напишите свой номер '
        + 'телефона в формате 89ххххххххх, по которому с'
        + 'вами можно будет связаться'
    )
    await TownHouseCallbackStates.next()


@dp.message_handler(state=TownHouseCallbackStates.T19)
async def entering_townhouse_agency_name(
    message: types.Message, state: FSMContext
):
    if re.match(r"^[0-9]+$", message.text):
        await state.update_data(townhouse_phone_number=message.text)
        await message.answer(
            '🔻 В каком агентстве вы трудитесь?\n\n'
            + 'Если вы частный риелтор, то напишите "Частный"'
        )
        await TownHouseCallbackStates.next()
    else:
        await message.answer(
            '🔻 Вы ошиблись с вводом номера телефона. '
            + f'Введённый вами номер телефона {message.text} '
            + 'не соответствует формату "89ххххххххх". '
            + '\n'
            + 'Введите просто 11 цифр номера, начиная с 8'
        )
        await TownHouseCallbackStates.T19.set()


@dp.message_handler(state=TownHouseCallbackStates.T20)
async def entering_townhouse_rieltor_name(
    message: types.Message, state: FSMContext
):
    answer = message.text.title()
    await state.update_data(townhouse_agency_name=answer)
    await message.answer(
        '🔻 Напишите своё имя'
    )
    await TownHouseCallbackStates.next()


@dp.message_handler(state=TownHouseCallbackStates.T21)
async def townhouse_result_text(message: types.Message, state: FSMContext):
    answer = message.text.title()
    await state.update_data(townhouse_rieltor_name=answer)
    data = await state.get_data()

    # запись в базу
    if not DB_Worker.townhouse_to_db(data):
        await message.answer(
            'К сожаления, в работе бота произошла ошибка. Попробуйте еще раз. '
            + 'Если ошибка повторится, напишите об этом @davletelvir'
        )
    else:
        await message.answer(
            '\n'.join(
                message_texts.townhouse_adding_result_text(data)
            ),
            parse_mode="Markdown"
        )
    await state.finish()


# С ЭТОГО МЕСТА ОПРОС ПО УЧАСТКУ
@dp.callback_query_handler(text='Участок')
async def add_land(callback: types.CallbackQuery, state: FSMContext):
    """Ответ на кнопку добавления участка"""

    await state.update_data(land_reality_category=callback.data)
    await callback.message.edit_text(
        'Приготовьтесь ответить на несколько вопросов про ваш объект '
        + 'недвижимости. 😏 Это займёт не более 2-3х минут.'
        + '\n'
        + '\n🔻 Укажите микрорайон расположения участка:'
        + ''
        + '\n🔻 Если нужного микрорайона/села/деревни нет, напишите @davletelvir, добавлю.',
        reply_markup=keyboards.microregion_keyboard()
    )
    await LandCallbackStates.L1.set()


@dp.callback_query_handler(
    state=LandCallbackStates.L1,
    text=[
        'Касёво', 'Восточный 1,2,3,4,5', 'Ротково',
        'Марино', 'Телевышка', 'Лесная поляна',
        'Михайловка', 'Ташкиново', 'Николо-Берёзовка',
        'Кутлинка', 'Новонагаево', 'Актанышбаш',
        'Амзя', 'Карманово', 'Можары', 'Арлан', 'Зубовка',
        'Кариево'
    ]
)
async def entering_land_street_name(
    callback: types.CallbackQuery, state: FSMContext
):
    await state.update_data(land_microregion=callback.data)
    await callback.message.edit_text(
        '🔻 Напишите название улицы'
    )
    await LandCallbackStates.next()


@dp.message_handler(state=LandCallbackStates.L2)
async def entering_land_number(message: types.Message, state: FSMContext):

    answer = message.text.title()
    await state.update_data(land_street_name=answer)
    await message.answer(
        '🔻 Напишите номер участка',
    )
    await LandCallbackStates.next()


@dp.message_handler(state=LandCallbackStates.L3)
async def entering_land_purpose(message: types.Message, state: FSMContext):

    answer = message.text.upper()
    await state.update_data(land_number_name=answer)
    await message.answer(
        '🔻 Укажите назначение участка',
        reply_markup=keyboards.purpose_choise_keyboard()
    )
    await LandCallbackStates.next()


@dp.callback_query_handler(
    state=LandCallbackStates.L4,
    text=['ИЖС', 'СНТ, ДНТ', 'ЛПХ']
)
async def entering_land_gas(
    callback: types.CallbackQuery, state: FSMContext
):
    await state.update_data(land_purpose=callback.data)
    await callback.message.edit_text(
        '🔻 По улице проходит газ',
        reply_markup=keyboards.yes_no_keyboard('land_gaz')
    )
    await LandCallbackStates.next()


@dp.callback_query_handler(
    state=LandCallbackStates.L5, text=[
        'yes_land_gaz',
        'no_land_gaz'
    ]
)
async def entering_land_waters(
    callback: types.CallbackQuery, state: FSMContext
):
    if callback.data == 'yes_land_gaz':
        await state.update_data(land_gaz='Да')
    if callback.data == 'no_land_gaz':
        await state.update_data(land_gaz='Нет')
    await callback.message.edit_text(
        '🔻 По улице проходит вода?',
        reply_markup=keyboards.yes_no_keyboard('land_water')
    )
    await LandCallbackStates.next()


@dp.callback_query_handler(
    state=LandCallbackStates.L6, text=[
        'yes_land_water',
        'no_land_water'
    ]
)
async def entering_land_sauna(
    callback: types.CallbackQuery, state: FSMContext
):
    if callback.data == 'yes_land_water':
        await state.update_data(land_water='Да')
    if callback.data == 'no_land_water':
        await state.update_data(land_water='Нет')

    await callback.message.edit_text(
        '🔻 На териитории участка баня или сауна',
        reply_markup=keyboards.yes_no_keyboard(item='land_sauna')
    )
    await LandCallbackStates.next()


@dp.callback_query_handler(
    state=LandCallbackStates.L7, text=[
        'yes_land_sauna',
        'no_land_sauna'
    ]
)
async def entering_land_garage(
    callback: types.CallbackQuery, state: FSMContext
):
    if callback.data == 'yes_land_sauna':
        await state.update_data(land_sauna='Есть')
    if callback.data == 'no_land_sauna':
        await state.update_data(land_sauna='Нет')

    await callback.message.edit_text(
        '🔻 На териитории участка есть гараж?',
        reply_markup=keyboards.yes_no_keyboard(item='land_garage')
    )
    await LandCallbackStates.next()


@dp.callback_query_handler(
    state=LandCallbackStates.L8, text=[
        'yes_land_garage',
        'no_land_garage'
    ]
)
async def entering_land_fence(
    callback: types.CallbackQuery, state: FSMContext
):
    if callback.data == 'yes_land_garage':
        await state.update_data(land_garage='Есть')
    if callback.data == 'no_land_garage':
        await state.update_data(land_garage='Нет')
    await callback.message.edit_text(
        '🔻 Участок огорожен?',
        reply_markup=keyboards.yes_no_keyboard(item='land_fence')
    )
    await LandCallbackStates.next()


@dp.callback_query_handler(
    state=LandCallbackStates.L9, text=[
        'yes_land_fence',
        'no_land_fence'
    ]
)
async def entering_land_road(
    callback: types.CallbackQuery, state: FSMContext
):
    if callback.data == 'yes_land_fence':
        await state.update_data(land_fence='Есть')
    if callback.data == 'no_land_fence':
        await state.update_data(land_fence='Нет')
    await callback.message.edit_text(
        '🔻 К участку есть проезд?',
        reply_markup=keyboards.road_choice_keyboard()
    )
    await LandCallbackStates.next()


@dp.callback_query_handler(
    state=LandCallbackStates.L10, text=[
        'Асфальт',
        'Неплохая насыпная дорога',
        'Неплохая грунтовая дорога',
        'Бездорожье, затрудняющее проезд'
    ]
)
async def entering_land_area(
    callback: types.CallbackQuery, state: FSMContext
):
    await state.update_data(land_road=callback.data)
    await callback.message.edit_text(
        '🔻 Введите площадь участка в сотках. '
        + '(Цифру в документах умножьте на 100) '
        + 'Используйте разделитель "." для дробной и целой частей.'
    )
    await LandCallbackStates.next()


@dp.message_handler(state=LandCallbackStates.L11)
async def entering_land_price(message: types.Message, state: FSMContext):
    try:
        answer = float(message.text)
        await state.update_data(land_area=answer)
        await message.answer(
            '🔻 Напишите цену.\n\nПросто полную цену цифрами, '
            + 'не сокращая, и без знаков Р, р, ₽, руб. и т.п.\n\nЕсли недвижимость '
            + 'стоит 3400000 рублей, значит так и пишите 3400000'
        )
        await LandCallbackStates.next()
    except (ValueError) as e:
        await LandCallbackStates.L11.set()
        await message.answer(
            '🤔 Вы ошиблись при вводе значения площади.\n\nПлощадь'
            + ' следует вводить цифрами и использовать разделитель "." для '
            + 'дробных значений. Так же НЕ указывайтье единицы измерения. '
            + ''
            + '🔻 Попробуйте ввести значение заново:'
        )
        logging.error(f'{e}')


@dp.message_handler(state=LandCallbackStates.L12)
async def entering_land_description(message: types.Message, state: FSMContext):
    try:
        answer = int(message.text)
        await state.update_data(land_price=answer)
        await message.answer(
            '🔻 Добавьте небольшое описание.\n\nПожалуйста, '
            + ' руководствуйтесь принципом "Краткость - сестра таланта" '
            + ' и не дублируйте '
            + 'в описании информацию об участке, такие как площадь, цена и др. '
            + '\n\nТолько кратко, самую суть - состояние.'
        )
        await LandCallbackStates.next()

    except (ValueError) as e:
        await LandCallbackStates.L12.set()
        await message.answer(
            '🤔 🤔 Вы ошиблись при вводе значения цены. Цену'
            + ' следует вводить цифрами без разделителя "." '
            + 'и без указания единицы измерения.'
            + ''
            + '🔻 Попробуйте ввести значение заново:'
        )
        logging.error(f'{e}')


@dp.message_handler(state=LandCallbackStates.L13)
async def entering_land_encumbrance(
    message: types.Message, state: FSMContext
):
    answer = message.text
    await state.update_data(land_description=answer)
    await message.answer(
        '🔻 На объекте есть обременение?',
        reply_markup=keyboards.yes_no_keyboard('land_encumbrance')
    )
    await LandCallbackStates.next()


@dp.callback_query_handler(
    state=LandCallbackStates.L14,
    text=['yes_land_encumbrance', 'no_land_encumbrance']
)
async def entering_land_children(
    callback: types.CallbackQuery, state: FSMContext
):
    if callback.data == 'yes_land_encumbrance':
        await state.update_data(land_encumbrance=True)
    if callback.data == 'no_land_encumbrance':
        await state.update_data(land_encumbrance=False)
    await callback.message.edit_text(
        '🔻 В собственности есть дети?',
        reply_markup=keyboards.yes_no_keyboard('land_children')
    )
    await LandCallbackStates.next()


@dp.callback_query_handler(
    state=LandCallbackStates.L15,
    text=['yes_land_children', 'no_land_children']
)
async def entering_land_mortage(
    callback: types.CallbackQuery, state: FSMContext
):
    if callback.data == 'yes_land_children':
        await state.update_data(land_children=True)
    if callback.data == 'no_land_children':
        await state.update_data(land_children=False)
    await callback.message.edit_text(
        '🔻 Дом возможно купить по иптоеке?',
        reply_markup=keyboards.yes_no_keyboard('land_mortage')
    )
    await LandCallbackStates.next()


@dp.callback_query_handler(
    state=LandCallbackStates.L16,
    text=['yes_land_mortage', 'no_land_mortage']
)
async def entering_land_phone_number(
    callback: types.CallbackQuery, state: FSMContext
):
    if callback.data == 'yes_land_mortage':
        await state.update_data(land_mortage=True)
    if callback.data == 'no_land_mortage':
        await state.update_data(land_mortage=False)
    await callback.message.edit_text(
        '🔻 Напишите свой номер '
        + 'телефона в формате 89ххххххххх, по которому с'
        + 'вами можно будет связаться'
    )
    await LandCallbackStates.next()


@dp.message_handler(state=LandCallbackStates.L17)
async def entering_land_agency_name(
    message: types.Message, state: FSMContext
):
    if re.match(r"^[0-9]+$", message.text):
        await state.update_data(land_phone_number=message.text)
        await message.answer(
            '🔻 В каком агентстве вы трудитесь?\n\n'
            + 'Если вы частный риелтор, то напишите "Частный"'
        )
        await LandCallbackStates.next()
    else:
        await message.answer(
            'Вы ошиблись с вводом номера телефона. '
            + f'Введённый вами номер телефона {message.text} '
            + 'не соответствует формату "89ххххххххх". '
            + '\n'
            + '🔻 Введите просто 11 цифр номера, начиная с 8'
        )
        await LandCallbackStates.L17.set()


@dp.message_handler(state=LandCallbackStates.L18)
async def entering_land_rieltor_name(
    message: types.Message, state: FSMContext
):
    answer = message.text.title()
    await state.update_data(land_agency_name=answer)
    await message.answer(
        '🔻 Напишите своё имя'
    )
    await LandCallbackStates.next()


@dp.message_handler(state=LandCallbackStates.L19)
async def land_result_text(message: types.Message, state: FSMContext):
    answer = message.text.title()
    await state.update_data(land_rieltor_name=answer)
    data = await state.get_data()

    # запись в базу
    if not DB_Worker.land_to_db(data):
        await message.answer(
            'К сожаления, в работе бота произошла ошибка. Попробуйте еще раз. '
            + 'Если ошибка повторится, напишите об этом @davletelvir'
        )
    else:
        await message.answer(
            '\n'.join(
                message_texts.land_adding_result_text(data)
            ),
            parse_mode="Markdown"
        )
    await state.finish()


@dp.message_handler(commands=['myobjects'])
async def my_objects(message: types.Message):
    """Ответ на кнопку просмотра объектов пользователя."""

    await message.answer(
        '🔻 Введи свой номер телефона в формате 89ххххххххх '
        + '(11 цифр номера, начиная с 8-ки)'
    )
    await MyObjectsCallbackStates.MO1.set()


@dp.message_handler(state=MyObjectsCallbackStates.MO1)
async def entering_phone_number_for_searching(
    message: types.Message, state: FSMContext
):
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

    data = {
        'total_count': total_count,
        'apartment_count': apartment_count,
        'room_count': room_count,
        'house_count': house_count,
        'townhouse_count': townhouse_count,
        'land_count': land_count,
    }

    await message.answer(
        message_texts.my_objects_text(data),
        parse_mode="Markdown"
    )
    for item in apartment_queryset:
        await message.answer(
            f'🆔 {item.pk}, 🏡 *{item.room_quantity} к.кв.* '
            + f'{item.street_name} д.{item.number_of_house}, '
            + f'{item.floor} этаж - *{int(item.price)} ₽*',
            parse_mode="Markdown"
        )

    for item in room_queryset:
        await message.answer(
            f'🆔 {item.pk}, 🏡 *Комната* {item.street_name} '
            + f'д.{item.number_of_house}, {item.floor} этаж - *{int(item.price)} ₽*',
            parse_mode="Markdown"
        )

    for item in house_queryset:
        await message.answer(
            f'🆔 {item.pk}, 🏡 *Дом* {item.microregion}, {item.street_name} - *{int(item.price)} ₽*',
            parse_mode="Markdown"
        )

    for item in townhouse_queryset:
        await message.answer(
            f'🆔 {item.pk}, 🏡 *Таунхаус* {item.microregion}, {item.street_name} - *{int(item.price)} ₽*',
            parse_mode="Markdown"
        )

    for item in land_queryset:
        await message.answer(
            f'🆔 {item.pk}, 🏡 *Участок* {item.microregion}, {item.street_name} - {int(item.price)} ₽',
            parse_mode="Markdown"
        )

    await state.finish()


@dp.message_handler(commands=['editprice'])
async def edit_price(message: types.Message):
    """Ответ на кнопку редактирования цены."""

    await message.answer(
        '🔻 Введи свой номер телефона в формате 89ххххххххх '
        + '(11 цифр номера, начиная с 8-ки)'
    )
    await PriceEditCallbackStates.EP1.set()


@dp.message_handler(state=PriceEditCallbackStates.EP1)
async def object_choice_for_editing(
    message: types.Message, state: FSMContext
):
    cond1 = Apartment.objects.filter(phone_number=message.text).exists()
    cond2 = Room.objects.filter(phone_number=message.text).exists()
    cond3 = House.objects.filter(phone_number=message.text).exists()
    cond4 = TownHouse.objects.filter(phone_number=message.text).exists()
    cond5 = Land.objects.filter(phone_number=message.text).exists()

    big_cond = cond1 or cond2 or cond3 or cond4 or cond5

    if re.match(r"^[0-9]+$", message.text) and big_cond:
        await message.answer(
            '🔻 Выберите объект, цену которого вы хотите изменить',
            reply_markup=keyboards.objects_list_keyboard(message.text)
        )
        await PriceEditCallbackStates.next()
    else:
        await message.answer(
            ' Вы ошиблись с вводом номера телефона. '
            + f'Введённый вами номер телефона {message.text} '
            + 'не соответствует формату "89ххххххххх" или такого в базе нет.'
            + '\n\n'
            + '🔻 Введите заново номер телефона'
        )
        await PriceEditCallbackStates.EP1.set()


@dp.callback_query_handler(
    state=PriceEditCallbackStates.EP2
)
async def entering_new_price(
    callback: types.CallbackQuery, state: FSMContext
):
    category = callback.data.split()[1]
    id = callback.data.split()[0]
    await state.update_data(searching_category=category.capitalize())
    await state.update_data(searching_id=id)

    await callback.message.edit_text(
        '🔻 Напишите новую цену.\n\nПолную цену цифрами, '
        + 'не сокращая, и без знаков Р, р, ₽, руб. и т.п.'
    )
    await PriceEditCallbackStates.next()


@dp.message_handler(state=PriceEditCallbackStates.EP3)
async def price_updating_process(
    message: types.Message, state: FSMContext
):
    try:
        data = await state.get_data()
        class_name = Output.str_to_class(data.get('searching_category'))
        queryset = class_name.objects.get(pk=data.get('searching_id'))
        queryset.price = int(message.text)
        queryset.save()
        await message.answer(
            'Сделано!'
        )
        await state.finish()
    except Exception as e:
        await message.answer(
            'Ошибка при вводе цены. Вводимое значение должно '
            + 'быть числом. Не пишите "Р", "р", "руб". '
            + '🔻 Напишите новую цену заново'
        )
        logging.error(
            f'Ошибка при вводе новой цены, {e}'
        )
        await PriceEditCallbackStates.EP3.set()
        await state.finish()

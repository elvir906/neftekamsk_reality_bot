# import datetime as dt
import logging
import os

import django
# import psycopg2
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from baza.answer_messages import message_texts
from baza.models import Apartment, House, Land, Room, TownHouse
from baza.states import CallbackOnStart, RoomCallbackStates
# from baza.users import users
from baza.utils import keyboards
from decouple import config
from django.core.management.base import BaseCommand

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

    answer = message.text
    await state.update_data(street_name=answer)

    await message.answer(
        '🔻 Напишите номер дома в формате "5", "5А" или "91 корп.1'
    )
    await CallbackOnStart.next()


@dp.message_handler(state=CallbackOnStart.Q2)
async def entering_house_number(message: types.Message, state: FSMContext):
    """Запись номера дома. Следующий вопрос """

    answer = message.text
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
            '🔻 Добавьте небольшое описание квартиры.\n\nПожалуйста, не дублируйте '
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

    answer = message.text
    await state.update_data(phone_number=answer)
    await message.answer(
        '🔻 В каком агентстве вы трудитесь?\n\n'
        + 'Если вы частный риелтор, то напишите "Частный"'
    )
    await CallbackOnStart.next()


@dp.message_handler(state=CallbackOnStart.Q12)
async def entering_agency_name(message: types.Message, state: FSMContext):
    """Запись названия агентства"""

    answer = message.text
    await state.update_data(agency_name=answer)
    await message.answer(
        '🔻 Напишите своё имя'
    )
    await CallbackOnStart.next()


@dp.message_handler(state=CallbackOnStart.Q13)
async def entering_rialtor_name(message: types.Message, state: FSMContext):
    """Запись имени риелтора и вывод результирующего текста"""

    answer = message.text
    await state.update_data(rieltor_name=answer)
    data = await state.get_data()
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

    await state.update_data(room_street_name=message.text)
    await message.answer(
        '🔻 Напишите номер дома в формате "5", "5А" или "91 корп.1'
    )
    await RoomCallbackStates.next()


@dp.message_handler(state=RoomCallbackStates.R2)
async def enetering_rooms_house_number(
    message: types.Message, state: FSMContext
):
    """Запись номера дома"""

    await state.update_data(room_house_number=message.text)
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
            '🔻 Добавьте небольшое описание квартиры.\n\nПожалуйста, не дублируйте '
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
        reply_markup=keyboards.yes_no_keyboard('encumbrance')
    )
    await RoomCallbackStates.next()


@dp.callback_query_handler(
    state=RoomCallbackStates.R8,
    text=['yes_encumbrance', 'no_encumbrance']
)
async def entering_room_encumbrance(callback: types.CallbackQuery, state: FSMContext):
    """Запись наличия обременения"""

    if callback.data == 'yes_encumbrance':
        await state.update_data(room_encumbrance=True)
    if callback.data == 'no_encumbrance':
        await state.update_data(room_encumbrance=False)
    await callback.message.edit_text(
        '🔻 В собственности есть дети?',
        reply_markup=keyboards.yes_no_keyboard('children')
    )
    await RoomCallbackStates.next()


@dp.callback_query_handler(
    state=RoomCallbackStates.R9,
    text=['yes_children', 'no_children']
)
async def entering_room_children(callback: types.CallbackQuery, state: FSMContext):
    """Запись наличия детей"""

    if callback.data == 'yes_children':
        await state.update_data(room_children=True)
    if callback.data == 'no_children':
        await state.update_data(room_children=False)
    await callback.message.edit_text(
        '🔻 Недвижимость возможно купить по иптоеке?',
        reply_markup=keyboards.yes_no_keyboard('mortage')
    )
    await RoomCallbackStates.next()


@dp.callback_query_handler(
    state=RoomCallbackStates.R10,
    text=['yes_mortage', 'no_mortage']
)
async def entering_room_mortage(callback: types.CallbackQuery, state: FSMContext):
    """Запись возможности покупки в ипотеку"""

    if callback.data == 'yes_mortage':
        await state.update_data(room_mortage=True)
    if callback.data == 'no_mortage':
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

    answer = message.text
    await state.update_data(room_phone_number=answer)
    await message.answer(
        '🔻 В каком агентстве вы трудитесь?\n\n'
        + 'Если вы частный риелтор, то напишите "Частный"'
    )
    await RoomCallbackStates.next()


@dp.message_handler(state=RoomCallbackStates.R12)
async def entering_room_agency_name(message: types.Message, state: FSMContext):
    """Запись названия агентства"""

    answer = message.text
    await state.update_data(room_agency_name=answer)
    await message.answer(
        '🔻 Напишите своё имя'
    )
    await RoomCallbackStates.next()


@dp.message_handler(state=RoomCallbackStates.R13)
async def entering_room_rialtor_name(message: types.Message, state: FSMContext):
    """Запись имени риелтора и вывод результирующего текста"""

    answer = message.text
    await state.update_data(room_rieltor_name=answer)
    data = await state.get_data()
    await message.answer(
        '\n'.join(
            message_texts.room_adding_result_text(data)
        ),
        parse_mode="Markdown"
    )
    await state.finish()


# С ЭТОГО МЕСТА ОПРОС ПО КОМНАТЕ


    # data = await state.get_data()
    # text = []
    # for i in data:
    #     text.append(f'{data[i]}')
    # print(text)

# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)

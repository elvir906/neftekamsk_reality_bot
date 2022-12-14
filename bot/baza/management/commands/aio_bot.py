import asyncio
import logging
import os
import re

import django
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import (CallbackQuery, ContentType, InputFile, MediaGroup,
                           Message)
from baza.answer_messages import message_texts
from baza.db_worker import DB_Worker
from baza.models import (Apartment, Buyer as BuyerDB, House, Individuals, Land, Room,
                         Subscriptors, TownHouse)
from baza.states import (Buyer, CallbackOnStart, DeleteCallbackStates,
                         HouseCallbackStates, LandCallbackStates,
                         PriceEditCallbackStates, RoomCallbackStates,
                         TownHouseCallbackStates, DeleteBuyer, ObjForBuyer)
from baza.utils import (Output, keyboards,
                        object_city_microregions_for_checking,
                        object_country_microregions_for_checking,
                        object_microregions)
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

# -----------------------------------------------------------------------------
# --------------------УДАЛЕНИЕ ОБЪЕКТА-----------------------------------------
# -----------------------------------------------------------------------------
@dp.message_handler(commands=['deleteobject'])
async def delete_object(message: Message):
    user_id = message.from_user.id

    cond1 = Apartment.objects.filter(user_id=user_id).exists()
    cond2 = Room.objects.filter(user_id=user_id).exists()
    cond3 = House.objects.filter(user_id=user_id).exists()
    cond4 = TownHouse.objects.filter(user_id=user_id).exists()
    cond5 = Land.objects.filter(user_id=user_id).exists()

    big_cond = cond1 or cond2 or cond3 or cond4 or cond5

    if big_cond:
        await message.answer(
            'Выберите объект для удаления:',
            reply_markup=keyboards.objects_list_keyboard(user_id)
        )
        await DeleteCallbackStates.D2.set()
    else:
        await message.answer(
            ' У вас нет объектов в базе'
        )


@dp.callback_query_handler(state=DeleteCallbackStates.D2)
async def deleting_object(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отмена':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        category = callback.data.split()[1]
        id = callback.data.split()[0]
        await state.update_data(searching_category=category)
        await state.update_data(searching_id=id)

        try:
            data = await state.get_data()
            class_name = Output.str_to_class(data.get('searching_category'))
            class_name.objects.filter(pk=data.get('searching_id')).delete()
            await callback.message.answer(
                'Сделано!'
            )
            await state.finish()
        except Exception as e:
            await callback.message.answer(
                'Во время удаления возникла ошибка, попробуйте снова.'
                + 'Если ошибка поторится, напишиет об это м @davletelvir'
            )
            logging.error(
                f'Ошибка удаления объекта, {e}'
            )
            await DeleteCallbackStates.D2.set()

# -----------------------------------------------------------------------------
# --------------------агидель-----------------------------------------
# -----------------------------------------------------------------------------
@dp.message_handler(commands=['aqidel'])
async def history_is_lie(message: Message):
    await message.answer(
        message_texts.aqidel()
    )

# -----------------------------------------------------------------------------
# --------------------старт-----------------------------------------
# -----------------------------------------------------------------------------
@dp.message_handler(commands=['start'])
async def start(message: Message):
    await bot.send_sticker(
                chat_id=message.from_user.id,
                sticker=r"CAACAgIAAxkBAAEG_-hjqHFB5AuVlWSh8UJYzNBdchxvtwACbwAD29t-AAGZW1Coe5OAdCwE"
            )
    await message.answer(message_texts.on.get('start'))

# -----------------------------------------------------------------------------
# --------------------About-----------------------------------------
# -----------------------------------------------------------------------------
@dp.message_handler(commands=['about'])
async def about(message: Message):
    await message.answer(
        '\n'.join(message_texts.on.get('about')),
        parse_mode='markdown'
    )

# -----------------------------------------------------------------------------
# --------------------СТАИСТИКА-----------------------------------------
# -----------------------------------------------------------------------------
@dp.message_handler(commands=['getstatistics'])
async def get_statistics(message: Message):
    await message.answer(message_texts.on.get('statistics'))


# -----------------------------------------------------------------------------
# --------------------ПОИСК ОБЪЕКТА-----------------------------------------
# -----------------------------------------------------------------------------

"""
Раскоментить для платной подписки и нижнюю удалить
Реагирует на частных риелторов
"""
# @dp.message_handler(commands=['searchobjects'])
# async def search_objects(message: Message):
#     """Ответ на кнопку просмотра базы"""

#     individuals = [int(', '.join(
#         user
#     )) for user in Individuals.objects.all().values_list('user_id')]
#     print(individuals)
#     if message.from_id in individuals:
#         await message.answer('Просмотр объектов доступно только по '
#               + 'платной подписке на бот. Свяжитесь с @davletelvir')
#     else:
#         await message.answer(
#             '✏ Выберите один из двух форматов просмотра объектов:\n'
#             + '*Каскадная* - все объекты вываливаются в чат, *с фото*.\n'
#             + '*Карусель* - лаконичное перелистывание, но *без фото*.',
#             reply_markup=keyboards.carousel_or_cascade_keyboard(),
#             parse_mode='Markdown'
#         )

# !!!Закоменьтить перед внедрением платной подписки
# 👇👇👇👇👇


@dp.message_handler(commands=['searchobjects'])
async def search_objects(message: Message):
    photo = InputFile("baza/media/view_form_example.png")
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo,
        caption='✏ Выберите один из двух форматов просмотра объектов:\n'
                + '*Каскадная* - все объекты вываливаются в чат, *с фото*.\n'
                + '*Карусель* - лаконичное перелистывание, но *без фото*.',
                reply_markup=keyboards.carousel_or_cascade_keyboard(),
                parse_mode='Markdown'
        )


@dp.callback_query_handler(text=['cascade', 'carousel'])
async def cascade(callback: CallbackQuery, state: FSMContext):
    """Ответ на кнопку просмотра базы в каскадной форме"""
    await state.reset_data()
    await state.update_data(view_form=callback.data)
    await callback.message.answer(
        '✏ Выберите категорию объектов для поиска',
        reply_markup=keyboards.get_category_keyboard()
    )


"""
Раскоментить для платной подписки и нижнюю удалить
реагирует на подписчиков
"""
# @dp.message_handler(commands=['addobject'])
# async def add_object(message: Message):
#     """Ответ на кнопку обавления объекта"""

#     subscriptors = [int(', '.join(
#         user
#     )) for user in Subscriptors.objects.all().values_list('user_id')]

#     if message.from_id not in subscriptors:
#         await message.answer('Добавление объектов доступно только'
#       + ' по платной подписке на бот. Свяжитесь с @davletelvir')
#     else:
#         await message.answer(
#                 '✏ Что желаете добавить?',
#                 reply_markup=keyboards.add_category_keyboard()
#             )

# !!!Закоменьтить перед внедрением платной подписки
# 👇👇👇👇👇

# -----------------------------------------------------------------------------
# --------------------ДОБАЛЕНИЕ ОБЪЕКТА-----------------------------------------
# -----------------------------------------------------------------------------
@dp.message_handler(commands=['addobject'])
async def add_object(message: Message):
    """Ответ на кнопку обавления объекта"""
    await message.answer(
            '✏ Что желаете добавить?',
            reply_markup=keyboards.add_category_keyboard()
        )

# -----------------------------------------------------------------------------
# --------------------ПОИСК ОБЪЕКТА-----------------------------------------
# -----------------------------------------------------------------------------
@dp.callback_query_handler(text="Квартиры")
async def apartments(callback: CallbackQuery):
    """Ответ на кнопку поиска по квартирам"""

    await callback.message.edit_text(
        '✏ Выберите по количеству комнат',
        reply_markup=keyboards.get_rooms_count_keyboard()
    )


@dp.callback_query_handler(text='Комнаты')
async def rooms(callback: CallbackQuery, state: FSMContext):
    """
    Ответ на кнопку поиска по комнатам
    ПАГИНАЦИЮ комментами разжевал в участках ниже если чо
    """

    query_set = Room.objects.order_by('-pub_date')
    pages_count = query_set.count()
    data = await state.get_data()

    await callback.message.answer(
        f'✳ Вот, что я нашёл по *комнатам* ({pages_count}):',
        parse_mode='Markdown'
    )

    """Вид отображения каскадом"""
    if data.get('view_form') == 'cascade':

        for item in query_set:
            await asyncio.sleep(0.5)
            album = MediaGroup()
            photo_list = item.photo_id
            for photo_id in photo_list:
                if photo_id == photo_list[-1]:
                    album.attach_photo(
                        photo_id,
                        caption=message_texts.room_search_result_text(item=item),
                        parse_mode='Markdown'
                    )
                else:
                    album.attach_photo(photo_id)
            await callback.message.answer_media_group(media=album)

    """Вид отображения каруселью"""
    if data.get('view_form') == 'carousel':
        if query_set:
            page = 1
            await callback.message.answer(
                message_texts.room_search_result_text(
                    item=query_set[page - 1]
                ),
                reply_markup=keyboards.pagination_keyboard(
                    page=page,
                    pages=pages_count,
                    category='room'
                ),
                parse_mode='Markdown'
            )
            await state.update_data(
                page=page,
                pages_count=pages_count,
                query_set=query_set
            )


@dp.callback_query_handler(text=['room_prev', 'room_next'])
async def rooms_next(callback: CallbackQuery, state: FSMContext):
    """ПАГИНАЦИЯ"""
    try:
        data = await state.get_data()
        if callback.data == 'room_prev':
            page = data.get('page') - 1
        elif callback.data == 'room_next':
            page = data.get('page') + 1

        if (page > 0) and (page <= data.get('pages_count')):
            await state.update_data(page=page)
            await callback.message.edit_text(
                message_texts.room_search_result_text(
                    item=data.get('query_set')[page - 1]
                ),
                reply_markup=keyboards.pagination_keyboard(
                    page=page,
                    pages=data.get('pages_count'),
                    category='room'
                ),
                parse_mode='Markdown'
            )
    except IndexError:
        pass
    except ValueError:
        pass


@dp.callback_query_handler(text='Дома')
async def houses(callback: CallbackQuery, state: FSMContext):
    """Ответ на кнопку поиска по домам"""

    query_set = House.objects.order_by('-pub_date')
    pages_count = query_set.count()
    data = await state.get_data()

    await callback.message.answer(
        f'✳ Вот, что я нашёл по *домам* ({pages_count}):',
        parse_mode='Markdown'
    )

    """Вид отображения каскадом"""
    if data.get('view_form') == 'cascade':
        for item in query_set:
            await asyncio.sleep(0.5)
            album = MediaGroup()
            photo_list = item.photo_id
            for photo_id in photo_list:
                if photo_id == photo_list[-1]:
                    album.attach_photo(
                        photo_id,
                        caption=message_texts.house_search_result_text(
                            item=item
                        ),
                        parse_mode='Markdown'
                    )
                else:
                    album.attach_photo(photo_id)
            await callback.message.answer_media_group(media=album)

    """Вид отображения карусель"""
    if data.get('view_form') == 'carousel':
        if query_set:
            page = 1
            await callback.message.answer(
                message_texts.house_search_result_text(
                    item=query_set[page - 1]
                ),
                reply_markup=keyboards.pagination_keyboard(
                    page=page,
                    pages=pages_count,
                    category='house'
                ),
                parse_mode='Markdown'
            )
            await state.update_data(
                page=page,
                pages_count=pages_count,
                query_set=query_set
            )


@dp.callback_query_handler(text=['house_prev', 'house_next'])
async def houses_next(callback: CallbackQuery, state: FSMContext):
    """ПАГИНАЦИЯ"""
    # МАГИЯ!
    try:
        data = await state.get_data()
        if callback.data == 'house_prev':
            page = data.get('page') - 1
        elif callback.data == 'house_next':
            page = data.get('page') + 1

        if (page > 0) and (page <= data.get('pages_count')):
            await state.update_data(page=page)
            await callback.message.edit_text(
                message_texts.house_search_result_text(
                    item=data.get('query_set')[page - 1]
                ),
                reply_markup=keyboards.pagination_keyboard(
                    page=page,
                    pages=data.get('pages_count'),
                    category='house'
                ),
                parse_mode='Markdown'
            )
    except IndexError:
        pass
    except ValueError:
        pass


@dp.callback_query_handler(text='Таунхаусы')
async def townhouses(callback: CallbackQuery, state: FSMContext):
    """Ответ на кнопку поиска по таунхаусам ПАГИНАЦИЯ"""

    query_set = TownHouse.objects.order_by('-pub_date')
    pages_count = query_set.count()
    data = await state.get_data()

    await callback.message.answer(
        f'✳ Вот, что я нашёл по *таунхаусам* ({pages_count}):',
        parse_mode='Markdown'
    )

    """Вид отображения каскадом"""
    if data.get('view_form') == 'cascade':
        for item in query_set:
            await asyncio.sleep(0.5)
            album = MediaGroup()
            photo_list = item.photo_id
            for photo_id in photo_list:
                if photo_id == photo_list[-1]:
                    album.attach_photo(
                        photo_id,
                        caption=message_texts.townhouse_search_result_text(
                            item=item
                        ),
                        parse_mode='Markdown'
                    )
                else:
                    album.attach_photo(photo_id)
            await callback.message.answer_media_group(media=album)

    """Вид отображения каруселью"""
    if data.get('view_form') == 'carousel':
        if query_set:
            page = 1
            await callback.message.answer(
                message_texts.townhouse_search_result_text(
                    item=query_set[page - 1]
                ),
                reply_markup=keyboards.pagination_keyboard(
                    page=page,
                    pages=pages_count,
                    category='townhouse'
                ),
                parse_mode='Markdown'
            )
            await state.update_data(
                page=page,
                pages_count=pages_count,
                query_set=query_set
            )


@dp.callback_query_handler(text=['townhouse_prev', 'townhouse_next'])
async def townhouses_next(callback: CallbackQuery, state: FSMContext):
    """ПАГИНАЦИЯ"""
    try:
        data = await state.get_data()
        if callback.data == 'townhouse_prev':
            page = data.get('page') - 1
        elif callback.data == 'townhouse_next':
            page = data.get('page') + 1

        if (page > 0) and (page <= data.get('pages_count')):
            await state.update_data(page=page)
            await callback.message.edit_text(
                message_texts.townhouse_search_result_text(
                    data.get('query_set')[page - 1]
                ),
                reply_markup=keyboards.pagination_keyboard(
                    page, data.get('pages_count'), 'townhouse'
                ),
                parse_mode='Markdown'
            )
    except IndexError:
        pass
    except ValueError:
        pass


@dp.callback_query_handler(text='Участки')
async def lands(callback: CallbackQuery, state: FSMContext):
    """Ответ на кнопку поиска по участкам ПАГИНАЦИЯ"""

    # подготовка инфы (кверисет) на вывод
    query_set = Land.objects.order_by('-pub_date')
    pages_count = query_set.count()
    data = await state.get_data()

    # дежурная фраза
    await callback.message.answer(
        f'✳ Вот, что я нашёл по *участкам* ({pages_count}):',
        parse_mode='Markdown'
    )

    """Вид отображения каскадом"""
    if data.get('view_form') == 'cascade':
        for item in query_set:
            await asyncio.sleep(0.5)
            album = MediaGroup()
            photo_list = item.photo_id
            for photo_id in photo_list:
                if photo_id == photo_list[-1]:
                    album.attach_photo(
                        photo_id,
                        caption=message_texts.lands_search_result_text(
                            item=item
                        ),
                        parse_mode='Markdown'
                    )
                else:
                    album.attach_photo(photo_id)
            await callback.message.answer_media_group(media=album)

    """вид отображения каруселью"""
    if data.get('view_form') == 'carousel':
        if query_set:
            # установка значения номера страницы на первую
            page = 1
            await callback.message.answer(
                # вывод на экран первого элемента (инфы об объекте) кверисета
                message_texts.lands_search_result_text(
                    item=query_set[page - 1]
                ),
                reply_markup=keyboards.pagination_keyboard(
                    page=page,
                    pages=pages_count,
                    category='land'
                ),
                parse_mode='Markdown'
            )
            await state.update_data(
                # запоминание состояний в FSM для передачи
                # во вторую часть магии
                page=page,
                pages_count=pages_count,
                query_set=query_set
            )


@dp.callback_query_handler(text=['land_prev', 'land_next'])
async def lands_next(callback: CallbackQuery, state: FSMContext):
    """ПАГИНАЦИЯ"""
    # вторая часть МАГИИ!
    try:
        # увеличение/уменьшение переменной номера страницы
        data = await state.get_data()
        if callback.data == 'land_prev':
            page = data.get('page') - 1
        elif callback.data == 'land_next':
            page = data.get('page') + 1

        # чтобы не было отрицательных индексов и перебора
        if (page > 0) and (page <= data.get('pages_count')):

            # запоминание текущего номера страницы
            await state.update_data(page=page)

            await callback.message.edit_text(

                # вывод на экран через кастомный метод
                message_texts.lands_search_result_text(
                    item=data.get('query_set')[page - 1]
                ),
                # кейборд из кастомного метода
                reply_markup=keyboards.pagination_keyboard(
                    page=page,
                    pages=data.get('pages_count'),
                    category='land'
                ),
                parse_mode='Markdown'
            )
    # от греха подальше, хотя не должно быть
    except IndexError:
        pass
    except ValueError:
        pass


@dp.callback_query_handler(text='⏪ Назад')
async def back_button_action(callback: CallbackQuery):
    """Ответ на кнопку НАЗАД при просмотре категорий"""

    await callback.message.edit_text(
        '✏ Выберите категорию объектов для поиска',
        reply_markup=keyboards.get_category_keyboard()
    )


@dp.callback_query_handler(text=[
    '1-комнатные', '2-комнатные',
    '3-комнатные', '4-комнатные',
    '5-комнатные'
])
async def apartment_search_result(
    callback: CallbackQuery,
    state: FSMContext
):
    """Ответ на кнопку просмотра квартир"""

    room_count = callback.data.removesuffix('-комнатные')
    await callback.message.answer(
        f'✳ Вот, что я нашёл по *{room_count}-комнатным*:',
        parse_mode='Markdown',
    )

    data = await state.get_data()
    query_set = Apartment.objects.filter(
        room_quantity=int(room_count)
    ).order_by('-pub_date')

    """Вид отображения каскадом"""
    if data.get('view_form') == 'cascade':
        for item in query_set:
            await asyncio.sleep(0.5)
            album = MediaGroup()
            photo_list = item.photo_id
            for photo_id in photo_list:
                if photo_id == photo_list[-1]:
                    album.attach_photo(
                        photo_id,
                        caption=message_texts.apartments_search_result_text(
                                room_count=room_count,
                                item=item
                            ),
                        parse_mode='Markdown'
                    )
                else:
                    album.attach_photo(photo_id)
            await callback.message.answer_media_group(media=album)

    if data.get('view_form') == 'carousel':
        """Отображение каруселью"""
        pages_count = query_set.count()

        if query_set:
            page = 1
            await callback.message.answer(
                message_texts.apartments_search_result_text(
                    int(room_count),
                    query_set[page - 1]
                ),
                reply_markup=keyboards.pagination_keyboard(
                    page=page,
                    pages=pages_count,
                    category='apartment'
                ),
                parse_mode='Markdown'
            )
            await state.update_data(
                page=page,
                pages_count=pages_count,
                query_set=query_set,
                room_count=room_count
            )


@dp.callback_query_handler(text=['apartment_prev', 'apartment_next'])
async def apartment_next(callback: CallbackQuery, state: FSMContext):
    """ПАГИНАЦИЯ"""
    try:
        data = await state.get_data()
        if callback.data == 'apartment_prev':
            page = data.get('page') - 1
        elif callback.data == 'apartment_next':
            page = data.get('page') + 1

        if (page > 0) and (page <= data.get('pages_count')):

            await state.update_data(page=page)
            await callback.message.edit_text(
                message_texts.apartments_search_result_text(
                    int(data.get('room_count')),
                    data.get('query_set')[page - 1]
                ),
                reply_markup=keyboards.pagination_keyboard(
                    page=page,
                    pages=data.get('pages_count'),
                    category='apartment'
                ),
                parse_mode='Markdown'
            )
    except IndexError:
        pass
    except ValueError:
        pass

# --------------------------------------------------------------------------
# ------------------- ОПРОС ПО КВАРТИРЕ ------------------------------------
# --------------------------------------------------------------------------


@dp.callback_query_handler(text='Квартиру')
async def add_apartment(callback: CallbackQuery, state: FSMContext):
    """Ответ на кнопку добавления квартиры"""

    await state.update_data(reality_category=callback.data)
    await callback.message.edit_text(
        'Приготовьтесь ответить на 13 вопросов про ваш объект '
        + 'недвижимости. 😏 Это займёт не более 2-3х минут.'
        + '\n'
        + '\n✏ Введите количество комнат',
        reply_markup=keyboards.add_rooms_count_keyboard()
    )


@dp.callback_query_handler(text=[
    'add_1_room', 'add_2_room',
    'add_3_room', 'add_4_room',
    'add_5_room'
])
async def entering_room_count(
    callback: CallbackQuery,
    state: FSMContext
):
    """Ответ на нажатие выбора количества комнат при добавлении кв."""

    await state.update_data(room_count=callback.data[4])
    await callback.message.edit_text(
        '✏ Напишите название улицы.\n\n'
        + '🙅‍♂️ Чтобы отменить внесение объекта, напишите "Стоп"'
    )
    await CallbackOnStart.Q1.set()


@dp.message_handler(state=CallbackOnStart.Q1)
async def entering_street_name(
    message: Message,
    state: FSMContext
):
    """Запись названия улицы, следующий вопрос """

    answer = message.text.title()
    if answer == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        await state.update_data(street_name=answer)

        await message.answer(
            '✏ Напишите номер дома в формате 5, 5А или 91 корп.1\n\n'
            + '🙅‍♂️ Чтобы отменить внесение объекта, напишите "Стоп"'
        )
        await CallbackOnStart.next()


@dp.message_handler(state=CallbackOnStart.Q2)
async def entering_house_number(message: Message, state: FSMContext):
    """Запись номера дома. Следующий вопрос """
    answer = message.text
    if answer == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        if '"' in answer:
            formatting_answer = answer.replace('"', '')
            answer = formatting_answer

        if ' ' in answer:
            formatting_answer = answer.replace(' ', '')
            answer = formatting_answer

        await state.update_data(house_number=answer)
        await message.answer(
            '✏ Введите этаж квартиры',
            reply_markup=keyboards.floor_number_or_count_keyboard(
                object='apartment_floor'
            )
        )
        await CallbackOnStart.next()


@dp.callback_query_handler(state=CallbackOnStart.Q3, text=[
    '1_afloor', '2_afloor', '3_afloor', '4_afloor',
    '5_afloor', '6_afloor', '7_afloor', '8_afloor',
    '9_afloor', '10_afloor', '11_afloor', '12_afloor',
    '13_afloor', '14_afloor', '15_afloor', '16_afloor',
    '17_afloor', '18_afloor', 'Отменить внесение объекта'
])
async def entering_floor(callback: CallbackQuery, state: FSMContext):
    """Ответ на кнопку выбора этажа квартиры"""
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        await state.update_data(floor=callback.data.removesuffix('_afloor'))
        await callback.message.edit_text(
            '✏ Введите количество этажей',
            reply_markup=keyboards.floor_number_or_count_keyboard(
                object='apartment_house_floors'
            )
        )
        await CallbackOnStart.next()


@dp.callback_query_handler(state=CallbackOnStart.Q4, text=[
    '1_afloors', '2_afloors', '3_afloors', '4_afloors',
    '5_afloors', '6_afloors', '7_afloors', '8_afloors',
    '9_afloors', '10_afloors', '11_afloors', '12_afloors',
    '13_afloors', '14_afloors', '15_afloors', '16_afloors',
    '17_afloors', '18_afloors', 'Отменить внесение объекта'
])
async def entering_floors(callback: CallbackQuery, state: FSMContext):
    """Ответ на кнопку выбора этажности дома"""
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        await state.update_data(floors=callback.data.removesuffix('_afloors'))

        await callback.message.edit_text(
            '✏ Напишите площадь квартиры, как в'
            + ' указано в свидетельстве или выписке\n\n'
            + '🙅‍♂️ Чтобы отменить внесение объекта, напишите "Стоп"'
        )
        await CallbackOnStart.next()


@dp.message_handler(state=CallbackOnStart.Q5)
async def entering_area(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        try:
            if ',' in message.text:
                formatting_string = message.text.replace(',', '.')
                answer = float(formatting_string)
            else:
                answer = float(message.text)
            await state.update_data(area=answer)
            await message.answer(
                message_texts.on.get('enter_price')
            )
            await CallbackOnStart.next()

        except (ValueError) as e:
            await CallbackOnStart.Q5.set()
            await bot.send_sticker(
                chat_id=message.from_user.id,
                sticker=r"CAACAgIAAxkBAAEG_-ZjqHE6DzrO1BV48O2huiQ8kDVIIQACYwAD29t-AAGMnQU950KD5ywE"
            )
            await message.answer(
                message_texts.on.get('area_entering_error')
            )
            logging.error(f'{e}')


@dp.message_handler(state=CallbackOnStart.Q6)
async def entering_price(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        try:
            answer = int(message.text)
            await state.update_data(price=answer)
            await message.answer(
                message_texts.entering_description_text(category='квартиры')
            )
            await CallbackOnStart.next()

        except (ValueError) as e:
            await CallbackOnStart.Q6.set()
            await bot.send_sticker(
                chat_id=message.from_user.id,
                sticker=r"CAACAgIAAxkBAAEG_-ZjqHE6DzrO1BV48O2huiQ8kDVIIQACYwAD29t-AAGMnQU950KD5ywE"
            )
            await message.answer(
                message_texts.on.get('price_entering_error')
            )
            logging.error(f'{e}')


@dp.message_handler(state=CallbackOnStart.Q7)
async def entering_description(message: Message, state: FSMContext):
    """Запись состояния"""

    answer = message.text
    if answer == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        if len(message.text) <= 200:
            await state.update_data(description=answer)
            await message.answer(
                '✏ На недвижимости есть обременение?',
                reply_markup=keyboards.yes_no_keyboard('encumbrance')
            )
            await CallbackOnStart.next()
        else:
            await message.answer(
                message_texts.character_limit(len(message.text))
            )
            logging.error('Превышение лимита знаков')
            await CallbackOnStart.Q7.set()


@dp.callback_query_handler(
    state=CallbackOnStart.Q8,
    text=['yes_encumbrance', 'no_encumbrance', 'Отменить внесение объекта']
)
async def entering_encumbrance(callback: CallbackQuery, state: FSMContext):
    """Запись наличия обременения"""
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_encumbrance':
            await state.update_data(encumbrance=True)
        if callback.data == 'no_encumbrance':
            await state.update_data(encumbrance=False)
        await callback.message.edit_text(
            '✏ В собственности есть дети?',
            reply_markup=keyboards.yes_no_keyboard('children')
        )
        await CallbackOnStart.next()


@dp.callback_query_handler(
    state=CallbackOnStart.Q9,
    text=['yes_children', 'no_children', 'Отменить внесение объекта']
)
async def entering_children(callback: CallbackQuery, state: FSMContext):
    """Запись наличия детей"""
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_children':
            await state.update_data(children=True)
        if callback.data == 'no_children':
            await state.update_data(children=False)
        await callback.message.edit_text(
            '✏ Недвижимость возможно купить по иптоеке?',
            reply_markup=keyboards.yes_no_keyboard('mortage')
        )
        await CallbackOnStart.next()


@dp.callback_query_handler(
    state=CallbackOnStart.Q10,
    text=['yes_mortage', 'no_mortage', 'Отменить внесение объекта']
)
async def entering_mortage(callback: CallbackQuery, state: FSMContext):
    """Запись возможности покупки в ипотеку"""
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_mortage':
            await state.update_data(mortage=True)
        if callback.data == 'no_mortage':
            await state.update_data(mortage=False)
        await callback.message.edit_text(
            message_texts.on.get('phone_number_entering_text')
        )
        await CallbackOnStart.next()


@dp.message_handler(state=CallbackOnStart.Q11)
async def entering_phone_number(message: Message, state: FSMContext):
    """Запись номера телефона"""
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        if re.match(r"^[0-9]+$", message.text):
            await state.update_data(phone_number=message.text)
            await message.answer(
                message_texts.on.get('agency_entering_text')
            )
            await CallbackOnStart.next()
        else:
            await bot.send_sticker(
                chat_id=message.from_user.id,
                sticker=r"CAACAgIAAxkBAAEG_-ZjqHE6DzrO1BV48O2huiQ8kDVIIQACYwAD29t-AAGMnQU950KD5ywE"
            )
            await message.answer(
                message_texts.phone_number_entering_error(message.text)
            )
            logging.error(f'🧐 Ошибка при вводе номера телефона {message.text}')
            await CallbackOnStart.Q11.set()


@dp.message_handler(state=CallbackOnStart.Q12)
async def entering_agency_name(message: Message, state: FSMContext):
    """Запись названия агентства"""
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        answer = message.text.title()
        await state.update_data(agency_name=answer)
        await message.answer(
            '✏ Напишите своё имя\n\n'
            + '🙅‍♂️ Чтобы отменить внесение объекта, напишите "Стоп"'
        )
        await CallbackOnStart.next()


@dp.message_handler(state=CallbackOnStart.Q13)
async def entering_rieltor_name(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        answer = message.text.title()

        await state.update_data(rieltor_name=answer)
        await message.answer(
            '✏ Загрузите до 6 фото квартиры\n\n'
        )
        await CallbackOnStart.Q14.set()


images = {}


@dp.message_handler(state=CallbackOnStart.Q14, content_types=ContentType.PHOTO)
async def report_photo(message: Message, state: FSMContext):

    global images
    key = str(message.from_user.id)
    images.setdefault(key, [])

    if len(images[key]) == 0:
        images[key].append(message.photo[-1].file_id)
        await message.answer(message_texts.on.get('code_word_text'))
        await CallbackOnStart.Q15.set()
    else:
        images[key].append(message.photo[-1].file_id)


@dp.message_handler(state=CallbackOnStart.Q15)
async def base_updating(message: Message, state: FSMContext):

    await state.update_data(code_word=message.text)

    user_id = message.from_user.id
    photo = images.get(str(user_id))
    images.pop(str(user_id))
    await state.update_data(photo=photo)
    await state.update_data(user_id=user_id)

    data = await state.get_data()

    # ЗАПИСЬ В БАЗУ И выдача
    await asyncio.sleep(2)
    if not DB_Worker.apartment_to_db(data):
        await message.answer(
            message_texts.on.get('sorry_about_error')
        )
    else:
        album = MediaGroup()
        photo_list = data.get('photo')
        for photo_id in photo_list:
            if photo_id == photo_list[-1]:
                album.attach_photo(
                    photo_id,
                    caption='\n'.join(
                        message_texts.apartment_adding_result_text(data)
                    ),
                    parse_mode='Markdown'
                )
            else:
                album.attach_photo(photo_id)
        await message.answer_media_group(media=album)
    await state.finish()


# --------------------------------------------------------------------------
# ------------------- ОПРОС ПО КОМНАТЕ ------------------------------------
# --------------------------------------------------------------------------
@dp.callback_query_handler(text='Комнату')
async def add_room(callback: CallbackQuery, state: FSMContext):
    """Ответ на кнопку добавления квартиры"""

    await state.update_data(room_reality_category=callback.data)
    await callback.message.edit_text(
        'Приготовьтесь ответить на несколько вопросов про ваш объект '
        + 'недвижимости. 😏 Это займёт не более 2-3х минут.'
        + '\n'
        + '\n✏ Напишите название улицы\n\n'
        + '🙅‍♂️ Чтобы отменить внесение объекта, напишите "Стоп"'
    )
    await RoomCallbackStates.R1.set()


@dp.message_handler(state=RoomCallbackStates.R1)
async def enetering_rooms_street_name(
    message: Message, state: FSMContext
):
    """Запись названия улицы комнаты"""
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        await state.update_data(room_street_name=message.text.title())
        await message.answer(
            '✏ Напишите номер дома в формате 5, 5А или 91 корп.1\n\n'
            + '🙅‍♂️ Чтобы отменить внесение объекта, напишите "Стоп"'
        )
        await RoomCallbackStates.next()


@dp.message_handler(state=RoomCallbackStates.R2)
async def enetering_rooms_house_number(
    message: Message, state: FSMContext
):
    """Запись номера дома"""
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        answer = message.text
        if '"' in answer:
            formatting_answer = answer.replace('"', '')
            answer = formatting_answer

        if ' ' in answer:
            formatting_answer = answer.replace(' ', '')
            answer = formatting_answer

        await state.update_data(room_house_number=answer.upper())
        await message.answer(
            '✏ Введите этаж комнаты',
            reply_markup=keyboards.floor_number_or_count_keyboard('room_floor')
        )
        await RoomCallbackStates.next()


@dp.callback_query_handler(state=RoomCallbackStates.R3, text=[
    '1_rfloor', '2_rfloor', '3_rfloor', '4_rfloor',
    '5_rfloor', '6_rfloor', '7_rfloor', '8_rfloor',
    '9_rfloor', '10_rfloor', '11_rfloor', '12_rfloor',
    '13_rfloor', '14_rfloor', '15_rfloor', '16_rfloor',
    '17_rfloor', '18_rfloor', 'Отменить внесение объекта',
])
async def entering_room_floor(callback: CallbackQuery, state: FSMContext):
    """Ответ на кнопку выбора этажа комнаты"""
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        await state.update_data(room_floor=callback.data.removesuffix('_rfloor'))
        await callback.message.edit_text(
            '✏ Введите количество этажей',
            reply_markup=keyboards.floor_number_or_count_keyboard(
                object='room_house_floors'
            )
        )
        await RoomCallbackStates.next()


@dp.callback_query_handler(state=RoomCallbackStates.R4, text=[
    '1_rfloors', '2_rfloors', '3_rfloors', '4_rfloors',
    '5_rfloors', '6_rfloors', '7_rfloors', '8_rfloors',
    '9_rfloors', '10_rfloors', '11_rfloors', '12_rfloors',
    '13_rfloors', '14_rfloors', '15_rfloors', '16_rfloors',
    '17_rfloors', '18_rfloors', 'Отменить внесение объекта',
])
async def entering_room_floors(
    callback: CallbackQuery, state: FSMContext
):
    """Ответ на кнопку выбора этажности дома"""
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        await state.update_data(room_floors=callback.data.removesuffix('_rfloors'))
        await callback.message.edit_text(
            '✏ Введите площадь комнаты, как в указано в свидетельстве или выписке\n\n'
            + '🙅‍♂️ Чтобы отменить внесение объекта, напишите "Стоп"'
        )
        await RoomCallbackStates.next()


@dp.message_handler(state=RoomCallbackStates.R5)
async def enetering_rooms_area(
    message: Message, state: FSMContext
):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        try:
            answer = message.text

            if ',' in message.text:
                formatting_string = message.text.replace(',', '.')
                answer = float(formatting_string)
            else:
                answer = float(message.text)
            await state.update_data(room_area=answer)
            await message.answer(
                message_texts.on.get('enter_price')
            )
            await RoomCallbackStates.next()

        except (ValueError) as e:
            await RoomCallbackStates.R5.set()
            await message.answer(
                message_texts.on.get('area_entering_error')
            )
            logging.error(f'{e}')


@dp.message_handler(state=RoomCallbackStates.R6)
async def entering_room_price(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        try:
            answer = int(message.text)
            await state.update_data(room_price=answer)
            await message.answer(
                message_texts.entering_description_text(category='комнаты')
            )
            await RoomCallbackStates.next()

        except (ValueError) as e:
            await RoomCallbackStates.R6.set()
            await message.answer(
                message_texts.on.get('price_entering_error')
            )
            logging.error(f'{e}')


@dp.message_handler(state=RoomCallbackStates.R7)
async def entering_room_description(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        answer = message.text
        if len(message.text) <= 200:
            await state.update_data(room_description=answer)
            await message.answer(
                '✏ На недвижимости есть обременение?',
                reply_markup=keyboards.yes_no_keyboard(item='room_encumbrance')
                )
            await RoomCallbackStates.next()
        else:
            await message.answer(
                message_texts.character_limit(len(message.text))
            )
            logging.error('Превышение лимита знаков')
            await RoomCallbackStates.R7.set()


@dp.callback_query_handler(
    state=RoomCallbackStates.R8,
    text=['yes_room_encumbrance', 'no_room_encumbrance', 'Отменить внесение объекта']
)
async def entering_room_encumbrance(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_room_encumbrance':
            await state.update_data(room_encumbrance=True)
        if callback.data == 'no_room_encumbrance':
            await state.update_data(room_encumbrance=False)
        await callback.message.edit_text(
            '✏ В собственности есть дети?',
            reply_markup=keyboards.yes_no_keyboard(item='room_children')
        )
        await RoomCallbackStates.next()


@dp.callback_query_handler(
    state=RoomCallbackStates.R9,
    text=['yes_room_children', 'no_room_children', 'Отменить внесение объекта']
)
async def entering_room_children(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_room_children':
            await state.update_data(room_children=True)
        if callback.data == 'no_room_children':
            await state.update_data(room_children=False)
        await callback.message.edit_text(
            '✏ Недвижимость возможно купить по иптоеке?',
            reply_markup=keyboards.yes_no_keyboard(item='room_mortage')
        )
        await RoomCallbackStates.next()


@dp.callback_query_handler(
    state=RoomCallbackStates.R10,
    text=['yes_room_mortage', 'no_room_mortage', 'Отменить внесение объекта']
)
async def entering_room_mortage(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_room_mortage':
            await state.update_data(room_mortage=True)
        if callback.data == 'no_room_mortage':
            await state.update_data(room_mortage=False)
        await callback.message.edit_text(
            message_texts.on.get('phone_number_entering_text')
        )
        await RoomCallbackStates.next()


@dp.message_handler(state=RoomCallbackStates.R11)
async def entering_room_phone_number(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        if re.match(r"^[0-9]+$", message.text):
            await state.update_data(room_phone_number=message.text)
            await message.answer(
                message_texts.on.get('agency_entering_text')
            )
            await RoomCallbackStates.next()
        else:
            await message.answer(
                message_texts.phone_number_entering_error(
                    phone_number=message.text
                )
            )
            logging.error(f'🧐 Ошибка при вводе номера телефона {message.text}')
            await RoomCallbackStates.R11.set()


@dp.message_handler(state=RoomCallbackStates.R12)
async def entering_room_agency_name(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        answer = message.text.title()
        await state.update_data(room_agency_name=answer)
        await message.answer(
            '✏ Напишите своё имя\n\n'
            + '🙅‍♂️ Чтобы отменить внесение объекта, напишите "Стоп"'
        )
        await RoomCallbackStates.next()


@dp.message_handler(state=RoomCallbackStates.R13)
async def entering_room_realtor_name(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        answer = message.text.title()
        global flag
        flag = False
        await state.update_data(room_rieltor_name=answer)
        await message.answer(
            '✏ Загрузите до 6 фото квартиры\n\n'
        )
        await RoomCallbackStates.R14.set()


@dp.message_handler(state=RoomCallbackStates.R14, content_types=ContentType.PHOTO)
async def report_room_photo(message: Message):
    global images
    key = str(message.from_user.id)
    images.setdefault(key, [])

    if len(images[key]) == 0:
        images[key].append(message.photo[-1].file_id)
        await message.answer(message_texts.on.get('code_word_text'))
        await RoomCallbackStates.R15.set()
    else:
        images[key].append(message.photo[-1].file_id)


@dp.message_handler(state=RoomCallbackStates.R15)
async def room_base_updating(message: Message, state: FSMContext):

    await state.update_data(room_code_word=message.text)

    user_id = message.from_user.id
    photo = images.get(str(user_id))
    images.pop(str(user_id))
    await state.update_data(room_photo=photo)
    await state.update_data(room_user_id=user_id)

    data = await state.get_data()

    # ЗАПИСЬ В БАЗУ И выдача
    await asyncio.sleep(2)
    if not DB_Worker.room_to_db(data):
        await message.answer(
            message_texts.on.get('sorry_about_error')
        )
    else:
        album = MediaGroup()
        photo_list = data.get('room_photo')
        for photo_id in photo_list:
            if photo_id == photo_list[-1]:
                album.attach_photo(
                    photo_id,
                    caption='\n'.join(
                        message_texts.room_adding_result_text(data)
                    ),
                    parse_mode='Markdown'
                )
            else:
                album.attach_photo(photo_id)
        await message.answer_media_group(media=album)
    await state.finish()


# --------------------------------------------------------------------------
# ------------------- ОПРОС ПО ДОМУ ------------------------------------
# --------------------------------------------------------------------------
@dp.callback_query_handler(text='Дом')
async def add_house(callback: CallbackQuery, state: FSMContext):
    """Ответ на кнопку добавления дома"""

    await state.update_data(house_reality_category=callback.data)
    await callback.message.edit_text(
        'Приготовьтесь ответить на несколько вопросов про ваш объект '
        + 'недвижимости. 😏 Это займёт не более 2-3х минут.'
        + '\n'
        + '\n✏ Укажите микрорайон расположения дома:'
        + ''
        + '\n✏ Если нужного микрорайона/села/деревни нет, напишите @davletelvir, добавлю.',
        reply_markup=keyboards.microregion_keyboard('object')
    )
    await HouseCallbackStates.H1.set()


@dp.callback_query_handler(
    state=HouseCallbackStates.H1,
    text=object_microregions.append('Отменить внесение объекта')
)
async def entering_house_street_name(
    callback: CallbackQuery, state: FSMContext
):
    """Ответ на кнопку выбора мирорайона"""
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        await state.update_data(house_microregion=callback.data)
        await callback.message.edit_text(
            '✏ Напишите название улицы (и номер - по желанию)\n\n'
            + '🙅‍♂️ Чтобы отменить внесение объекта, напишите "Стоп"'
        )
        await HouseCallbackStates.next()


@dp.message_handler(state=HouseCallbackStates.H2)
async def entering_house_purpose(message: Message, state: FSMContext):
    """Ответ на написание названия улицы"""
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        answer = message.text.title()
        await state.update_data(house_street_name=answer)
        await message.answer(
            '✏ Укажите назначение участка',
            reply_markup=keyboards.purpose_choise_keyboard()
        )
        await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H3, text=[
        'ИЖС',
        'СНТ, ДНТ',
        'ЛПХ',
        'Отменить внесение объекта'
    ]
)
async def entering_house_finish(
    callback: CallbackQuery, state: FSMContext
):
    """Ответ на ввод назначения"""
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        await state.update_data(house_purpose=callback.data)
        await callback.message.edit_text(
            '✏ Это завершённое строительство',
            reply_markup=keyboards.yes_no_keyboard(item='house_finish')
        )
        await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H4, text=[
        'yes_house_finish',
        'no_house_finish',
        'Отменить внесение объекта'
    ]
)
async def entering_house_material(
    callback: CallbackQuery, state: FSMContext
):
    """Ответ на ввод завершённости строительства"""
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_house_finish':
            await state.update_data(house_finish='Да')
        if callback.data == 'no_house_finish':
            await state.update_data(house_finish='Нет')

        await callback.message.edit_text(
            '✏ Укажите материал стен дома',
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
        'Другое',
        'Отменить внесение объекта',
    ]
)
async def entering_house_gas(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        await state.update_data(house_material=callback.data)
        await callback.message.edit_text(
            '✏ Укажите степень газификации дома',
            reply_markup=keyboards.gaz_choise_keyboard()
        )
        await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H6, text=[
        'Газифицирован, дом отапливается',
        'Улица газифицировна, дом - нет',
        'Улица не газифицирована',
        'Отменить внесение объекта',
    ]
)
async def entering_house_waters(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        await state.update_data(house_gaz=callback.data)
        await callback.message.edit_text(
            '✏ В доме есть вода?',
            reply_markup=keyboards.water_choice_keyboard()
        )
        await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H7, text=[
        'Водоснабжение центральное',
        'Колодец',
        'Вода по улице',
        'Воды нет',
        'Отменить внесение объекта',
    ]
)
async def entering_house_sauna(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        await state.update_data(house_water=callback.data)
        await callback.message.edit_text(
            '✏ На териитории участка/в доме есть баня или сауна',
            reply_markup=keyboards.yes_no_keyboard(item='house_sauna')
        )
        await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H8, text=[
        'yes_house_sauna',
        'no_house_sauna',
        'Отменить внесение объекта',
    ]
)
async def entering_house_garage(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_house_sauna':
            await state.update_data(house_sauna='Есть')
        if callback.data == 'no_house_sauna':
            await state.update_data(house_sauna='Нет')

        await callback.message.edit_text(
            '✏ На териитории участка есть гараж?',
            reply_markup=keyboards.yes_no_keyboard(item='house_garage')
        )
        await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H9, text=[
        'yes_house_garage',
        'no_house_garage',
        'Отменить внесение объекта',
    ]
)
async def entering_house_fence(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_house_garage':
            await state.update_data(house_garage='Есть')
        if callback.data == 'no_house_garage':
            await state.update_data(house_garage='Нет')
        await callback.message.edit_text(
            '✏ Участок огорожен?',
            reply_markup=keyboards.yes_no_keyboard(item='house_fence')
        )
        await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H10, text=[
        'yes_house_fence',
        'no_house_fence',
        'Отменить внесение объекта',
    ]
)
async def entering_house_road(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_house_fence':
            await state.update_data(house_fence='Есть')
        if callback.data == 'no_house_fence':
            await state.update_data(house_fence='Нет')
        await callback.message.edit_text(
            '✏ К участку есть проезд?',
            reply_markup=keyboards.road_choice_keyboard()
        )
        await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H11, text=[
        'Асфальт',
        'Неплохая насыпная дорога',
        'Неплохая грунтовая дорога',
        'Бездорожье, затрудняющее проезд',
        'Отменить внесение объекта',
    ]
)
async def entering_house_area(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        await state.update_data(house_road=callback.data)
        await callback.message.edit_text(
            '✏ Введите площадь дома, как в указано в свидетельстве или выписке. '
            + 'Используйте разделитель "." для дробной и целой частей.\n\n'
            + '🙅‍♂️ Чтобы отменить внесение объекта, напишите "Стоп"'
        )
        await HouseCallbackStates.next()


@dp.message_handler(state=HouseCallbackStates.H12)
async def entering_house_land_area(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        try:
            answer = message.text
            if ',' in message.text:
                formatting_string = message.text.replace(',', '.')
                answer = float(formatting_string)
            else:
                answer = float(message.text)
            await state.update_data(house_area=answer)
            await message.answer(
                '✏ Введите площадь участка в сотках. '
                + '(Цифру в документах разделите на 100) '
                + 'Используйте разделитель "." для дробной и целой частей.\n\n'
                + '🙅‍♂️ Чтобы отменить внесение объекта, напишите "Стоп"'
            )
            await HouseCallbackStates.next()

        except (ValueError) as e:
            await HouseCallbackStates.H12.set()
            await message.answer(
                message_texts.on.get('area_entering_error')
            )
            logging.error(f'{e}')


@dp.message_handler(state=HouseCallbackStates.H13)
async def entering_house_price(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        try:
            answer = message.text
            if ',' in message.text:
                formatting_string = message.text.replace(',', '.')
                answer = float(formatting_string)
            else:
                answer = float(message.text)
            await state.update_data(house_land_area=answer)
            await message.answer(
                message_texts.on.get('enter_price')
            )
            await HouseCallbackStates.next()

        except (ValueError) as e:
            await HouseCallbackStates.H13.set()
            await message.answer(
                message_texts.on.get('area_entering_error')
            )
            logging.error(f'{e}')


@dp.message_handler(state=HouseCallbackStates.H14)
async def entering_house_description(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        try:
            answer = int(message.text)
            await state.update_data(house_price=answer)
            await message.answer(
                message_texts.entering_description_text('дома')
            )
            await HouseCallbackStates.next()

        except (ValueError) as e:
            await HouseCallbackStates.H14.set()
            await message.answer(
                message_texts.on.get('price_entering_error')
            )
            logging.error(f'{e}')


@dp.message_handler(state=HouseCallbackStates.H15)
async def entering_house_encumbrance(
    message: Message, state: FSMContext
):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        answer = message.text
        if len(message.text) <= 200:
            await state.update_data(house_description=answer)
            await message.answer(
                '✏ На доме есть обременение?',
                reply_markup=keyboards.yes_no_keyboard('house_encumbrance')
            )
            await HouseCallbackStates.next()
        else:
            await message.answer(
                message_texts.character_limit(len(message.text))
            )
            logging.error('Превышение лимита знаков')
            await HouseCallbackStates.H15.set()


@dp.callback_query_handler(
    state=HouseCallbackStates.H16,
    text=[
        'yes_house_encumbrance',
        'no_house_encumbrance',
        'Отменить внесение объекта',
    ]
)
async def entering_house_children(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_house_encumbrance':
            await state.update_data(house_encumbrance=True)
        if callback.data == 'no_house_encumbrance':
            await state.update_data(house_encumbrance=False)
        await callback.message.edit_text(
            '✏ В собственности есть дети?',
            reply_markup=keyboards.yes_no_keyboard('house_children')
        )
        await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H17,
    text=[
        'yes_house_children',
        'no_house_children',
        'Отменить внесение объекта',
    ]
)
async def entering_house_mortage(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_house_children':
            await state.update_data(house_children=True)
        if callback.data == 'no_house_children':
            await state.update_data(house_children=False)
        await callback.message.edit_text(
            '✏ Дом возможно купить по иптоеке?',
            reply_markup=keyboards.yes_no_keyboard('house_mortage')
        )
        await HouseCallbackStates.next()


@dp.callback_query_handler(
    state=HouseCallbackStates.H18,
    text=[
        'yes_house_mortage',
        'no_house_mortage',
        'Отменить внесение объекта',
    ]
)
async def entering_house_phone_number(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_house_mortage':
            await state.update_data(house_mortage=True)
        if callback.data == 'no_house_mortage':
            await state.update_data(house_mortage=False)
        await callback.message.edit_text(
            message_texts.on.get('phone_number_entering_text')
        )
        await HouseCallbackStates.next()


@dp.message_handler(state=HouseCallbackStates.H19)
async def entering_house_agency_name(
    message: Message, state: FSMContext
):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        if re.match(r"^[0-9]+$", message.text):
            await state.update_data(house_phone_number=message.text)
            await message.answer(
                message_texts.on.get('agency_entering_text')
            )
            await HouseCallbackStates.next()
        else:
            await message.answer(
                message_texts.phone_number_entering_error(message.text)
            )
            logging.error(f'🧐 Ошибка при вводе номера телефона {message.text}')
            await HouseCallbackStates.H19.set()


@dp.message_handler(state=HouseCallbackStates.H20)
async def entering_house_rieltor_name(
    message: Message, state: FSMContext
):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        answer = message.text.title()
        await state.update_data(house_agency_name=answer)
        await message.answer(
            '✏ Напишите своё имя\n\n'
            + '🙅‍♂️ Чтобы отменить внесение объекта, напишите "Стоп"'
        )
        await HouseCallbackStates.next()


@dp.message_handler(state=HouseCallbackStates.H21)
async def house_entering_rieltor_name(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        answer = message.text.title()
        global flag
        flag = False
        await state.update_data(house_rieltor_name=answer)
        await message.answer(
            '✏ Загрузите до 6 фото дома'
        )
        await HouseCallbackStates.H22.set()


@dp.message_handler(state=HouseCallbackStates.H22, content_types=ContentType.PHOTO)
async def house_report_photo(message: Message):
    global images
    key = str(message.from_user.id)
    images.setdefault(key, [])

    if len(images[key]) == 0:
        images[key].append(message.photo[-1].file_id)
        await message.answer(message_texts.on.get('code_word_text'))
        await HouseCallbackStates.H23.set()
    else:
        images[key].append(message.photo[-1].file_id)


@dp.message_handler(state=HouseCallbackStates.H23)
async def house_base_updating(message: Message, state: FSMContext):

    await state.update_data(house_code_word=message.text)

    user_id = message.from_user.id
    photo = images.get(str(user_id))
    images.pop(str(user_id))
    await state.update_data(house_photo=photo)
    await state.update_data(house_user_id=user_id)

    data = await state.get_data()

    # ЗАПИСЬ В БАЗУ И выдача
    await asyncio.sleep(2)
    if not DB_Worker.house_to_db(data):
        await message.answer(
            message_texts.on.get('sorry_about_error')
        )
    else:
        album = MediaGroup()
        photo_list = data.get('house_photo')
        for photo_id in photo_list:
            if photo_id == photo_list[-1]:
                album.attach_photo(
                    photo_id,
                    caption='\n'.join(
                        message_texts.house_adding_result_text(data)
                    ),
                    parse_mode='Markdown'
                )
            else:
                album.attach_photo(photo_id)
        await message.answer_media_group(media=album)
    await state.finish()


# --------------------------------------------------------------------------
# ------------------- ОПРОС ПО ТАУНХАУСУ ------------------------------------
# --------------------------------------------------------------------------
@dp.callback_query_handler(text='Таунхаус')
async def add_townhouse(callback: CallbackQuery, state: FSMContext):
    """Ответ на кнопку добавления таунхауса"""

    await state.update_data(townhouse_reality_category=callback.data)
    await callback.message.edit_text(
        'Приготовьтесь ответить на несколько вопросов про ваш объект '
        + 'недвижимости. 😏 Это займёт не более 2-3х минут.'
        + '\n'
        + '\n✏ Укажите микрорайон расположения таунхауса:'
        + ''
        + '\n✏ Если нужного микрорайона/села/деревни нет, напишите @davletelvir, добавлю.\n\n'
        + '🙅‍♂️ Чтобы отменить внесение объекта, напишите "Стоп"',
        reply_markup=keyboards.microregion_keyboard('object')
    )
    await TownHouseCallbackStates.T1.set()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T1,
    text=object_microregions.append('Отменить внесение объекта')
)
async def entering_townhouse_street_name(
    callback: CallbackQuery, state: FSMContext
):
    """Ответ на кнопку выбора мирорайона"""
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        await state.update_data(townhouse_microregion=callback.data)
        await callback.message.edit_text(
            '✏ Напишите название улицы (и номер дома - по желанию)\n\n'
            + '🙅‍♂️ Чтобы отменить внесение объекта, напишите "Стоп"'
        )
        await TownHouseCallbackStates.next()


@dp.message_handler(state=TownHouseCallbackStates.T2)
async def entering_townhouse_purpose(message: Message, state: FSMContext):
    """Ответ на написание названия улицы"""
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        answer = message.text.title()
        await state.update_data(townhouse_street_name=answer)
        await message.answer(
            '✏ Укажите назначение участка',
            reply_markup=keyboards.purpose_choise_keyboard()
        )
        await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T3, text=[
        'ИЖС',
        'СНТ, ДНТ',
        'ЛПХ',
        'Отменить внесение объекта'
    ]
)
async def entering_townhouse_finish(
    callback: CallbackQuery, state: FSMContext
):
    """Ответ на ввод назначения"""
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        await state.update_data(townhouse_purpose=callback.data)
        await callback.message.edit_text(
            '✏ Это завершённое строительство',
            reply_markup=keyboards.yes_no_keyboard(item='townhouse_finish')
        )
        await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T4, text=[
        'yes_townhouse_finish', 'no_townhouse_finish', 'Отменить внесение объекта',
    ]
)
async def entering_townhouse_material(
    callback: CallbackQuery, state: FSMContext
):
    """Ответ на ввод завершённости строительства"""
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_townhouse_finish':
            await state.update_data(townhouse_finish='Да')
        if callback.data == 'no_townhouse_finish':
            await state.update_data(townhouse_finish='Нет')

        await callback.message.edit_text(
            '✏ Укажите материал стен',
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
        'Другое',
        'Отменить внесение объекта',
    ]
)
async def entering_townhouse_gas(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        await state.update_data(townhouse_material=callback.data)
        await callback.message.edit_text(
            '✏ Укажите степень газификации',
            reply_markup=keyboards.gaz_choise_keyboard()
        )
        await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T6, text=[
        'Газифицирован, дом отапливается',
        'Улица газифицировна, дом - нет',
        'Улица не газифицирована',
        'Отменить внесение объекта',
    ]
)
async def entering_townhouse_waters(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        await state.update_data(townhouse_gaz=callback.data)
        await callback.message.edit_text(
            '✏ В таунхаус проведена вода?',
            reply_markup=keyboards.water_choice_keyboard()
        )
        await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T7, text=[
        'Водоснабжение центральное',
        'Колодец',
        'Вода по улице',
        'Воды нет',
        'Отменить внесение объекта',
    ]
)
async def entering_townhouse_sauna(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        await state.update_data(townhouse_water=callback.data)
        await callback.message.edit_text(
            '✏ На териитории участка или внутри есть баня или сауна',
            reply_markup=keyboards.yes_no_keyboard(item='townhouse_sauna')
        )
        await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T8, text=[
        'yes_townhouse_sauna',
        'no_townhouse_sauna',
        'Отменить внесение объекта',
    ]
)
async def entering_townhouse_garage(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_townhouse_sauna':
            await state.update_data(townhouse_sauna='Есть')
        if callback.data == 'no_townhouse_sauna':
            await state.update_data(townhouse_sauna='Нет')

        await callback.message.edit_text(
            '✏ На териитории участка есть гараж?',
            reply_markup=keyboards.yes_no_keyboard(item='townhouse_garage')
        )
        await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T9, text=[
        'yes_townhouse_garage',
        'no_townhouse_garage',
        'Отменить внесение объекта',
    ]
)
async def entering_townhouse_fence(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_townhouse_garage':
            await state.update_data(townhouse_garage='Есть')
        if callback.data == 'no_townhouse_garage':
            await state.update_data(townhouse_garage='Нет')
        await callback.message.edit_text(
            '✏ Участок огорожен?',
            reply_markup=keyboards.yes_no_keyboard(item='townhouse_fence')
        )
        await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T10, text=[
        'yes_townhouse_fence',
        'no_townhouse_fence',
        'Отменить внесение объекта',
    ]
)
async def entering_townhouse_road(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_townhouse_fence':
            await state.update_data(townhouse_fence='Есть')
        if callback.data == 'no_townhouse_fence':
            await state.update_data(townhouse_fence='Нет')
        await callback.message.edit_text(
            '✏ К участку есть проезд?',
            reply_markup=keyboards.road_choice_keyboard()
        )
        await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T11, text=[
        'Асфальт',
        'Неплохая насыпная дорога',
        'Неплохая грунтовая дорога',
        'Бездорожье, затрудняющее проезд',
        'Отменить внесение объекта',
    ]
)
async def entering_townhouse_area(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        await state.update_data(townhouse_road=callback.data)
        await callback.message.edit_text(
            message_texts.on.get('area_entering_text')
        )
        await TownHouseCallbackStates.next()


@dp.message_handler(state=TownHouseCallbackStates.T12)
async def entering_townhouse_land_area(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        try:
            answer = message.text
            if ',' in message.text:
                formatting_string = message.text.replace(',', '.')
                answer = float(formatting_string)
            else:
                answer = float(message.text)
            await state.update_data(townhouse_area=answer)
            await message.answer(
                '✏ Введите площадь участка в сотках. '
                + '(Цифру в документах разделите на 100) '
                + 'Используйте разделитель "." для дробной и целой частей.\n\n'
                + '🙅‍♂️ Чтобы отменить внесение объекта, напишите "Стоп"'
            )
            await TownHouseCallbackStates.next()

        except (ValueError) as e:
            await TownHouseCallbackStates.T12.set()
            await message.answer(
                message_texts.on.get('area_entering_error')
            )
            logging.error(f'{e}')


@dp.message_handler(state=TownHouseCallbackStates.T13)
async def entering_townhouse_price(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        try:
            answer = message.text
            if ',' in message.text:
                formatting_string = message.text.replace(',', '.')
                answer = float(formatting_string)
            else:
                answer = float(message.text)
            await state.update_data(townhouse_land_area=answer)
            await message.answer(
                message_texts.on.get('enter_price')
            )
            await TownHouseCallbackStates.next()

        except (ValueError) as e:
            await TownHouseCallbackStates.T13.set()
            await message.answer(
                message_texts.on.get('area_entering_error')
            )
            logging.error(f'{e}')


@dp.message_handler(state=TownHouseCallbackStates.T14)
async def entering_townhouse_description(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        try:
            answer = int(message.text)
            await state.update_data(townhouse_price=answer)
            await message.answer(
                message_texts.entering_description_text('таунхауса')
            )
            await TownHouseCallbackStates.next()

        except (ValueError) as e:
            await TownHouseCallbackStates.T14.set()
            await message.answer(
                message_texts.on.get('price_entering_error')
            )
            logging.error(f'{e}')


@dp.message_handler(state=TownHouseCallbackStates.T15)
async def entering_townhouse_encumbrance(
    message: Message, state: FSMContext
):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        answer = message.text
        if len(message.text) <= 200:
            await state.update_data(townhouse_description=answer)
            await message.answer(
                '✏ На таунхаусе есть обременение?',
                reply_markup=keyboards.yes_no_keyboard('townhouse_encumbrance')
            )
            await TownHouseCallbackStates.next()
        else:
            await message.answer(
                message_texts.character_limit(len(message.text))
            )
            logging.error('Превышение лимита знаков')
            await TownHouseCallbackStates.T15.set()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T16,
    text=[
        'yes_townhouse_encumbrance',
        'no_townhouse_encumbrance',
        'Отменить внесение объекта',
    ]
)
async def entering_townhouse_children(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_townhouse_encumbrance':
            await state.update_data(townhouse_encumbrance=True)
        if callback.data == 'no_townhouse_encumbrance':
            await state.update_data(townhouse_encumbrance=False)
        await callback.message.edit_text(
            '✏ В собственности есть дети?',
            reply_markup=keyboards.yes_no_keyboard('townhouse_children')
        )
        await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T17,
    text=[
        'yes_townhouse_children',
        'no_townhouse_children',
        'Отменить внесение объекта',
    ]
)
async def entering_townhouse_mortage(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_townhouse_children':
            await state.update_data(townhouse_children=True)
        if callback.data == 'no_townhouse_children':
            await state.update_data(townhouse_children=False)
        await callback.message.edit_text(
            '✏ Таунхаусы возможно купить по иптоеке?',
            reply_markup=keyboards.yes_no_keyboard('townhouse_mortage')
        )
        await TownHouseCallbackStates.next()


@dp.callback_query_handler(
    state=TownHouseCallbackStates.T18,
    text=[
        'yes_townhouse_mortage',
        'no_townhouse_mortage',
        'Отменить внесение объекта',
    ]
)
async def entering_townhouse_phone_number(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_townhouse_mortage':
            await state.update_data(townhouse_mortage=True)
        if callback.data == 'no_townhouse_mortage':
            await state.update_data(townhouse_mortage=False)
        await callback.message.edit_text(
            message_texts.on.get('phone_number_entering_text')
        )
        await TownHouseCallbackStates.next()


@dp.message_handler(state=TownHouseCallbackStates.T19)
async def entering_townhouse_agency_name(
    message: Message, state: FSMContext
):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        if re.match(r"^[0-9]+$", message.text):
            await state.update_data(townhouse_phone_number=message.text)
            await message.answer(
                message_texts.on.get('agency_entering_text')
            )
            await TownHouseCallbackStates.next()
        else:
            await message.answer(
                message_texts.phone_number_entering_error(message.text)
            )
            logging.error(f'🧐 Ошибка при вводе номера телефона {message.text}')
            await TownHouseCallbackStates.T19.set()


@dp.message_handler(state=TownHouseCallbackStates.T20)
async def entering_townhouse_rieltor_name(
    message: Message, state: FSMContext
):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        answer = message.text.title()
        await state.update_data(townhouse_agency_name=answer)
        await message.answer(
            '✏ Напишите своё имя\n\n'
            + '🙅‍♂️ Чтобы отменить внесение объекта, напишите "Стоп"'
        )
        await TownHouseCallbackStates.next()


@dp.message_handler(state=TownHouseCallbackStates.T21)
async def townhous_upload_photos(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        answer = message.text.title()
        global flag
        flag = False
        await state.update_data(townhouse_rieltor_name=answer)
        await message.answer(
            '✏ Загрузите до 6 фото таунхауса'
        )
        await TownHouseCallbackStates.T22.set()


@dp.message_handler(state=TownHouseCallbackStates.T22, content_types=ContentType.PHOTO)
async def townhouse_report_photo(message: Message):
    global images
    key = str(message.from_user.id)
    images.setdefault(key, [])

    if len(images[key]) == 0:
        images[key].append(message.photo[-1].file_id)
        await message.answer(message_texts.on.get('code_word_text'))
        await TownHouseCallbackStates.T23.set()
    else:
        images[key].append(message.photo[-1].file_id)


@dp.message_handler(state=TownHouseCallbackStates.T23)
async def townhouse_base_updating(message: Message, state: FSMContext):

    await state.update_data(townhouse_code_word=message.text)

    user_id = message.from_user.id
    photo = images.get(str(user_id))
    images.pop(str(user_id))
    await state.update_data(townhouse_photo=photo)
    await state.update_data(townhouse_user_id=user_id)

    data = await state.get_data()

    # ЗАПИСЬ В БАЗУ И выдача
    await asyncio.sleep(2)
    if not DB_Worker.townhouse_to_db(data):
        await message.answer(
            message_texts.on.get('sorry_about_error')
        )
    else:
        album = MediaGroup()
        photo_list = data.get('townhouse_photo')
        for photo_id in photo_list:
            if photo_id == photo_list[-1]:
                album.attach_photo(
                    photo_id,
                    caption='\n'.join(
                        message_texts.townhouse_adding_result_text(data)
                    ),
                    parse_mode='Markdown'
                )
            else:
                album.attach_photo(photo_id)
        await message.answer_media_group(media=album)
    await state.finish()


# --------------------------------------------------------------------------
# ------------------- ОПРОС ПО УЧАСТКУ ------------------------------------
# --------------------------------------------------------------------------
@dp.callback_query_handler(text='Участок')
async def add_land(callback: CallbackQuery, state: FSMContext):
    """Ответ на кнопку добавления участка"""

    await state.update_data(land_reality_category=callback.data)
    await callback.message.edit_text(
        'Приготовьтесь ответить на несколько вопросов про ваш объект '
        + 'недвижимости. 😏 Это займёт не более 2-3х минут.'
        + '\n'
        + '\n✏ Укажите микрорайон расположения участка:'
        + ''
        + '\n✏ Если нужного микрорайона/села/деревни нет, напишите @davletelvir, добавлю.\n\n'
        + '🙅‍♂️ Чтобы отменить внесение объекта, напишите "Стоп"',
        reply_markup=keyboards.microregion_keyboard('object')
    )
    await LandCallbackStates.L1.set()


@dp.callback_query_handler(
    state=LandCallbackStates.L1,
    text=object_microregions.append('Отменить внесение объекта')
)
async def entering_land_street_name(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        await state.update_data(land_microregion=callback.data)
        await callback.message.edit_text(
            '✏ Напишите название улицы\n\n'
            + '🙅‍♂️ Чтобы отменить внесение объекта, напишите "Стоп"'
        )
        await LandCallbackStates.next()


@dp.message_handler(state=LandCallbackStates.L2)
async def entering_land_number(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        answer = message.text.title()
        await state.update_data(land_street_name=answer)
        await message.answer(
            '✏ Напишите номер участка\n\n'
            + '🙅‍♂️ Чтобы отменить внесение объекта, напишите "Стоп"',
        )
        await LandCallbackStates.next()


@dp.message_handler(state=LandCallbackStates.L3)
async def entering_land_purpose(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        answer = message.text
        if '"' in answer:
            formatting_answer = answer.replace('"', '')
            answer = formatting_answer

        if ' ' in answer:
            formatting_answer = answer.replace(' ', '')
            answer = formatting_answer

        answer = answer.upper()
        await state.update_data(land_number_name=answer)
        await message.answer(
            '✏ Укажите назначение участка',
            reply_markup=keyboards.purpose_choise_keyboard()
        )
        await LandCallbackStates.next()


@dp.callback_query_handler(
    state=LandCallbackStates.L4,
    text=['ИЖС', 'СНТ, ДНТ', 'ЛПХ', 'Отменить внесение объекта']
)
async def entering_land_gas(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        await state.update_data(land_purpose=callback.data)
        await callback.message.edit_text(
            '✏ По улице проходит газ',
            reply_markup=keyboards.yes_no_keyboard('land_gaz')
        )
        await LandCallbackStates.next()


@dp.callback_query_handler(
    state=LandCallbackStates.L5, text=[
        'yes_land_gaz',
        'no_land_gaz',
        'Отменить внесение объекта'
    ]
)
async def entering_land_waters(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_land_gaz':
            await state.update_data(land_gaz='Да')
        if callback.data == 'no_land_gaz':
            await state.update_data(land_gaz='Нет')
        await callback.message.edit_text(
            '✏ По улице проходит вода?',
            reply_markup=keyboards.yes_no_keyboard('land_water')
        )
        await LandCallbackStates.next()


@dp.callback_query_handler(
    state=LandCallbackStates.L6, text=[
        'yes_land_water',
        'no_land_water',
        'Отменить внесение объекта'
    ]
)
async def entering_land_sauna(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_land_water':
            await state.update_data(land_water='Да')
        if callback.data == 'no_land_water':
            await state.update_data(land_water='Нет')

        await callback.message.edit_text(
            '✏ На териитории участка баня или сауна',
            reply_markup=keyboards.yes_no_keyboard(item='land_sauna')
        )
        await LandCallbackStates.next()


@dp.callback_query_handler(
    state=LandCallbackStates.L7, text=[
        'yes_land_sauna',
        'no_land_sauna',
        'Отменить внесение объекта'
    ]
)
async def entering_land_garage(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_land_sauna':
            await state.update_data(land_sauna='Есть')
        if callback.data == 'no_land_sauna':
            await state.update_data(land_sauna='Нет')

        await callback.message.edit_text(
            '✏ На териитории участка есть гараж?',
            reply_markup=keyboards.yes_no_keyboard(item='land_garage')
        )
        await LandCallbackStates.next()


@dp.callback_query_handler(
    state=LandCallbackStates.L8, text=[
        'yes_land_garage',
        'no_land_garage',
        'Отменить внесение объекта'
    ]
)
async def entering_land_fence(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_land_garage':
            await state.update_data(land_garage='Есть')
        if callback.data == 'no_land_garage':
            await state.update_data(land_garage='Нет')
        await callback.message.edit_text(
            '✏ Участок огорожен?',
            reply_markup=keyboards.yes_no_keyboard(item='land_fence')
        )
        await LandCallbackStates.next()


@dp.callback_query_handler(
    state=LandCallbackStates.L9, text=[
        'yes_land_fence',
        'no_land_fence',
        'Отменить внесение объекта'
    ]
)
async def entering_land_road(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_land_fence':
            await state.update_data(land_fence='Есть')
        if callback.data == 'no_land_fence':
            await state.update_data(land_fence='Нет')
        await callback.message.edit_text(
            '✏ К участку есть проезд?',
            reply_markup=keyboards.road_choice_keyboard()
        )
        await LandCallbackStates.next()


@dp.callback_query_handler(
    state=LandCallbackStates.L10, text=[
        'Асфальт',
        'Неплохая насыпная дорога',
        'Неплохая грунтовая дорога',
        'Бездорожье, затрудняющее проезд',
        'Отменить внесение объекта'
    ]
)
async def entering_land_area(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        await state.update_data(land_road=callback.data)
        await callback.message.edit_text(
            '✏ Введите площадь участка в сотках. '
            + '(Цифру в документах разделите на 100) '
            + 'Используйте разделитель "." для дробной и целой частей.'
        )
        await LandCallbackStates.next()


@dp.message_handler(state=LandCallbackStates.L11)
async def entering_land_price(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        try:
            answer = message.text
            if ',' in message.text:
                formatting_string = message.text.replace(',', '.')
                answer = float(formatting_string)
            else:
                answer = float(message.text)
            await state.update_data(land_area=answer)
            await message.answer(
                message_texts.on.get('enter_price')
            )
            await LandCallbackStates.next()
        except (ValueError) as e:
            await LandCallbackStates.L11.set()
            await message.answer(
                message_texts.on.get('area_entering_error')
            )
            logging.error(f'{e}')


@dp.message_handler(state=LandCallbackStates.L12)
async def entering_land_description(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        try:
            answer = int(message.text)
            await state.update_data(land_price=answer)
            await message.answer(
                message_texts.entering_description_text('участка')
            )
            await LandCallbackStates.next()

        except (ValueError) as e:
            await LandCallbackStates.L12.set()
            await message.answer(
                message_texts.on.get('price_entering_error')
            )
            logging.error(f'{e}')


@dp.message_handler(state=LandCallbackStates.L13)
async def entering_land_encumbrance(
    message: Message, state: FSMContext
):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        answer = message.text
        if len(message.text) <= 200:
            await state.update_data(land_description=answer)
            await message.answer(
                '✏ На объекте есть обременение?',
                reply_markup=keyboards.yes_no_keyboard('land_encumbrance')
            )
            await LandCallbackStates.next()
        else:
            await message.answer(
                message_texts.character_limit(len(message.text))
            )
            logging.error('Превышение лимита знаков')
            await LandCallbackStates.L13.set()


@dp.callback_query_handler(
    state=LandCallbackStates.L14,
    text=[
        'yes_land_encumbrance',
        'no_land_encumbrance',
        'Отменить внесение объекта'
    ]
)
async def entering_land_children(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_land_encumbrance':
            await state.update_data(land_encumbrance=True)
        if callback.data == 'no_land_encumbrance':
            await state.update_data(land_encumbrance=False)
        await callback.message.edit_text(
            '✏ В собственности есть дети?',
            reply_markup=keyboards.yes_no_keyboard('land_children')
        )
        await LandCallbackStates.next()


@dp.callback_query_handler(
    state=LandCallbackStates.L15,
    text=[
        'yes_land_children',
        'no_land_children',
        'Отменить внесение объекта'
    ]
)
async def entering_land_mortage(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_land_children':
            await state.update_data(land_children=True)
        if callback.data == 'no_land_children':
            await state.update_data(land_children=False)
        await callback.message.edit_text(
            '✏ Дом возможно купить по иптоеке?',
            reply_markup=keyboards.yes_no_keyboard('land_mortage')
        )
        await LandCallbackStates.next()


@dp.callback_query_handler(
    state=LandCallbackStates.L16,
    text=[
        'yes_land_mortage',
        'no_land_mortage',
        'Отменить внесение объекта'
    ]
)
async def entering_land_phone_number(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отменить внесение объекта':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        if callback.data == 'yes_land_mortage':
            await state.update_data(land_mortage=True)
        if callback.data == 'no_land_mortage':
            await state.update_data(land_mortage=False)
        await callback.message.edit_text(
            message_texts.on.get('phone_number_entering_text')
        )
        await LandCallbackStates.next()


@dp.message_handler(state=LandCallbackStates.L17)
async def entering_land_agency_name(
    message: Message, state: FSMContext
):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        if re.match(r"^[0-9]+$", message.text):
            await state.update_data(land_phone_number=message.text)
            await message.answer(
                message_texts.on.get('agency_entering_text')
            )
            await LandCallbackStates.next()
        else:
            await message.answer(
                message_texts.phone_number_entering_error(message.text)
            )
            logging.error(f'🧐 Ошибка при вводе номера телефона {message.text}')
            await LandCallbackStates.L17.set()


@dp.message_handler(state=LandCallbackStates.L18)
async def entering_land_rieltor_name(
    message: Message, state: FSMContext
):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        answer = message.text.title()
        await state.update_data(land_agency_name=answer)
        await message.answer(
            '✏ Напишите своё имя\n\n'
            + '🙅‍♂️ Чтобы отменить внесение объекта, напишите "Стоп"'
        )
        await LandCallbackStates.next()


@dp.message_handler(state=LandCallbackStates.L19)
async def land_photo_upload(
    message: Message, state: FSMContext
):
    if message.text == 'Стоп':
        await message.answer(
            'Действие отменено'
        )
        await state.finish()
    else:
        answer = message.text.title()
        global flag
        flag = False
        await state.update_data(land_rieltor_name=answer)
        await message.answer(
            '✏ Загрузите до 6 фото участка. '
        )
        await LandCallbackStates.L20.set()


@dp.message_handler(state=LandCallbackStates.L20, content_types=ContentType.PHOTO)
async def land_report_photo(message: Message):
    global images
    key = str(message.from_user.id)
    images.setdefault(key, [])

    if len(images[key]) == 0:
        images[key].append(message.photo[-1].file_id)
        await message.answer(message_texts.on.get('code_word_text'))
        await LandCallbackStates.L21.set()
    else:
        images[key].append(message.photo[-1].file_id)


@dp.message_handler(state=LandCallbackStates.L21)
async def land_base_updating(message: Message, state: FSMContext):

    await state.update_data(land_code_word=message.text)

    user_id = message.from_user.id
    photo = images.get(str(user_id))
    images.pop(str(user_id))
    await state.update_data(land_photo=photo)
    await state.update_data(land_user_id=user_id)

    data = await state.get_data()

    # ЗАПИСЬ В БАЗУ И выдача
    await asyncio.sleep(2)
    if not DB_Worker.land_to_db(data):
        await message.answer(
            message_texts.on.get('sorry_about_error')
        )
    else:
        album = MediaGroup()
        photo_list = data.get('land_photo')
        for photo_id in photo_list:
            if photo_id == photo_list[-1]:
                album.attach_photo(
                    photo_id,
                    caption='\n'.join(
                        message_texts.land_adding_result_text(data)
                    ),
                    parse_mode='Markdown'
                )
            else:
                album.attach_photo(photo_id)
        await message.answer_media_group(media=album)
    await state.finish()

# -----------------------------------------------------------------------------
# -------------- МОИ ОБЪЕКТЫ --------------------------------------------------
# -----------------------------------------------------------------------------
@dp.message_handler(commands=['myobjects'])
async def entering_phone_number_for_searching(message: Message):
    apartment_queryset = Apartment.objects.filter(user_id=message.from_user.id)
    room_queryset = Room.objects.filter(user_id=message.from_user.id)
    house_queryset = House.objects.filter(user_id=message.from_user.id)
    townhouse_queryset = TownHouse.objects.filter(user_id=message.from_user.id)
    land_queryset = Land.objects.filter(user_id=message.from_user.id)

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
        parse_mode='Markdown'
    )
    for item in apartment_queryset:
        await message.answer(
            f'🆔 {item.pk}, 🏡 *{item.room_quantity} к.кв.* '
            + f'{item.street_name} д.{item.number_of_house}, '
            + f'{item.floor} этаж - *{int(item.price)} ₽*',
            parse_mode='Markdown'
        )

    for item in room_queryset:
        await message.answer(
            f'🆔 {item.pk}, 🏡 *Комната* {item.street_name} '
            + f'д.{item.number_of_house}, {item.floor} этаж - *{int(item.price)} ₽*',
            parse_mode='Markdown'
        )

    for item in house_queryset:
        await message.answer(
            f'🆔 {item.pk}, 🏡 *Дом* {item.microregion}, {item.street_name} - *{int(item.price)} ₽*',
            parse_mode='Markdown'
        )

    for item in townhouse_queryset:
        await message.answer(
            f'🆔 {item.pk}, 🏡 *Таунхаус* {item.microregion}, {item.street_name} - *{int(item.price)} ₽*',
            parse_mode='Markdown'
        )

    for item in land_queryset:
        await message.answer(
            f'🆔 {item.pk}, 🏡 *Участок* {item.microregion}, {item.street_name} - *{int(item.price)} ₽*',
            parse_mode='Markdown'
        )

# -----------------------------------------------------------------------------
# -------------- РЕДАКТИРОВНАИЕ ЦЕНЫ-------------------------------------------
# -----------------------------------------------------------------------------
@dp.message_handler(commands=['editprice'])
async def edit_price(message: Message):
    """Ответ на кнопку редактирования цены."""
    user_id = message.from_user.id

    cond1 = Apartment.objects.filter(user_id=user_id).exists()
    cond2 = Room.objects.filter(user_id=user_id).exists()
    cond3 = House.objects.filter(user_id=user_id).exists()
    cond4 = TownHouse.objects.filter(user_id=user_id).exists()
    cond5 = Land.objects.filter(user_id=user_id).exists()

    big_cond = cond1 or cond2 or cond3 or cond4 or cond5

    # if re.match(r"^[0-9]+$", message.text) and big_cond:
    if big_cond:
        await message.answer(
            '✏ Выберите объект, цену которого вы хотите изменить',
            reply_markup=keyboards.objects_list_keyboard(user_id)
        )
        await PriceEditCallbackStates.EP2.set()
    else:
        await message.answer(
            ' У вас нет объектов в базе'
        )


@dp.callback_query_handler(
    state=PriceEditCallbackStates.EP2
)
async def entering_new_price(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отмена':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        category = callback.data.split()[1]
        id = callback.data.split()[0]
        await state.update_data(searching_category=category)
        await state.update_data(searching_id=id)

        await callback.message.edit_text(
            '✏ Напишите новую цену.\n\nПолную цену цифрами, '
            + 'не сокращая, и без знаков Р, р, ₽, руб. и т.п.'
        )
        await PriceEditCallbackStates.next()


@dp.message_handler(state=PriceEditCallbackStates.EP3)
async def price_updating_process(
    message: Message, state: FSMContext
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
            'Ошибка при вводе цены. \n\nВводимое значение должно '
            + 'быть числом. Не пишите "Р", "р", "руб". '
            + '\n\n✏ Напишите новую цену заново'
        )
        logging.error(
            f'Ошибка при вводе новой цены, {e}'
        )
        await PriceEditCallbackStates.EP3.set()


@dp.callback_query_handler(text=['Отменить внесение объекта'])
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_text('Действие отменено')


# -----------------------------------------------------------------------------
# -------------------ДОБАВЛЕНИЕ КЛИЕНТА----------------------------------------
# -----------------------------------------------------------------------------
@dp.message_handler(commands=['addbuyer'])
async def add_buyer(message: Message):
    await message.answer(
        # 'Внимание! Данные о покупателе будут видны только вам, а так же '
        # + 'вашему руководителю будут видны имя, категория поиска, лимит, '
        # + 'источник оплаты, дата внесения\n\n'
        '✏ Введите имя покупателя\n\n'
        + '🙅‍♂️ Чтобы отменить внесение покупателя, напишите "Стоп"'
    )
    await Buyer.buyer_phone_number.set()


@dp.message_handler(state=Buyer.buyer_phone_number)
async def add_phone_number(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer('Действие по добавлению покупателя отменено')
        await state.finish()
    else:
        await state.update_data(buyer_name=message.text)
        await message.answer(
            message_texts.on.get('buyer_phone_number_entering_text')
        )
        await Buyer.category.set()


@dp.message_handler(state=Buyer.category)
async def add_category(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer('Действие по добавлению покупателя отменено')
        await state.finish()
    else:
        if re.match(r"^[0-9]+$", message.text):
            await state.update_data(buyer_phone_number=message.text)
            await message.answer(
                'В какой категории покупатель осуществляет поиск?\n\n'
                + '✳ Если ваш покупатель ищет в нескольких категориях, '
                + 'то заведите его требуемое количество раз с нужными категориями.',
                reply_markup=keyboards.buyer_searching_category()
            )
            await Buyer.limit.set()
        else:
            await message.answer(
                message_texts.phone_number_entering_error(
                    phone_number=message.text
                )
            )
            logging.error(f'🧐 Ошибка при вводе номера телефона {message.text}')
            await Buyer.category.set()


@dp.callback_query_handler(
    state=Buyer.limit,
    text=[
        'поиск_1к.кв.',
        'поиск_2к.кв.',
        'поиск_3к.кв.',
        'поиск_4к.кв.',
        'поиск_5к.кв.',
        'поиск_Комнаты, КГТ',
        'поиск_Дома',
        'поиск_Таунхаусы',
        'поиск_Участки',
        'Отменить внесение покупателя'
    ]
)
async def add_limit(callback: CallbackQuery, state: FSMContext):
    answer = callback.data
    if answer == 'Отменить внесение покупателя':
        await callback.message.edit_text(
            'Действие по добавлению покупателя отменено'
        )
        await state.finish()
    else:
        if answer in [
            'поиск_1к.кв.', 'поиск_2к.кв.', 'поиск_3к.кв.',
            'поиск_4к.кв.', 'поиск_5к.кв.'
        ]:
            await state.update_data(buyer_search_category=answer[6])
        elif answer == 'поиск_Комнаты, КГТ':
            await state.update_data(buyer_search_category='room')
        elif answer == 'поиск_Дома':
            await state.update_data(buyer_search_category='house')
        elif answer == 'поиск_Таунхаусы':
            await state.update_data(buyer_search_category='townhouse')
        else:
            await state.update_data(buyer_search_category='land')
        await callback.message.edit_text(
            '✏ Каков предел суммы покупателя?\n\n'
            + '❗ Напишите полное число со всеми нулями\n\n'
            + '🙅‍♂️ Чтобы отменить внесение покупателя, напишите "Стоп"'
        )
        await Buyer.source.set()


@dp.message_handler(state=Buyer.source)
async def add_source(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer('Действие по добавлению покупателя отменено')
        await state.finish()
    else:
        try:
            await state.update_data(buyer_limit=int(message.text))
            await message.answer(
                '✏ Выберите форму расчёта покупателя',
                reply_markup=keyboards.buyer_source_choice_keyboard()
            )
            await Buyer.microregion.set()
        except (ValueError) as e:
            await Buyer.source.set()
            await bot.send_sticker(
                chat_id=message.from_user.id,
                sticker=r"CAACAgIAAxkBAAEG_-ZjqHE6DzrO1BV48O2huiQ8kDVIIQACYwAD29t-AAGMnQU950KD5ywE"
            )
            await message.answer(
                message_texts.on.get('price_entering_error')
            )
            logging.error(f'{e}')


@dp.callback_query_handler(
    state=Buyer.microregion,
    text=[
        'Ипотечный кредит',
        'Наличные деньги',
        'Только мат. кап.',
        'Др. сертификаты',
        'Отменить внесение покупателя'
        ]
)
async def add_microregion(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'Отменить внесение покупателя':
        await callback.message.edit_text(
            'Действие по добавлению покупателя отменено'
        )
        await state.finish()
    else:
        await state.update_data(buyer_source=callback.data)
        data = await state.get_data()
        global checked
        if data.get(
            'buyer_search_category'
        ) in ['1', '2', '3', '4', '5'] or data.get(
            'buyer_search_category'
        ) == 'room':
            await callback.message.edit_text(
                '✏ Укажите один или несколько микрорайонов поиска',
                reply_markup=keyboards.city_microregion_keyboard(checked_buttons=[])
            )
            checked = []
            await Buyer.city_microregion.set()
        if data.get(
            'buyer_search_category'
        ) in ['house', 'townhouse', 'land']:
            await callback.message.edit_text(
                '✏ Укажите один или несколько микрорайонов поиска',
                reply_markup=keyboards.country_microregion_keyboard(checked_buttons=[])
            )
            checked = []
            await Buyer.country_microregion.set()


@dp.callback_query_handler(
    state=Buyer.city_microregion,
    text=object_city_microregions_for_checking
)
async def city_microreg_checkbox(callback: CallbackQuery, state: FSMContext):
    answer = callback.data
    if answer == 'Отменить внесение покупателя':
        await callback.message.edit_text(
            'Действие по добавлению покупателя отменено'
        )
        await state.finish()
    else:
        if answer == 'Подтвердить выбор':
            await state.update_data(microregions=checked)
            await callback.message.edit_text(
                '✏ Добавьте необходимый, по вашему мнению, комментарий к покупателю'
                + '(банк, что продаёт, сумму ПВ, без ПВ, и т.п.)\n\n'
                + '🙅‍♂️ Чтобы отменить внесение покупателя, напишите "Стоп"'
            )
            await Buyer.base_update.set()
        else:
            if '✅' in answer:
                checked.remove(answer.removeprefix('✅ '))
            else:
                checked.append(answer)
            await callback.message.edit_text(
                '✏ Укажите один или несколько микрорайонов поиска',
                reply_markup=keyboards.city_microregion_keyboard(checked_buttons=checked)
            )
            await Buyer.city_microregion.set()


@dp.callback_query_handler(
    state=Buyer.country_microregion,
    text=object_country_microregions_for_checking
)
async def country_microreg_checkbox(callback: CallbackQuery, state: FSMContext):
    answer = callback.data
    if answer == 'Отменить внесение покупателя':
        await callback.message.edit_text(
            'Действие по добавлению покупателя отменено'
        )
        await state.finish()
    else:
        if answer == 'Подтвердить выбор':
            await state.update_data(microregions=checked)
            await callback.message.edit_text(
                '✏ Добавьте необходимый, по вашему мнению, комментарий к покупателю'
                + '(банк, что продаёт, сумму ПВ, без ПВ, и т.п.)\n\n'
                + '🙅‍♂️ Чтобы отменить внесение покупателя, напишите "Стоп"'
            )
            await Buyer.base_update.set()
        else:
            if '✅' in answer:
                checked.remove(answer.removeprefix('✅ '))
            else:
                checked.append(answer)
            await callback.message.edit_text(
                '✏ Укажите один или несколько микрорайонов поиска',
                reply_markup=keyboards.country_microregion_keyboard(checked_buttons=checked)
            )
            await Buyer.country_microregion.set()


@dp.message_handler(state=Buyer.base_update)
async def base_update(message: Message, state: FSMContext):
    if message.text == 'Стоп':
        await message.answer('Действие по добавлению покупателя отменено')
        await state.finish()
    else:
        if len(message.text) <= 500:
            await state.update_data(buyer_comment=message.text, buyer_user_id=message.from_user.id)
            data = await state.get_data()
            # добавление в базу субъекта
            if not DB_Worker.buyer_to_db(data):
                await message.answer(
                    message_texts.on.get('sorry_about_error')
                )
            else:
                await message.answer('\n'.join(message_texts.buyer_adding_result_text(data=data)))

                class_name = Output.str_to_class(data.get('buyer_search_category').title())
                queryset = class_name.objects.filter(price__lte=data.get('buyer_limit'))
                if queryset.exists():
                    for item in queryset:
                        await bot.send_message(
                            chat_id=item.user_id, text='🚀 У пользователя '
                            + f'@{message.from_user.username}, '
                            + 'есть возможный '
                            + 'покупатель на твой объект\n'
                            + f'{Output.search_category_output(data.get("buyer_search_category"))}, '
                            + f'ул.{item.street_name}'
                        )

            await state.finish()
        else:
            await message.answer(
                'Комментарий по клиенту не должен превышать 500 знаков. '
                + 'Отредактируйте и попробуйте заново.'
            )
            await Buyer.base_update.set()

# -----------------------------------------------------------------------------
# -------------------УДАЛЕНИЕ КЛИЕНТА------------------------------------------
# -----------------------------------------------------------------------------


@dp.message_handler(commands=['deletebuyer'])
async def delete_buyer(message: Message):
    user_id = message.from_user.id
    if BuyerDB.objects.filter(user_id=user_id).exists():
        await message.answer(
            '✏ Выберите покупатея, которого вы хотите удалить',
            reply_markup=keyboards.buyer_list_keyboard(searching_user_id=user_id)
        )
        await DeleteBuyer.step2.set()
    else:
        await message.answer(
            ' У вас нет клиентов в базе'
        )


@dp.callback_query_handler(state=DeleteBuyer.step2)
async def deleting_buyer(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отмена':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        id = callback.data
        try:
            BuyerDB.objects.filter(pk=id).delete()
            await callback.message.edit_text(
                'Сделано!'
            )
            await state.finish()
        except Exception as e:
            await callback.message.answer(
                'Во время удаления возникла ошибка, попробуйте снова.'
                + 'Если ошибка поторится, напишиет об этом @davletelvir'
            )
            logging.error(
                f'Ошибка удаления субъекта, {e}'
            )
            await DeleteBuyer.step2.set()


# -----------------------------------------------------------------------------
# -------------------МОИ КЛИЕНТЫ------------------------------------------
# -----------------------------------------------------------------------------


@dp.message_handler(commands=['mybuyers'])
async def my_buyers(message: Message):
    user_id = message.from_user.id
    queryset = BuyerDB.objects.filter(user_id=user_id)
    if queryset.exists():
        await message.answer(
            f'У тебя {queryset.count()} покупателя(-ей):'
        )
        for item in queryset:
            await message.answer(
                f'❇ _Дата внесения: {item.pub_date.date().strftime("%d-%m-%Y")}_\n'
                f'*Имя:* {item.buyer_name},\n'
                + f'*Тел:* {item.phone_number},\n\n'
                + f'*Объект поиска:* {Output.search_category_output(item.category)},\n'
                + f'*Область поиска:* {item.microregion},\n\n'
                + f'*Денежный лимит:* {item.limit} ₽,\n'
                + f'*Денежный ресурс:* {item.source},\n\n'
                + f'*Комментарий:* {item.comment}',
                parse_mode='Markdown'
            )
    else:
        await message.answer(
            ' У тебя нет клиентов в базе'
        )

# -----------------------------------------------------------------------------
# -------------------ОБЪЕКТЫ ДЛЯ КЛИЕНТА---------------------------------------
# -----------------------------------------------------------------------------


@dp.message_handler(commands=['obj4mybuyer'])
async def obj_for_my_buyer(message: Message):
    user_id = message.from_user.id
    queryset = BuyerDB.objects.filter(user_id=user_id)
    if queryset.exists():
        await message.answer(
            '✏ Выберите покупатея, для которого вы хотите посмотреть подходящие объекты',
            reply_markup=keyboards.buyer_list_keyboard(searching_user_id=user_id)
        )
        await ObjForBuyer.step2.set()
    else:
        await message.answer(
            ' У вас нет клиентов в базе'
        )


@dp.callback_query_handler(state=ObjForBuyer.step2)
async def searching_for_buyer(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == 'Отмена':
        await callback.message.edit_text(
            'Действие отменено'
        )
        await state.finish()
    else:
        id = callback.data
        buyer = BuyerDB.objects.filter(pk=id)
        buyer_category = await buyer.values('category').aget()
        buyer_limit = await buyer.values('limit').aget()

        class_name = Output.str_to_class(buyer_category.get('category').title())

        queryset = class_name.objects.filter(price__lte=(buyer_limit.get('limit')))

        if queryset.exists():
            await callback.message.answer('🔎 Возможно, покупателю подойдут такие варианты:')

            if class_name == House:
                for item in queryset:
                    await asyncio.sleep(0.5)
                    album = MediaGroup()
                    photo_list = item.photo_id
                    for photo_id in photo_list:
                        if photo_id == photo_list[-1]:
                            album.attach_photo(
                                photo_id,
                                caption=message_texts.house_search_result_text(
                                    item=item
                                ),
                                parse_mode='Markdown'
                            )
                        else:
                            album.attach_photo(photo_id)
                    await callback.message.answer_media_group(media=album)

            elif class_name == TownHouse:
                for item in queryset:
                    await asyncio.sleep(0.5)
                    album = MediaGroup()
                    photo_list = item.photo_id
                    for photo_id in photo_list:
                        if photo_id == photo_list[-1]:
                            album.attach_photo(
                                photo_id,
                                caption=message_texts.townhouse_search_result_text(
                                    item=item
                                ),
                                parse_mode='Markdown'
                            )
                        else:
                            album.attach_photo(photo_id)
                    await callback.message.answer_media_group(media=album)

            elif class_name == Land:
                for item in queryset:
                    await asyncio.sleep(0.5)
                    album = MediaGroup()
                    photo_list = item.photo_id
                    for photo_id in photo_list:
                        if photo_id == photo_list[-1]:
                            album.attach_photo(
                                photo_id,
                                caption=message_texts.lands_search_result_text(
                                    item=item
                                ),
                                parse_mode='Markdown'
                            )
                        else:
                            album.attach_photo(photo_id)
                    await callback.message.answer_media_group(media=album)

            elif class_name == Apartment:
                for item in queryset:
                    await asyncio.sleep(0.5)
                    album = MediaGroup()
                    photo_list = item.photo_id
                    for photo_id in photo_list:
                        if photo_id == photo_list[-1]:
                            album.attach_photo(
                                photo_id,
                                caption=message_texts.apartments_search_result_text(
                                        room_count=int(buyer_category.get('category')),
                                        item=item
                                    ),
                                parse_mode='Markdown'
                            )
                        else:
                            album.attach_photo(photo_id)
                    await callback.message.answer_media_group(media=album)

            else:
                for item in queryset:
                    await asyncio.sleep(0.5)
                    album = MediaGroup()
                    photo_list = item.photo_id
                    for photo_id in photo_list:
                        if photo_id == photo_list[-1]:
                            album.attach_photo(
                                photo_id,
                                caption=message_texts.room_search_result_text(item=item),
                                parse_mode='Markdown'
                            )
                        else:
                            album.attach_photo(photo_id)
                    await callback.message.answer_media_group(media=album)
        else:
            await callback.message.edit_text(
                'К сожалению, ничего не нашёл в базе для твоего клиента'
            )
        await state.finish()

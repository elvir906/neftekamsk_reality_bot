from baza.management.commands.aio_bot import FSMContext
from baza.models import Apartment, House, Land, Room, TownHouse
from baza.utils import Output


class message_texts():
    on = {
        'delete': '❗ Внимание! Удаление объектов производится в ручном режиме '
                  + 'разработчиками, да бы избежать несанкционированных удалений. Напишите @davletelvir в произвольной '
                  + 'форме, что именно хотите удалить и его id - можно посмотреть в /myobjects. '
                  + 'Например, так: "Здравствуйте, '
                  + 'хочу удалить 2х, Ленина 7, id 45."',
        'about': [
                '✅ Бот поможет быстрее сработаться риелторам. Как? Все просто: если все объекты'
                + ' риелторов хранятся в одном месте, то легко в нужный момент найти их и связаться для показа.'
                + ' Поиск объектов по сайтам, группам и чатам – в прошлом! ',
                '',
                '*Как это работает*? У бота есть '
                + 'простое меню. Через команды вы можете добавить свои объекты или '
                + 'посмотреть объекты других риелторов и связаться друг с другом. Всё просто!',
                '',
                '✅ *ВАЖНО*! Разработчик не ставил перед собой цель "объехать" вас - риелторов, '
                + 'или быть между вами посредником: звонить по объекту будут вам.'
                + ' Смелей добавляйте объекты! 👍',
                '',
                'Обращения по работе бота направляйте @davletelvir. ',
                '',
                '*Версия 1.2:*\n'
                + '- Исправлен баг одновременной работы нескольких пользователей;\n'
                  ,
                '*Версия 1.1:*\n'
                + '- Возможность добавить в базу квартиры, комнаты, дома, таунхаусы и участки;\n'
                + '- Просмотр всех объектов;\n'
                + '- Просмотр своих объектов;\n'
                + '- Удаление объектов;\n'
                + '- Редактирование цены.',
                ],
        'statistics': 'Статистика по объектам пока недоступна',
    }

    def room_search_result_text(item: Room) -> str:
        """Шаблон тексата выдачи поиска по комнатам"""

        text = (
            f'🔸 _Комната {item.street_name} д.{item.number_of_house}_'
            + f'\n*Этаж:* {item.floor}/{item.number_of_floors}'
            + f'\n*Площадь комнаты:* {item.area} кв.м.'
            + f'\n*Описание:* {item.description} '
            + f'\n*Обременение:* {Output.false_or_true(item)[2]} '
            + f'\n*Дети в собственности:* {Output.false_or_true(item)[0]}'
            + f'\n*Возможность приобрести в ипотеку:* {Output.false_or_true(item)[1]}'
            + f'\n*Цена:* {int(item.price)} ₽'
            + f'\n*Агентство:* {item.agency_name}'
            + f'\n*Имя риелтора:* {item.author}'
            + f'\n*Номер телефона:* {item.phone_number}'
            + f'\n*Дата публикации:* {item.pub_date.date()}'
        )
        return text

    def house_search_result_text(item: House) -> str:
        """Шаблон тексата выдачи поиска по домам """

        text = (
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
            + f'\n*Обременение:* {Output.false_or_true(item)[2]}'
            + f'\n*Дети в собственности:* {Output.false_or_true(item)[0]}'
            + f'\n*Возможность приобрести в ипотеку:* {Output.false_or_true(item)[1]}'
            + f'\n*Цена:* {int(item.price)} ₽'
            + f'\n*Агентство:* {item.agency_name}'
            + f'\n*Имя риелтора:* {item.author}'
            + f'\n*Номер телефона:* {item.phone_number}'
            + f'\n*Дата публикации:* {item.pub_date.date()}'
        )
        return text

    def townhouse_search_result_text(item: TownHouse) -> str:
        """Шаблон текста выдачи поиска по таунхаусам"""

        text = (
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
            + f'\n*Обременение:* {Output.false_or_true(item)[2]}'
            + f'\n*Дети в собственности:* {Output.false_or_true(item)[0]}'
            + f'\n*Возможность приобрести в ипотеку:* {Output.false_or_true(item)[1]}'
            + f'\n*Цена:* {int(item.price)} ₽'
            + f'\n*Агентство:* {item.agency_name}'
            + f'\n*Имя риелтора:* {item.author}'
            + f'\n*Номер телефона:* {item.phone_number}'
            + f'\n*Дата публикации:* {item.pub_date.date()}'
        )
        return text

    def lands_search_result_text(item: Land) -> str:
        """Шаблон текста выдачи поиска по участкам"""

        text = (
            f'🔸 _Участок {item.microregion}, {item.street_name} уч.{item.number_of_land} _'
            + f'\n*Площадь участка:* {item.area_of_land} сот.'
            + f'\n*Назначение участка:* {item.purpose}'
            + f'\n*Степень газификации:* {item.gaz}'
            + f'\n*Вода:* {item.water}'
            + f'\n*Подъезд к участку:* {item.road}'
            + f'\n*Наличие ограждения:* {item.fence}'
            + f'\n*Описание:* {item.description}'
            + f'\n*Обременение:* {Output.false_or_true(item)[2]}'
            + f'\n*Дети в собственности:* {Output.false_or_true(item)[0]}'
            + f'\n*Возможность приобрести в ипотеку:* {Output.false_or_true(item)[1]}'
            + f'\n*Цена:* {int(item.price)} ₽'
            + f'\n*Агентство:* {item.agency_name}'
            + f'\n*Имя риелтора:* {item.author}'
            + f'\n*Номер телефона:* {item.phone_number}'
            + f'\n*Дата публикации:* {item.pub_date.date()}'
        )
        return text

    def apartments_search_result_text(room_count: int, item: Apartment) -> str:
        """Шаблон текста выдачи поиска по квартирам"""

        text = (
            f'🔸 _{room_count}к.кв. {item.street_name} д.{item.number_of_house}_'
            + f'\n*Этаж:* {item.floor}/{item.number_of_floors} '
            + f'\n*Площадь квартиры:* {item.area} кв.м.'
            + f'\n*Описание:* {item.description}'
            + f'\n*Обременение:* {Output.false_or_true(item)[2]}'
            + f'\n*Дети в собственности:* {Output.false_or_true(item)[0]}'
            + f'\n*Возможность приобрести в ипотеку:* {Output.false_or_true(item)[1]}'
            + f'\n*Цена:* {int(item.price)} ₽'
            + f'\n*Агентство:* {item.agency}'
            + f'\n*Имя риелтора:* {item.author}'
            + f'\n*Номер телефона:* {item.phone_number}'
            + f'\n*Дата публикации:* {item.pub_date.date()}'
        )
        return text

    def apartment_adding_result_text(data: dict) -> list:
        """Шаблон текста после добавления квартиры"""

        text = [
            '🔻 Готово! Вы занесли объект в базу:',
            f'*{data.get("reality_category")}*',
            f'*Количество комнат:* {data.get("room_count")}',
            f'*Название улицы:* {data.get("street_name")}',
            f'*Номер дома:* {data.get("house_number")}',
            f'*Этаж:* {data.get("floor")}/{data.get("floors")}',
            f'*Площадь:* {data.get("area")} кв.м.',
            f'*Краткое описание:* {data.get("description")}',
            f'*Обременение:* {Output.false_or_true(data.get("encumbrance"))}',
            f'*Дети в собственности:* {Output.false_or_true(data.get("cihldren"))}',
            f'*Оформить в ипотеку:* {Output.false_or_true(data.get("mortage"))}',
            f'*Цена:* {data.get("price")} ₽',
            f'*Имя риелтора:* {data.get("rieltor_name")}',
            f'*Название агентства:* {data.get("agency_name")}',
            f'*Контактный телефон:* {data.get("phone_number")}',
            '',
            '❎ Изменить цену в случае необходимости можно через пункт меню. '
            + 'Если надо удалить объект или изменить другую информацию, пишите @davletelvir'
        ]
        return text
    
    def room_adding_result_text(data: dict) -> list:
        """Шаблон текста после добавления квартиры"""

        text = [
            '🔻 Готово! Вы занесли объект в базу:',
            f'*{data.get("room_reality_category")}*',
            f'*Название улицы:* {data.get("room_street_name")}',
            f'*Номер дома:* {data.get("room_house_number")}',
            f'*Этаж:* {data.get("room_floor")}/{data.get("room_floors")}',
            f'*Площадь:* {data.get("room_area")} кв.м.',
            f'*Краткое описание:* {data.get("room_description")}',
            f'*Обременение:* {Output.false_or_true(data.get("room_encumbrance"))}',
            f'*Дети в собственности:* {Output.false_or_true(data.get("room_cihldren"))}',
            f'*Оформить в ипотеку:* {Output.false_or_true(data.get("room_mortage"))}',
            f'*Цена:* {data.get("room_price")} ₽',
            f'*Имя риелтора:* {data.get("room_rieltor_name")}',
            f'*Название агентства:* {data.get("room_agency_name")}',
            f'*Контактный телефон:* {data.get("room_phone_number")}',
            '',
            '❎ Изменить цену в случае необходимости можно через пункт меню. '
            + 'Если надо удалить объект или изменить другую информацию, пишите @davletelvir'
        ]
        return text

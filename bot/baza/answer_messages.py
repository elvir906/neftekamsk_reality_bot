from baza.models import Apartment, House, Land, Room, TownHouse
from baza.utils import Output


class message_texts():
    on = {
        'delete': '❗ Внимание!  Пока eдаление объектов производится в ручном режиме '
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
                + '- Появилась возможность добавить до 6 фото к объекту;\n'
                + '- Два варианта просмотра объектов - в "Карусели" и в каскадном виде;\n'
                + '- Несколько доработок опросника объектов'
                  ,
                '*Версия 1.1:*\n'
                + '- Возможность добавить в базу квартиры, комнаты, дома, таунхаусы и участки;\n'
                + '- Просмотр всех объектов;\n'
                + '- Просмотр своих объектов;\n'
                + '- Удаление объектов;\n'
                + '- Редактирование цены.',
                ],
        'statistics': 'Статистика по объектам пока недоступна. Будет, как только наберется 100+ объектов',

        'enter_price': '🔻 Напишите цену.\n\nПолную цену цифрами, '
                       + 'не сокращая, и без знаков Р, р, ₽, руб. и т.п.'
                       + '\n\nЕсли недвижимость '
                       + 'стоит 3400000 рублей, значит так и пишите 3400000',

        'area_entering_error': '🤔 Вы ошиблись при вводе значения площади.\n\nПлощадь'
                                + ' следует вводить цифрами и использовать разделитель "." для '
                                + 'дробных значений. Так же НЕ указывайте единицы измерения. '
                                + '\n\n🔻 Попробуйте ввести значение заново:',

        'price_entering_error': '🤔 Вы ошиблись при вводе значения цены.\n\nЦену'
                                + ' следует вводить цифрами без пробелов и разделителя "." '
                                + 'и без указания единицы измерения.'
                                + '\n\n🔻 Попробуйте ввести значение заново:',

        'phone_number_entering_text': '🔻 Напишите свой номер '
                                      + 'телефона в формате 89ххххххххх, по которому с'
                                      + 'вами можно будет связаться',

        'phone_number_entering_text_for_editing': '🔻 Введи свой номер телефона в формате 89ххххххххх '
                                                  + '(11 цифр номера, начиная с 8-ки)',

        'sorry_about_error': 'К сожалению, в работе бота произошла ошибка. Попробуйте еще раз. '
                             + 'Если ошибка повторится, напишите об этом @davletelvir',

        'agency_entering_text': '🔻 В каком агентстве вы трудитесь?\n\n'
                                + 'Если вы частный риелтор, то напишите "Частный"',

        'area_entering_text': '🔻 Введите площадь, как в указано в свидетельстве или выписке. '
                              + '\n\nИспользуйте разделитель "." для дробной и целой частей.',

        'start': '👋 Привет! Рад приветствовать тебя! Я храню в своей базе актуальные '
                              + 'объекты и помогаю риелторам города Нефтекамск сработаться.\n\n'
                              + '🔻 Начните работу с нажатия кнопки "Меню"',

        'code_word_text': 'Придумайте и запомните и введите кодовое слово. Оно пригодится'
        + ' в будущем для удаления или редактирования ваших объектов,'
        + ' чтобы никто, кроме вас, не смог этого сделать'
    }

    def character_limit(text_len: int) -> str:
        text = (
            f'🔻 Текст описания состоит из {text_len} знаков и тем самым превышает ограничение в 200 знаков. '
            + 'Попробуйте укоротить описание, оставив только суть - '
            + 'состояние.'
        )
        return text

    def entering_description_text(category: str) -> str:
        text = (
            f'🔻 Добавьте небольшое описание {category}.\n\nПожалуйста, '
            + ' руководствуйтесь принципом "Краткость - сестра таланта" '
            + ' не превышайте ограничение в 200 знаков и не дублируйте '
            + 'в описании информацию о квартире, такие как этаж, цена и др. '
            + '\n\nТолько кратко, самую суть - состояние. И если надо,'
            + ' кол-во c/у / комн. и пр. инфу в мс'
        )
        return text

    def phone_number_entering_error(phone_number: str) -> str:
        text = (
            '🔻 Вы ошиблись с вводом номера телефона. '
            + f'Введённый вами номер телефона {phone_number} '
            + '\n\nВведите просто 11 цифр номера, начиная с 8.'
        )
        return text

    def room_search_result_text(item: Room) -> str:
        """Шаблон тексата выдачи поиска по комнатам"""
        text = (
            f'✅ _Комната {item.street_name} д.{item.number_of_house}_'
            + f'\n*Этаж:* {item.floor}/{item.number_of_floors}'
            + f'\n*Площадь квартиры:* {item.area} кв.м.'
            + f'\n*Описание:* {item.description}'
            + f'\n*Обременение:* {Output.false_or_true(item.encumbrance)}'
            + f'\n*Дети в собственности:* {Output.false_or_true(item.children)}'
            + f'\n*Возможность приобрести в ипотеку:* {Output.false_or_true(item.mortage)}'
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
            f'✅ _Дом {item.microregion}, {item.street_name}_'
            + f'\n*Площадь дома:* {item.area} кв.м.'
            + f'\n*Площадь участка:* {item.area_of_land} сот.'
            + f'\n*Назначение участка:* {item.purpose}'
            + f'\n*Материал стен:* {item.material}'
            + f'\n*Завершённое строительство:* {item.finish}'
            + f'\n*Степень газификации:* {item.gaz}'
            + f'\n*Вода:* {item.water}'
            + f'\n*Подъезд к дому:* {item.road}'
            + f'\n*Наличие бани/сауны:* {item.sauna}'
            + f'\n*Наличие гаража:* {item.garage}'
            + f'\n*Наличие ограждения:* {item.fence}'
            + f'\n*Описание:* {item.description}'
            + f'\n*Обременение:* {Output.false_or_true(item.encumbrance)}'
            + f'\n*Дети в собственности:* {Output.false_or_true(item.children)}'
            + f'\n*Возможность приобрести в ипотеку:* {Output.false_or_true(item.mortage)}'
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
            f'✅ _Таунхаус {item.microregion}, {item.street_name}_'
            + f'\n*Площадь дома:* {item.area} кв.м.'
            + f'\n*Площадь участка:* {item.area_of_land} сот.'
            + f'\n*Назначение участка:* {item.purpose}'
            + f'\n*Материал стен:* {item.material}'
            + f'\n*Завершённое строительство:* {item.finish}'
            + f'\n*Степень газификации:* {item.gaz}'
            + f'\n*Вода:* {item.water}'
            + f'\n*Подъезд к дому:* {item.road}'
            + f'\n*Наличие бани/сауны:* {item.sauna}'
            + f'\n*Наличие гаража:* {item.garage}'
            + f'\n*Наличие ограждения:* {item.fence}'
            + f'\n*Описание:* {item.description}'
            + f'\n*Обременение:* {Output.false_or_true(item.encumbrance)}'
            + f'\n*Дети в собственности:* {Output.false_or_true(item.children)}'
            + f'\n*Возможность приобрести в ипотеку:* {Output.false_or_true(item.mortage)}'
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
            f'✅ _Участок {item.microregion}, {item.street_name} уч.{item.number_of_land} _'
            + f'\n*Площадь участка:* {item.area_of_land} сот.'
            + f'\n*Назначение участка:* {item.purpose}'
            + f'\n*Степень газификации:* {item.gaz}'
            + f'\n*Вода:* {item.water}'
            + f'\n*Подъезд к участку:* {item.road}'
            + f'\n*Наличие ограждения:* {item.fence}'
            + f'\n*Описание:* {item.description}'
            + f'\n*Обременение:* {Output.false_or_true(item.encumbrance)}'
            + f'\n*Дети в собственности:* {Output.false_or_true(item.children)}'
            + f'\n*Возможность приобрести в ипотеку:* {Output.false_or_true(item.mortage)}'
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
            f'✅ _{room_count}к.кв. {item.street_name} д.{item.number_of_house}_'
            + f'\n*Этаж:* {item.floor}/{item.number_of_floors}'
            + f'\n*Площадь квартиры:* {item.area} кв.м.'
            + f'\n*Описание:* {item.description}'
            + f'\n*Обременение:* {Output.false_or_true(item.encumbrance)}'
            + f'\n*Дети в собственности:* {Output.false_or_true(item.children)}'
            + f'\n*Возможность приобрести в ипотеку:* {Output.false_or_true(item.mortage)}'
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
            '🔻 Готово! Вы внесли объект в базу:',
            f'*{data.get("reality_category")}*',
            f'*Количество комнат:* {data.get("room_count")}',
            f'*Название улицы:* {data.get("street_name")}',
            f'*Номер дома:* {data.get("house_number")}',
            f'*Этаж:* {data.get("floor")}/{data.get("floors")}',
            f'*Площадь:* {data.get("area")} кв.м.',
            f'*Краткое описание:* {data.get("description")}',
            f'*Обременение:* {Output.false_or_true(data.get("encumbrance"))}',
            f'*Дети в собственности:* {Output.false_or_true(data.get("children"))}',
            f'*Оформить в ипотеку:* {Output.false_or_true(data.get("mortage"))}',
            f'*Цена:* {data.get("price")} ₽',
            f'*Имя риелтора:* {data.get("rieltor_name")}',
            f'*Название агентства:* {data.get("agency_name")}',
            f'*Контактный телефон:* {data.get("phone_number")}',
            '',
            '❎ Не забудьте удалить объект, когда он будет продан. '
            + 'Удалить объект или изменить цену в случае необходимости можно через пункт меню. '
            + 'Чтобы изменить другую информацию, пишите @davletelvir.'

        ]
        return text

    def room_adding_result_text(data: dict) -> list:
        """Шаблон текста после добавления квартиры"""

        text = [
            '🔻 Готово! Вы внесли объект в базу:',
            f'*{data.get("room_reality_category")}*',
            f'*Название улицы:* {data.get("room_street_name")}',
            f'*Номер дома:* {data.get("room_house_number")}',
            f'*Этаж:* {data.get("room_floor")}/{data.get("room_floors")}',
            f'*Площадь:* {data.get("room_area")} кв.м.',
            f'*Краткое описание:* {data.get("room_description")}',
            f'*Обременение:* {Output.false_or_true(data.get("room_encumbrance"))}',
            f'*Дети в собственности:* {Output.false_or_true(data.get("room_children"))}',
            f'*Оформить в ипотеку:* {Output.false_or_true(data.get("room_mortage"))}',
            f'*Цена:* {data.get("room_price")} ₽',
            f'*Имя риелтора:* {data.get("room_rieltor_name")}',
            f'*Название агентства:* {data.get("room_agency_name")}',
            f'*Контактный телефон:* {data.get("room_phone_number")}',
            '',
            '❎ Не забудьте удалить объект, когда он будет продан. '
            + 'Удалить объект или изменить цену в случае необходимости можно через пункт меню. '
            + 'Чтобы изменить другую информацию, пишите @davletelvir.'
        ]
        return text

    def house_adding_result_text(data: dict) -> list:
        """Шаблон текста после добавления дома"""

        text = [
            '🔻 Готово! Вы внесли объект в базу:',
            f'*{data.get("house_reality_category")}*',
            f'*Микрорайон расположения:* {data.get("house_microregion")}',
            f'*Название улицы:* {data.get("house_street_name")}',
            f'*Назначение земли:* {data.get("house_purpose")}',
            f'*Площадь участка:* {data.get("house_land_area")} сот.',
            f'*Завершённость строительства:* {data.get("house_finish")}',
            f'*Материал:* {data.get("house_material")}',
            f'*Степень газификации:* {data.get("house_gaz")}',
            f'*Степень водоснабжения:* {data.get("house_water")}',
            f'*Наличие бани/сауны:* {data.get("house_sauna")}',
            f'*Наличие гаража:* {data.get("house_garage")}',
            f'*Наличие забора:* {data.get("house_fence")}',
            f'*Проезд к дому:* {data.get("house_road")}',
            f'*Площадь дома:* {data.get("house_area")} кв.м.',
            f'*Краткое описание:* {data.get("house_description")}',
            f'*Обременение:* {Output.false_or_true(data.get("house_encumbrance"))}',
            f'*Дети в собственности:* {Output.false_or_true(data.get("house_children"))}',
            f'*Возможность оформить в ипотеку:* {Output.false_or_true(data.get("house_mortage"))}',
            f'*Цена:* {data.get("house_price")} ₽',
            f'*Имя риелтора:* {data.get("house_rieltor_name")}',
            f'*Название агентства:* {data.get("house_agency_name")}',
            f'*Контактный телефон:* {data.get("house_phone_number")}',
            '',
            '❎ Не забудьте удалить объект, когда он будет продан. '
            + 'Удалить объект или изменить цену в случае необходимости можно через пункт меню. '
            + 'Чтобы изменить другую информацию, пишите @davletelvir.'
        ]
        return text

    def townhouse_adding_result_text(data: dict) -> list:
        """Шаблон текста после добавления таунхауса"""

        text = [
            '🔻 Готово! Вы внесли объект в базу:',
            f'*{data.get("townhouse_reality_category")}*',
            f'*Микрорайон расположения:* {data.get("townhouse_microregion")}',
            f'*Название улицы:* {data.get("townhouse_street_name")}',
            f'*Назначение земли:* {data.get("townhouse_purpose")}',
            f'*Площадь участка:* {data.get("townhouse_land_area")} сот.',
            f'*Завершённость строительства:* {data.get("townhouse_finish")}',
            f'*Материал:* {data.get("townhouse_material")}',
            f'*Степень газификации:* {data.get("townhouse_gaz")}',
            f'*Степень водоснабжения:* {data.get("townhouse_water")}',
            f'*Наличие бани/сауны:* {data.get("townhouse_sauna")}',
            f'*Наличие гаража:* {data.get("townhouse_garage")}',
            f'*Наличие забора:* {data.get("townhouse_fence")}',
            f'*Проезд к дому:* {data.get("townhouse_road")}',
            f'*Площадь таунхауса:* {data.get("townhouse_area")} кв.м.',
            f'*Краткое описание:* {data.get("townhouse_description")}',
            f'*Обременение:* {Output.false_or_true(data.get("townhouse_encumbrance"))}',
            f'*Дети в собственности:* {Output.false_or_true(data.get("townhouse_children"))}',
            f'*Возможность оформить в ипотеку:* {Output.false_or_true(data.get("townhouse_mortage"))}',
            f'*Цена:* {data.get("townhouse_price")} ₽',
            f'*Имя риелтора:* {data.get("townhouse_rieltor_name")}',
            f'*Название агентства:* {data.get("townhouse_agency_name")}',
            f'*Контактный телефон:* {data.get("townhouse_phone_number")}',
            '',
            '❎ Не забудьте удалить объект, когда он будет продан. '
            + 'Удалить объект или изменить цену в случае необходимости можно через пункт меню. '
            + 'Чтобы изменить другую информацию, пишите @davletelvir.'
        ]
        return text

    def land_adding_result_text(data: dict) -> list:
        """Шаблон текста после добавления участка"""

        text = [
            '🔻 Готово! Вы внесли объект в базу:',
            f'*{data.get("land_reality_category")}*',
            f'*Микрорайон расположения:* {data.get("land_microregion")}',
            f'*Название улицы:* {data.get("land_street_name")}',
            f'*Номер участка:* {data.get("land_number_name")}',
            f'*Назначение земли:* {data.get("land_purpose")}',
            f'*Площадь участка:* {data.get("land_area")} сот.',
            f'*Газа по улице:* {data.get("land_gaz")}',
            f'*Вода по улице:* {data.get("land_water")}',
            f'*Наличие бани/сауны:* {data.get("land_sauna")}',
            f'*Наличие гаража:* {data.get("land_garage")}',
            f'*Наличие забора:* {data.get("land_fence")}',
            f'*Проезд к участку:* {data.get("land_road")}',
            f'*Краткое описание:* {data.get("land_description")}',
            f'*Обременение:* {Output.false_or_true(data.get("land_encumbrance"))}',
            f'*Дети в собственности:* {Output.false_or_true(data.get("land_children"))}',
            f'*Возможность оформить в ипотеку:* {Output.false_or_true(data.get("land_mortage"))}',
            f'*Цена:* {data.get("land_price")} ₽',
            f'*Имя риелтора:* {data.get("land_rieltor_name")}',
            f'*Название агентства:* {data.get("land_agency_name")}',
            f'*Контактный телефон:* {data.get("land_phone_number")}',
            '',
            '❎ Не забудьте удалить объект, когда он будет продан. '
            + 'Удалить объект или изменить цену в случае необходимости можно через пункт меню. '
            + 'Чтобы изменить другую информацию, пишите @davletelvir.'
        ]
        return text

    def my_objects_text(data: dict) -> str:
        if data.get("total_count") == 0:
            text = 'У вас нет объектов в базе'
            return text
        text = (f'У вас *{data.get("total_count")}* объект (-а, -ов):\n'
                + f'квартир - {data.get("apartment_count")},\n'
                + f'комнат - {data.get("room_count")},\n'
                + f'домов - {data.get("house_count")},\n'
                + f'таунхаусов - {data.get("townhouse_count")},\n'
                + f'участков - {data.get("land_count")}'
                + '\n\n'
                + 'Ниже список Ваших объектов с указанием id:')
        return text

    def aqidel():
        text = ('Гипотеза засыпанного русла.\n\n'
                + 'Вы будете удивлены, но река Белая раньше '
                + 'протекала рядом с местом, где стоит наш город Нефтекамск. '
                + 'Низины рядом с сёлами Кутлинка, Ташкиново - '
                + 'это её старые русла. Так же все овраги в нашем городе '
                + '- это заводи Белой и русла более маленьких рек.\n\n'
                + 'Река перестала существовать вследствие произошедшей '
                + 'в середине 19 века глобальной катастрофы, засыпавшей глиной '
                + 'первые этажи краснокирпичных зданий по всему миру. '
                + 'Досталось и реке: часть старого русла засыпало глиной. '
                + 'Теперь на её месте остались более мелкие речки: родники, '
                + 'питавшие большую реку, так сказать, никто не отменял. '
                + 'А сама река срезала себе путь.\n\n'
                + 'Не исключено, что раньше было развито рыболовство и судоходство, '
                + 'а так же торговля. Об этом свидетельствует усадьба '
                + 'нижегородских купцов Вечтомовых в Касёво. Они, якобы, сплавляясь '
                + 'по реке Кама, были удивлены местной красотой, что решили здесь '
                + 'обосноваться и вести торговлю. Тут у меня два вопроса. '
                + 'Официально на месте города всегда было поле и небольшие сёла. '
                + 'Соснового леса еще не было: ему от силы лет 150-170-200. '
                + 'Что здесь было делать? О какой тоговле может идти речь, '
                + 'если даже ближайший водный торговый путь по р.Кама находился '
                + 'как минимум в 10 км от Касёва? А то и больше. '
                + 'Зачем здесь было строить торговый дом, '
                + 'коим являлось их поместье?\n\n'
                + 'Купцы могли обосноваться и вести торговлю на этом месте, только '
                + 'если рядом был водный торговый путь и было развито судоходство, '
                + 'а так же было достаточное количество населения. Говоря '
                + 'современным языком, для хорошей торговли нужна была движуха.\n\n'
                + 'Само здание поместья Вечтомовых, точнее первый его этаж '
                + 'засыпан глиной, о чем свидетельствуют низко расположенные '
                + 'окна первого этажа. Оно располагается в Касёво на пересечении '
                + 'улиц Трактовой и Колхозной и располагается как раз вблизи '
                + 'реки Маринка. Если встать на мост этой реки, взглянуть вниз, '
                + 'то можно отметить для себя непропорциональность низины реки '
                + 'и её русла. Но речка шириной в 4 метра не могла себе создать '
                + 'низменность шириной более 110 метров! Такая низина вполне '
                + ' могла быть руслом реки шириной около 100 метров и, получается,'
                + ' глубиной 2,5-3. А этого достаточно для судоходства.\n\n'

                + 'Так же в нашем крае была развита и промышленность, на что имеются '
                + 'документальные следы о существовании '
                + 'прежде на месте города Нефтекамск медеплавительной базы под '
                + 'названием Ильдианск. Для её работы так же требовалось большое '
                + 'количество воды. Но после катастрофы производство пришлось '
                + 'свернуть и перевезти в другое место, так как требовлась вода, '
                + 'которой уже не было в нужном количестве. Кама хоть и полноводная, '
                + 'но строить на ней базу на тот момент было и не удобно и не резонно. '
                + 'Куда удобнее было на одной из устей реки Белой возвести '
                + 'дамбу и питаться от собравшейся воды. Небольшое устье реки белой в сторону '
                + 'Камы было идеальным местом! \n\n Я думаю, производство перевезли '
                + 'в Уфу. Именно перевезли, а не разрушили, как говорят историки, во '
                + 'время Пугачевских восстаний. Ведь тогда бы остались руины и '
                + 'материальные следы, подобно разрушенным старинным зданиям. '
                + 'Но на месте этой базы ничего нет.\n\n'
                + 'Всё это - материальные и документальные следы '
                + 'а так же мои предположения - прямо указывают '
                + 'на существование ранее рядом с Ташкиново, Кутлинка большой '
                + 'реки, а так же больших заводей и рек в сторону Касева, Михайловки, Роткова, '
                + 'Марино; большого количества населения с развитой торговлей '
                + 'ремесленничеством, рыболовством и промышленностью. \n\n'
                + 'На мои гипотезы подтолкнула карта 1779 года, на котором отмечено '
                + 'старое русло реки.')

        return text

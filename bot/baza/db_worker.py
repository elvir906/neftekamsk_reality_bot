import datetime as dt
import logging

from aiogram.dispatcher import FSMContext
from baza.models import Apartment, House, Land, Room, TownHouse
# from decouple import config

# DB_NAME = config('DB_NAME')
# POSTGRES_USER = config('POSTGRES_USER')
# POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
# DB_HOST = config('DB_HOST')
# DB_PORT = config('DB_PORT')

# pub_date = dt.datetime.now()

# db_connection = psycopg2.connect(
#         database=DB_NAME,
#         user=POSTGRES_USER,
#         password=POSTGRES_PASSWORD,
#         host=DB_HOST,
#         port=DB_PORT
#     )


class DB_Worker():
    def apartment_to_db(state_data: FSMContext) -> bool:
        try:
            Apartment.objects.create(
                room_quantity=state_data.get('room_count'),
                street_name=state_data.get('street_name'),
                number_of_house=state_data.get('house_number'),
                floor=state_data.get('floor'),
                area=state_data.get('area'),
                number_of_floors=state_data.get('floors'),
                price=state_data.get('price'),
                description=state_data.get('description'),
                encumbrance=state_data.get('encumbrance'),
                children=state_data.get('children'),
                mortage=state_data.get('mortage'),
                phone_number=state_data.get('phone_number'),
                agency=state_data.get('agency_name'),
                author=state_data.get('rieltor_name'),
                photo_id=state_data.get('photo'),
                code_word=state_data.get('code_word'),
                user_id=state_data.get('user_id'),
                pub_date=dt.datetime.now()
            )
            return True
        except Exception as e:
            logging.error(f'{e}')
            return False

    def room_to_db(state_data: FSMContext) -> bool:
        try:
            Room.objects.create(
                street_name=state_data.get('room_street_name'),
                number_of_house=state_data.get('room_house_number'),
                floor=state_data.get('room_floor'),
                area=state_data.get('room_area'),
                number_of_floors=state_data.get('room_floors'),
                price=state_data.get('room_price'),
                description=state_data.get('room_description'),
                encumbrance=state_data.get('room_encumbrance'),
                children=state_data.get('room_children'),
                mortage=state_data.get('room_mortage'),
                phone_number=state_data.get('room_phone_number'),
                agency_name=state_data.get('room_agency_name'),
                author=state_data.get('room_rieltor_name'),
                photo_id=state_data.get('room_photo'),
                code_word=state_data.get('room_code_word'),
                user_id=state_data.get('room_user_id'),
                pub_date=dt.datetime.now()
            )
            return True
        except Exception as e:
            logging.error(f'{e}')
            return False

    def house_to_db(state_data: FSMContext) -> bool:
        try:
            House.objects.create(
                microregion=state_data.get('house_microregion'),
                street_name=state_data.get('house_street_name'),
                purpose=state_data.get('house_purpose'),
                finish=state_data.get('house_finish'),
                material=state_data.get('house_material'),
                gaz=state_data.get('house_gaz'),
                water=state_data.get('house_water'),
                sauna=state_data.get('house_sauna'),
                garage=state_data.get('house_garage'),
                fence=state_data.get('house_fence'),
                road=state_data.get('house_road'),
                area=state_data.get('house_area'),
                area_of_land=state_data.get('house_land_area'),
                price=state_data.get('house_price'),
                description=state_data.get('house_description'),
                encumbrance=state_data.get('house_encumbrance'),
                children=state_data.get('house_children'),
                mortage=state_data.get('house_mortage'),
                phone_number=state_data.get('house_phone_number'),
                agency_name=state_data.get('house_agency_name'),
                author=state_data.get('house_rieltor_name'),
                photo_id=state_data.get('house_photo'),
                code_word=state_data.get('house_code_word'),
                user_id=state_data.get('house_user_id'),
                pub_date=dt.datetime.now()
            )
            return True
        except Exception as e:
            logging.error(f'{e}')
            return False

    def townhouse_to_db(state_data: FSMContext) -> bool:
        try:
            TownHouse.objects.create(
                microregion=state_data.get('townhouse_microregion'),
                street_name=state_data.get('townhouse_street_name'),
                purpose=state_data.get('townhouse_purpose'),
                finish=state_data.get('townhouse_finish'),
                material=state_data.get('townhouse_material'),
                gaz=state_data.get('townhouse_gaz'),
                water=state_data.get('townhouse_water'),
                sauna=state_data.get('townhouse_sauna'),
                garage=state_data.get('townhouse_garage'),
                fence=state_data.get('townhouse_fence'),
                road=state_data.get('townhouse_road'),
                area=state_data.get('townhouse_area'),
                area_of_land=state_data.get('townhouse_land_area'),
                price=state_data.get('townhouse_price'),
                description=state_data.get('townhouse_description'),
                encumbrance=state_data.get('townhouse_encumbrance'),
                children=state_data.get('townhouse_children'),
                mortage=state_data.get('townhouse_mortage'),
                phone_number=state_data.get('townhouse_phone_number'),
                agency_name=state_data.get('townhouse_agency_name'),
                author=state_data.get('townhouse_rieltor_name'),
                photo_id=state_data.get('townhouse_photo'),
                code_word=state_data.get('townhouse_code_word'),
                user_id=state_data.get('townhouse_user_id'),
                pub_date=dt.datetime.now()
            )
            return True
        except Exception as e:
            logging.error(f'{e}')
            return False

    def land_to_db(state_data: FSMContext) -> bool:
        try:
            Land.objects.create(
                microregion=state_data.get('land_microregion'),
                street_name=state_data.get('land_street_name'),
                number_of_land=state_data.get('land_number_name'),
                purpose=state_data.get('land_purpose'),
                gaz=state_data.get('land_gaz'),
                water=state_data.get('land_water'),
                sauna=state_data.get('land_sauna'),
                garage=state_data.get('land_garage'),
                fence=state_data.get('land_fence'),
                road=state_data.get('land_road'),
                area_of_land=state_data.get('land_area'),
                price=state_data.get('land_price'),
                description=state_data.get('land_description'),
                encumbrance=state_data.get('land_encumbrance'),
                children=state_data.get('land_children'),
                mortage=state_data.get('land_mortage'),
                phone_number=state_data.get('land_phone_number'),
                agency_name=state_data.get('land_agency_name'),
                author=state_data.get('land_rieltor_name'),
                photo_id=state_data.get('land_photo'),
                code_word=state_data.get('land_code_word'),
                user_id=state_data.get('land_user_id'),
                pub_date=dt.datetime.now()
            )
            return True
        except Exception as e:
            logging.error(f'{e}')
            return False

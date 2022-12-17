import datetime as dt
import logging

import psycopg2
from decouple import config

DB_NAME = config('DB_NAME')
POSTGRES_USER = config('POSTGRES_USER')
POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')

pub_date = dt.datetime.now()

db_connection = psycopg2.connect(
        database=DB_NAME,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


class DB_Worker():
    def apartment_to_db(state_data):
        cursor = db_connection.cursor()
        pub_date = dt.datetime.now()
        try:
            query_data = ()
            for item in state_data:
                if item != 'reality_category':
                    query_data = query_data + (state_data[item],)
            query_data = query_data + (pub_date,)
            query = 'INSERT INTO baza_apartment (room_quantity, street_name, number_of_house, floor, number_of_floors, area, price, description, encumbrance, children, mortage, phone_number, agency, author, photo_id, pub_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(query, query_data)
            db_connection.commit()
            return True
        except Exception as e:
            logging.error(f'{e}')
            return False
        finally:
            cursor.close()

    def room_to_db(state_data):
        cursor = db_connection.cursor()
        pub_date = dt.datetime.now()
        try:
            query_data = ()
            for item in state_data:
                if item != 'room_reality_category':
                    query_data = query_data + (state_data[item],)
            query_data = query_data + (pub_date,)
            query = 'INSERT INTO baza_room (street_name, number_of_house, floor, number_of_floors, area, price, description, encumbrance, children, mortage, phone_number, agency_name, author, photo_id, pub_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(query, query_data)
            db_connection.commit()
            return True
        except Exception as e:
            logging.error(f'{e}')
            return False
        finally:
            cursor.close()

    def house_to_db(state_data):
        cursor = db_connection.cursor()
        pub_date = dt.datetime.now()
        try:
            query_data = ()
            for item in state_data:
                if item != 'house_reality_category':
                    query_data = query_data + (state_data[item],)
            query_data = query_data + (pub_date,)
            query = 'INSERT INTO baza_house (microregion, street_name, purpose, finish, material, gaz, water, sauna, garage, fence, road, area, area_of_land, price, description, encumbrance, children, mortage, phone_number, agency_name, author, photo_id, pub_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(query, query_data)
            db_connection.commit()
            return True
        except Exception as e:
            logging.error(f'{e}')
            return False
        finally:
            cursor.close()

    def townhouse_to_db(state_data):
        cursor = db_connection.cursor()
        pub_date = dt.datetime.now()
        try:
            query_data = ()
            for item in state_data:
                if item != 'townhouse_reality_category':
                    query_data = query_data + (state_data[item],)
            query_data = query_data + (pub_date,)
            query = 'INSERT INTO baza_townhouse (microregion, street_name, purpose, finish, material, gaz, water, sauna, garage, fence, road, area, area_of_land, price, description, encumbrance, children, mortage, phone_number, agency_name, author, photo_id, pub_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(query, query_data)
            db_connection.commit()
            return True
        except Exception as e:
            logging.error(f'{e}')
            return False
        finally:
            cursor.close()

    def land_to_db(state_data):
        cursor = db_connection.cursor()
        pub_date = dt.datetime.now()
        try:
            query_data = ()
            for item in state_data:
                if item != 'land_reality_category':
                    query_data = query_data + (state_data[item],)
            query_data = query_data + (pub_date,)
            query = 'INSERT INTO baza_land (microregion, street_name, number_of_land, purpose, gaz, water, sauna, garage, fence, road, area_of_land, price, description, encumbrance, children, mortage, phone_number, agency_name, author, photo_id, pub_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(query, query_data)
            db_connection.commit()
            return True
        except Exception as e:
            logging.error(f'{e}')
            return False
        finally:
            cursor.close()

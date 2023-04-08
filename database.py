import logging

from typing import Union, Any


import pymysql

import pymysql.cursors


from config import DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME


class Database:

    """Класс работы с базой данных"""

    _post_connections: dict[int, pymysql.Connection]

    _post_cursors: dict[int, pymysql.cursors.DictCursor]

    def __init__(self):

        self._district_connection = self.connection(db="privat_privat")

        self._post_cursors = dict()

        self._post_connections = dict()

        logging.info("Database connection established")

    def connection(self, db=DB_NAME):
        return pymysql.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            db=db,
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=999999,
        )

    def _execute_query(self, query):
        cursor = self._district_connection.cursor()

        cursor.execute(query)

        records = cursor.fetchall()

        cursor.close()
        return records

    async def dispose_post_cursor(self, telegram_user_id: int):
        if telegram_user_id not in self._post_cursors.keys():
            return

        self._post_cursors[telegram_user_id].close()
        del self._post_cursors[telegram_user_id]

    def select_districts(
        self,
    ) -> Union[tuple[dict[str, Any], ...], None]:

        select_query = "SELECT id, name FROM spr_rajonw ORDER BY id ASC"

        self._district_connection.ping(reconnect=True)

        record = self._execute_query(select_query)

        self._district_connection.close()

        return record

    async def select_posts(
        self,
        city_id,
        type_object_id: str,
        room_count: list,
        ploshad: list,
        price: list,
        type_pomesh_id: Union[str, None],
        telegram_user_id: int,
    ):

        select_query = (
            "SELECT * FROM objectsw"
            f" WHERE type_object_id {type_object_id}"
            f" AND city_id = {city_id}"
        )

        counter = 0

        for sql_filter in room_count:

            if counter == 0:

                select_query += f" AND (room_count {sql_filter}"

            else:

                select_query += f" OR room_count {sql_filter}"

            counter += 1

        if room_count != []:
            select_query += ")"

        counter = 0

        for sql_filter in ploshad:

            if counter == 0:

                select_query += f" AND (ploshad {sql_filter}"

            else:

                select_query += f" OR ploshad {sql_filter}"

            counter += 1

        if ploshad != []:
            select_query += ")"

        counter = 0

        for sql_filter in price:

            if counter == 0:

                select_query += f" AND (price {sql_filter}"
            else:

                select_query += f" OR price {sql_filter}"

            counter += 1

        if price != []:
            select_query += ")"

        if type_pomesh_id is not None:

            select_query += f" AND type_pomesh_id = {type_pomesh_id}"

        self._post_connections[telegram_user_id] = self.connection()

        self._post_cursors[telegram_user_id] = self._post_connections[
            telegram_user_id
        ].cursor()

        self._post_cursors[telegram_user_id].execute(select_query)

    async def fetch_posts(self, telegram_user_id):
        self._post_connections[telegram_user_id].ping(reconnect=True)

        self._post_connections[telegram_user_id].cursor()

        record = self._post_cursors[telegram_user_id].fetchmany(8)
        return record

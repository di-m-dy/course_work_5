"""
ru: Модуль для работы с базой данных Postgres.
en: Module for working with the Postgres database.
"""
import psycopg2

from src.database.base_db import BaseDB


class PostgresDB(BaseDB):
    """
    ru: Класс для работы с базой данных Postgres.
    """

    def __init__(self, dbname: str, user: str, password: str, host: str, port: int):
        """
        ru: Инициализация класса.
        """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.__connection = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    @staticmethod
    def _get_fields_str(fields: dict) -> str:
        """
        ru: Получение строки с полями.
        """
        return ", ".join([f"{key} {value}" for key, value in fields.items()])

    def _query(self, *args):
        """
        ru: Метод запроса.
        """
        with self.__connection.cursor() as cursor:
            cursor.execute(*args)
            self.__connection.commit()

    def _query_fetchall(self, *args) -> list:
        """
        ru: Метод запроса с возвратом данных.
        """
        with self.__connection.cursor() as cursor:
            cursor.execute(*args)
            result = cursor.fetchall()
        return result

    def _query_fetchone(self, *args) -> any:
        """
        ru: Метод запроса с возвратом одной строки.
        """
        with self.__connection.cursor() as cursor:
            cursor.execute(*args)
            result = cursor.fetchone()
        return result[0]

    def check_value(self, table_name: str, key_name: str, value: any) -> bool:
        """
        ru: Проверка наличия значения в таблице.
        """
        return bool(self._query_fetchall(f"SELECT * FROM {table_name} WHERE {key_name} = '{value}'"))

    def create_table(self, table_name: str, fields: dict):
        """
        ru: Метод для создания таблицы.
        """
        self._query(f"CREATE TABLE IF NOT EXISTS {table_name} ({self._get_fields_str(fields)})")

    def drop_table(self, table_name: str):
        """
        ru: Удаление таблицы.
        """
        self._query(f"DROP TABLE IF EXISTS {table_name}")

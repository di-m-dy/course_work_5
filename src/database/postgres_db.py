"""
ru: Модуль для работы с базой данных Postgres.
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
        self.__connection = None

    def _get_connection(self):
        """
        ru: Получение соединения.
        """
        if self.__connection is None:
            self.__connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
        return self.__connection

    @staticmethod
    def _get_fields_str(fields: dict) -> str:
        """
        ru: Получение строки с полями.
        """
        return ", ".join([f"{key} {value}" for key, value in fields.items()])

    def _query(self, query: str):
        """
        ru: Метод запроса.
        """
        connection = self._get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()

    def _query_fetchall(self, query: str) -> list:
        """
        ru: Метод запроса с возвратом данных.
        """
        connection = self._get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

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

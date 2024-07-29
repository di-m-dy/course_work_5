"""
ru: Базовый класс для работы с базой данных.
"""
from abc import ABC, abstractmethod


class BaseDB(ABC):
    """
    ru: Абстрактный класс для работы с базой данных.
    en: Abstract class for working with the database.
    """

    @staticmethod
    @abstractmethod
    def _get_fields_str(fields: dict) -> str:
        pass

    @abstractmethod
    def _query(self, query: str):
        pass

    @abstractmethod
    def _query_fetchall(self, query: str) -> list:
        pass

    @abstractmethod
    def create_table(self, table_name: str, fields: dict):
        pass

    @abstractmethod
    def drop_table(self, table_name: str):
        pass

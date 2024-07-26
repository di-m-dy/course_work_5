"""
ru: Модуль для работы с базой данных.
"""
from src.database.postgres_db import PostgresDB


class DBManager(PostgresDB):
    """
    Менеджер базы данных.
    """

    def __init__(self, dbname: str, user: str, password: str, host: str, port: int):
        """
        Инициализация класса.
        """
        super().__init__(dbname, user, password, host, port)

    def create_tables(self):
        """
        ru: Создание таблиц.
        """
        pass

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием:
            - название компании
            - название вакансии
            - зарплата
            - ссылка на вакансию
        """
        pass

    def get_companies_and_vacancies_count(self):
        """
        Список компаний и количество вакансий у каждой.
        """
        pass

    def get_avg_salary(self):
        """
        ru: Получение средней зарплаты.
        """
        pass

    def get_vacancies_with_higher_salary(self):
        """
        ru: Получение вакансий с зарплатой выше средней.
        """
        pass

    def get_vacancies_with_keyword(self, keyword: str):
        """
        ru: Получение вакансий по ключевому слову.
        """
        pass

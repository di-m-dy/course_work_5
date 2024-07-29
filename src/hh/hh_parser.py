"""
ru: Модуль для работы с запросами к API hh.ru.
"""

import datetime

from src.bases.base_parser import ApiFindBase, ApiInfoBase
from src.bases.base_parser_exceptions import AttrValueRestrictionError

# API URL
SCOPES = {
    "find_vacancies": "https://api.hh.ru/vacancies",
    "find_employers": "https://api.hh.ru/employers",
    "info_vacancy": "https://api.hh.ru/vacancies",
    "info_employer": "https://api.hh.ru/employers",
    "dictionaries": "https://api.hh.ru/dictionaries"
}

# API HEADERS
HEADERS = {"User-Agent": "HH-User-Agent"}

class HHDictionaries(ApiFindBase):
    """
    ru: Класс для получения словарей.
    en: Class for getting dictionaries.
    """

    def __init__(self):
        self.scope = SCOPES["dictionaries"]
        self.headers = HEADERS
        super().__init__(self.scope, self.headers)

    def find(
            self,
            locale: str = "RU",
            host: str = "hh.ru"
    ) -> dict:
        """
        ru: Метод для получения словарей с параметрами
        en: Method for setting request parameters.

        :param locale: string, Локализация
        :param host: string, Хост
        """
        return super().find(locale=locale, host=host)


class HHFindVacancy(ApiFindBase):
    """
    ru: Класс для поиска вакансий.
    en: Class for searching for vacancies.
    """

    def __init__(self):
        self.scope = SCOPES["find_vacancies"]
        self.headers = HEADERS
        super().__init__(self.scope, self.headers)

    def find(
            self,
            per_page: int = 10,
            page: int = 0,
            text: str = None,
            search_field: str = None,
            experience: str = None,
            employment: str = None,
            schedule: str = None,
            area: str = None,
            industry: str = None,
            employer_id: int = None,
            currency: int = None,
            salary: int = None,
            label: str = None,
            only_with_salary: bool = False,
            period: int = None,
            date_from: str = None,
            date_to: str = None,
            top_lat: float = None,
            bottom_lat: float = None,
            left_lng: float = None,
            right_lng: float = None,
            order_by: str = None,
            sort_point_lat: float = None,
            sort_point_lng: float = None,
            clusters: bool = False,
            describe_arguments: bool = False,
            no_magic: bool = False,
            premium: bool = False,
            responses_count_enabled: bool = False,
            part_time: str = None,
            accept_temporary: bool = False,
            locale: str = "RU",
            host: str = "hh.ru"
    ) -> dict:
        """
        ru: Метод поиска с параметрами запроса
        en: Search method with request parameters

        :param per_page: integer <= 100, Количество элементов на странице
        :param page: integer, Количество страниц
        :param text: string, Текст поиска
        :param search_field: string, Поиск по полям (если не указано, то по всем полям)
        :param experience: string, Опыт работы (по id - https://api.hh.ru/dictionaries)
        :param employment: string, Тип занятости (по id - https://api.hh.ru/dictionaries)
        :param schedule: string, График работы (по id - https://api.hh.ru/dictionaries)
        :param area: string, Локация (по id - https://api.hh.ru/areas)
        :param industry: string, Отрасль (по id - https://api.hh.ru/dictionaries)
        :param employer_id: string, Id работодателя
        :param currency: string, Валюта (по id - https://api.hh.ru/dictionaries)
        :param salary: string, Зарплата
        :param label: string, Метка (по id - https://api.hh.ru/dictionaries)
        :param only_with_salary: boolean, Только с зарплатой
        :param period: integer, Период публикации вакансии
        :param date_from: string, Дата, ограничивающая диапазон дат публикации вакансий снизу
        :param date_to: string, Дата, ограничивающая диапазон дат публикации вакансий сверху
        :param top_lat: float, Верхняя широта границы. В адресе вакансии используется.
        :param bottom_lat: float, Нижняя широта границы. В адресе вакансии используется.
        :param left_lng: float, Левая долгота границы. В адресе вакансии используется.
        :param right_lng: float, Правая долгота границы. В адресе вакансии используется.
        :param order_by: string, Сортировка (по id - https://api.hh.ru/dictionaries)
        :param sort_point_lat: float, Для сортировки по удаленности - широта
        :param sort_point_lng: float, Для сортировки по удаленности - долгота
        :param clusters: boolean, Кластеры
        :param describe_arguments: boolean, Описать аргументы  # TODO: Использовать в клиентском коде для коллбеков
        :param no_magic: boolean,
        :param premium: boolean, Премиум вакансии
        :param responses_count_enabled: boolean, Количество откликов
        :param part_time: string, Частичная занятость
        :param accept_temporary: boolean, Принимаются временные вакансии
        :param locale: string, Локализация
        :param host: string, Хост
        """
        if not 1 <= per_page <= 100:
            raise AttrValueRestrictionError()
        return super().find(
            per_page=per_page,
            page=page,
            text=text,
            search_field=search_field,
            experience=experience,
            employment=employment,
            schedule=schedule,
            area=area,
            industry=industry,
            employer_id=employer_id,
            currency=currency,
            salary=salary,
            label=label,
            only_with_salary=only_with_salary,
            period=period,
            date_from=date_from,
            date_to=date_to,
            top_lat=top_lat,
            bottom_lat=bottom_lat,
            left_lng=left_lng,
            right_lng=right_lng,
            order_by=order_by,
            sort_point_lat=sort_point_lat,
            sort_point_lng=sort_point_lng,
            clusters=clusters,
            describe_arguments=describe_arguments,
            no_magic=no_magic,
            premium=premium,
            responses_count_enabled=responses_count_enabled,
            part_time=part_time,
            accept_temporary=accept_temporary,
            locale=locale,
            host=host
        )


class HHFindEmployer(ApiFindBase):
    """
    ru: Класс для поиска работодателей.
    en: Class for searching for employers.
    """

    def __init__(self):
        self.scope = SCOPES["find_employers"]
        self.headers = HEADERS
        super().__init__(self.scope)

    def find(
            self,
            text: str = None,
            area: str = None,
            type_: str = None,
            only_with_vacancies: bool = False,
            sort_by: str = None,
            page: int = 0,
            per_page: int = 10,
            locale: str = "RU",
            host: str = "hh.ru"
    ):
        """
        ru: Метод поиска с параметрами запроса.
        en: Search method with request parameters.

        :param text: string, Текст поиска
        :param area: string, Локация (по id - https://api.hh.ru/areas)
        :param type_: string, Тип работодателя (по id - https://api.hh.ru/dictionaries)
        :param only_with_vacancies: boolean, Только с вакансиями
        :param sort_by: string, Сортировка по имени или по открытым вакансиям
        :param page: integer, Номер страницы
        :param per_page: integer, Количество элементов на странице
        :param locale: string, Локализация
        :param host: string, Хост
        """
        return super().find(
            text=text,
            area=area,
            type_=type_,
            only_with_vacancies=only_with_vacancies,
            sort_by=sort_by,
            page=page,
            per_page=per_page,
            locale=locale,
            host=host
        )


class HHInfoVacancy(ApiInfoBase):
    """
    ru: Класс для запроса информации о вакансии.
    en: Class for requesting information about a vacancy.
    """

    def __init__(self, id_: str):
        """
        :param id_: integer, Id вакансии
        """
        self.id_ = id_
        self.scope = SCOPES["info_vacancy"]
        self.headers = HEADERS
        super().__init__(self.scope, id_, self.headers)

    def info(
            self,
            locale: str = "RU",
            host: str = "hh.ru"
    ) -> dict:
        """
        ru: Метод для возврата информации о вакансии с параметрами
        en: Method for setting request parameters.

        :param locale: string, Locale
        :param host: string, Host
        """
        return super().info(self.id_, locale=locale, host=host)


class HHInfoEmployer(ApiInfoBase):
    """
    ru: Класс для запроса информации о работодателе.
    en: Class for requesting information about an employer.
    """

    def __init__(self, id_: str):
        self.id_ = id_
        self.scope = SCOPES["info_employer"]
        self.headers = HEADERS
        super().__init__(self.scope, id_, self.headers)

    def info(
            self,
            locale: str = "RU",
            host: str = "hh.ru"
    ) -> dict:
        """
        ru: Метод для возврата информации о работодателе с параметрами
        en: Method for setting request parameters.

        :param locale: string, Locale
        :param host: string, Host
        """
        return super().info(self.id_, locale=locale, host=host)


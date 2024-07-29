"""
ru: Абстрактный класс для парсинга данных.
en: Abstract class for parsing data.
"""

from abc import ABC, abstractmethod
import requests

from src.bases.base_parser_exceptions import ApiQueryError


class Api(ABC):
    """
    ru: Абстрактный класс для работы с API.
        Определяет общий для всех дочерних классов метод запроса.
    en: Abstract class for working with API.
        Defines a common method for all child classes to request.
    """

    @abstractmethod
    def _query(self):
        pass


class ApiBase(Api):
    """
    ru: Базовый класс для работы с API.
        Определяет метод запроса и проверки ответа.
        Рекомендуется использовать для наследования, но можно использовать и самостоятельно.
    en: Base class for working with API.
        Defines the request method and response check.
        It is recommended to use for inheritance, but you can use it independently.
    """

    def __init__(self, scope: str, headers: dict = None):
        """
        ru: Инициализация класса.
        en: Class initialization.
        :param scope: request scope
        """
        self.scope = scope
        self.headers = headers or {}
        self.__parameters = {}

    @property
    def parameters(self) -> dict:
        """
        ru: Свойства параметров
        en: Property of parameters
        :return: dict
        """
        return self.__parameters

    @parameters.setter
    def parameters(self, value: dict):
        """
        ru: Свойства параметров
        en: Property of parameters
        :param value: dict
        """
        self.__parameters = value

    def _query(self) -> dict:
        """
        ru: Метод запроса.
        en: Request method.
        :return: dict
        """
        response = requests.get(
            self.scope,
            headers=self.headers,
            params=self.parameters
        )
        status = response.status_code
        if status == 200:
            return response.json()
        else:
            type_ = response.reason
            url = response.url
            raise ApiQueryError(f"«{url}»: [{status}] {type_}")


class ApiFindBase(ApiBase):
    """
    ru: Базовый класс для работы с API поиска.
        Определяет методы для поиска.
    en: Base class for working with search API.
        Defines methods for searching.
    """

    def __init__(self, scope: str, headers: dict = None):
        self.headers = headers or {}
        super().__init__(scope, self.headers)

    def find(self, **kwargs) -> dict:
        """
        ru: Метод поиска.
        en: Search method.
        :return: dict
        """
        self.parameters = kwargs
        return self._query()


class ApiInfoBase(ApiBase):
    def __init__(self, scope, id_, headers=None):
        self.headers = headers or {}
        super().__init__(f"{scope}/{id_}", headers)

    def info(self, id_: int | str, **kwargs) -> dict:
        self.parameters = kwargs
        return self._query()

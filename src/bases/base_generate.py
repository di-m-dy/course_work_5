"""
ru: Базовый класс для генерации списка объектов из API.
en: Base class for generating a list of objects from the API.
"""
from abc import ABC, abstractmethod

from src.bases.base_objects import JobObject


class GenerateObjectsListBase(ABC):
    """
    ru: Абстрактный класс для генерации списка объектов.
    en: Abstract class for generating a list of objects.
    """

    @abstractmethod
    def get_object(self):
        pass

    @abstractmethod
    def generate(self):
        pass


class GenerateObjectsList(GenerateObjectsListBase):
    """
    ru: Класс для генерации списка объектов.
    en: Class for generating a list of objects.
    """

    def __init__(self, items: list[dict]):
        """
        ru: Инициализация класса.
        en: Class initialization.
        :param items: список словарей c данными / list of dictionaries with data
        """
        self.items = items

    def get_object(self):
        """
        ru: Фабричный метод для передачи нужного объекта
        en: Factory method for passing the required object
        """
        return JobObject

    def generate(self):
        """
        ru: Генерация списка объектов.
        en: Generating a list of objects.
        """
        return [self.get_object().create(**obj) for obj in self.items]

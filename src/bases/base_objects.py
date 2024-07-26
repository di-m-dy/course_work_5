"""
ru: Базовые объекты для проекта.
"""
from abc import ABC, abstractmethod


class JobObjectBase(ABC):
    @classmethod
    @abstractmethod
    def create(cls, **kwargs):
        pass


class JobObject(JobObjectBase):
    def __init__(self, **kwargs):
        self.__dict__ = self.rename_built_keys(**kwargs)

    @staticmethod
    def rename_built_keys(**kwargs) -> dict:
        """
        ru: Переименование ключей, если они совпадают с ключевыми словами Python.
        en: Renaming keys if they match Python keywords.
        """
        arguments = {}
        builtins_names = ["id", "type", "from"]
        for key in kwargs.keys():
            if key in builtins_names:
                arguments[f"{key}_"] = kwargs[key]
            else:
                arguments[key] = kwargs[key]
        return arguments

    @classmethod
    def create(cls, **kwargs):
        """
        ru: Создание объекта.
        en: Object creation.
        """
        return cls(**cls.rename_built_keys(**kwargs))

    def get_dict(self) -> dict:
        """
        ru: Получение словаря аттрибутов объекта.
        en: Getting a dictionary of object attributes.
        """
        built_keys = ["id_", "type_", "from_"]
        result = {}
        for key in self.__dict__.keys():
            if key.startswith("_"):
                continue
            if key in built_keys:
                result[key[:-1]] = self.__dict__[key]
            else:
                result[key] = self.__dict__[key]
        return result

"""
ru: Модуль для генерации списков объектов из базы данных.
"""
from src.bases.base_generate import GenerateObjectsList
from src.hh.hh_objects import HHVacancy, HHEmployer


class HHGenerateVacanciesList(GenerateObjectsList):
    """
    ru: Класс для генерации списка объектов вакансий.
    en: Class for generating a list of vacancy objects.
    """

    def __init__(self, items: list[dict]):
        """
        :param items: list, Список словарей с параметрами вакансий
        """
        # валидация словарей / validation of dictionaries
        valid_items = []
        for item in items:
            new_dict = {
                "id_": item["id"],
                "name": item["name"],
                "created_at": item["created_at"],
                "published_at": item["published_at"],
                "alternate_url": item["alternate_url"],
                "employer": item["employer"],
                "salary": item["salary"],
                "area": item["area"],
                "experience": item["experience"],
                "employment": item["employment"],
                "schedule": item["schedule"],
                "description": item.get("description")
            }
            valid_items.append(new_dict)
        super().__init__(valid_items)

    def get_object(self):
        """
        ru: Фабричный метод для создания объекта вакансии.
        en: Factory method for creating a vacancy object.
        """
        return HHVacancy


class HHGenerateEmployersList(GenerateObjectsList):
    """
    ru: Класс для генерации списка объектов работодателей.
    en: Class for generating a list of employer objects.
    """

    def __init__(self, items: list[dict]):
        """
        :param items: list, Список словарей с параметрами работодателей
        """
        # валидация словарей / validation of dictionaries
        valid_items = []
        for item in items:
            new_dict = {
                "id_": item["id"],
                "name": item["name"],
                "alternate_url": item["alternate_url"],
                "logo_urls": item.get("logo_urls"),
                "accredited_it_employer": item.get("accredited_it_employer"),
                "description": item.get("description"),
                "site_url": item.get("site_url")
            }
            valid_items.append(new_dict)
        super().__init__(items)

    def get_object(self):
        """
        ru: Фабричный метод для создания объекта работодателя.
        en: Factory method for creating an employer object.
        """
        return HHEmployer

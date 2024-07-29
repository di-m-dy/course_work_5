"""
ru: Модуль cli интерфейса для приложения
"""
import os

import html2text

from src.app.hh_database import DBManager
from src.bases.base_parser_exceptions import ApiQueryError
from src.hh.hh_generate import HHGenerateVacanciesList, HHGenerateEmployersList
from src.hh.hh_objects import HHVacancy, HHEmployer
from src.hh.hh_parser import HHFindVacancy, HHFindEmployer, HHInfoVacancy, HHInfoEmployer
from src.ui.ui_cli import WidgetCLI, WidgetCLIField


class UserInterface:
    """
    ru: Класс для работы с пользовательским интерфейсом программы
    en: Class for working with the user interface of the program
    """

    def __init__(self):
        # объекты для работы с API hh.ru
        self.find_vacancy = HHFindVacancy()
        self.find_employer = HHFindEmployer()
        # обработка html в текст
        self.convert_html = html2text.HTML2Text()
        # объекты для работы с базой данных
        self.db = DBManager()
        self.db.create_tables()

    def start(self):
        """
        ru: Главное меню программы.
        en: Main program menu.
        """
        header = "[HH] parser (author: di-m-dy)"
        description = """UI CLI для работы с API hh.ru

Выберите вариант работы:
<online> - напрямую запрос на сервер
<local> - работа с локальной базой данных

Hint: 
— в [] указана клавиша для действия
— [exit] в любом месте программы закрывает ее
        """
        items = [
            {"text": "ОНЛАЙН", "action": self.menu_online, "args": {}},
            {"text": "ЛОКАЛЬНО", "action": self.menu_local, "args": {}},
        ]
        footer = [
            {"key": "exit", "text": "выйти", "action": WidgetCLI.stop, "args": {}}
        ]
        widget = WidgetCLI(header, description, items, footer)
        widget.show()

    def menu_online(self):
        """
        ru: Онлайн меню программы.
        en: Online program menu.
        """
        header = "[О]нлайн [М]еню"
        description = "Выберите вариант поиска:"
        items = [
            {"text": "Поиск вакансий", "action": self.find_vacancy_online, "args": {}},
            {"text": "Поиск работодателей", "action": self.quick_search_employer, "args": {}},
        ]
        footer = [
            {"key": "<", "text": "назад", "action": self.start, "args": {}}
        ]
        widget = WidgetCLI(header, description, items, footer)
        widget.show()

    def menu_local(self):
        """
        ru: Локальное меню программы.
        en: Local program menu.
        """
        header = "[Л]окальное [М]еню"
        description = "Выберите действие:"
        items = [
            {"text": "Список вакансий", "action": self.find_vacancy_local, "args": {}},
            {"text": "Список работодателей", "action": self.find_employer_local, "args": {}},
        ]
        footer = [
            {"key": "<", "text": "назад", "action": self.start, "args": {}}
        ]
        widget = WidgetCLI(header, description, items, footer)
        widget.show()

    def find_vacancy_online(self):
        """
        ru: Поиск вакансий онлайн.
        en: Online job search.
        """
        header = "[П]оиск [В]акансий [О]нлайн"
        description = """Выберите вариант поиска:

Подсказка:
<быстрый> - общий поиск по тексту
<параметры> - поиск с параметрами
        """
        items = [
            {"text": "Быстрый поиск", "action": self.quick_search_menu, "args": {}},
            {"text": "Параметры поиска", "action": self.advanced_search_vacancy, "args": {}},
        ]
        footer = [
            {"key": "<", "text": "назад", "action": self.menu_online, "args": {}}
        ]
        widget = WidgetCLI(header, description, items, footer)
        widget.show()

    def quick_search_menu(self):
        """
        ru: Быстрый поиск ваканcий онлайн.
        en: Quick job search online.
        """
        header = "[Б]ыстрый [П]оиск"
        description = "Введите название вакансии:"
        widget = WidgetCLIField(header, description, self.online_search_vacancy)
        widget.show()

    def online_search_vacancy(self, text: str, page: int = 0, **kwargs):
        """
        ru: Запрос и отбражение вакансий онлайн.
        en: Request and display jobs online.
        """
        try:
            data = self.find_vacancy.find(text=text, page=page, **kwargs)
        except ConnectionError as e:
            os.system("clear")
            input(f"Проблема с интернетом. Нажмите любую клавишу")
            self.find_vacancy_online()
        except ApiQueryError as e:
            os.system("clear")
            input(f"{e}. Нажмите любую клавишу.")
            self.find_vacancy_online()
        except Exception as e:
            os.system("clear")
            input(f"{e}. Нажмите любую клавишу.")
            self.find_vacancy_online()
        additional = kwargs
        vacancies = data["items"]
        page = data["page"]
        pages = data["pages"]
        found = data["found"]
        obj_list = HHGenerateVacanciesList(vacancies).generate()
        header = f"Результаты поиска вакансий '{text}':"
        description = f"Найдено {found} вакансий.\n{page + 1} страница из {pages}.\nВыберите вакансию для просмотра."
        items = [
            {
                "text": f"{str(obj)}\n{str(obj.salary)}\n{str(obj.employer)}",
                "action": self.show_info_vacancy,
                "args": {"vacancy": obj, "text": text, "page": page}
            } for obj in obj_list
        ]

        next_page = {
            "key": ">>",
            "text": "следующая страница",
            "action": self.online_search_vacancy,
            "args": {"page": page + 1, "text": text} | additional
        }
        prev_page = {
            "key": "<<",
            "text": "предыдущая страница",
            "action": self.online_search_vacancy,
            "args": {"page": page - 1, "text": text} | additional
        }
        footer = [
            {"key": "q", "text": "выйти", "action": self.find_vacancy_online, "args": {}},
            {
                "key": "s",
                "text": "сохранить страницу",
                "action": self.save_page_vacancies,
                "args": {"vacancies": obj_list, "page": page, "text": text} | additional
            }
        ]
        if page > 0:
            footer.append(prev_page)
        if page < pages:
            footer.append(next_page)
        widget = WidgetCLI(header, description, items, footer)
        widget.show()

    def show_info_vacancy(self, vacancy: HHVacancy, **kwargs):
        try:
            vacancy_info = HHInfoVacancy(vacancy.id_).info()
        except ConnectionError as e:
            os.system("clear")
            input(f"Проблема с интернетом. Нажмите любую клавишу")
            self.online_search_vacancy(**kwargs)
        except ApiQueryError as e:
            os.system("clear")
            input(f"{e}. Нажмите любую клавишу.")
            self.online_search_vacancy(**kwargs)
        except Exception as e:
            os.system("clear")
            input(f"{e}. Нажмите любую клавишу.")
            self.online_search_vacancy(**kwargs)
        self.save_vacancy_info(vacancy, vacancy_info["description"])
        vacancy_description = self.html2txt(vacancy_info["description"])
        salary = f"Зарплата: {str(vacancy.salary) if vacancy.salary else 'не указана'}"
        employer = f"Работодатель: {str(vacancy.employer)}"
        header = f"Информация о вакансии «{vacancy.name}»:"
        description = f"{salary}\n{employer}\n\n{vacancy_description}"
        footer = [
            {
                "key": "<",
                "text": "назад",
                "action": self.online_search_vacancy,
                "args": kwargs
            }
        ]
        widget = WidgetCLI(header=header, description=description, footer=footer)
        widget.show()

    def save_page_vacancies(self, vacancies: list[HHVacancy], **kwargs):
        print("Сохранение данных...")
        page = kwargs.get("page", 0)
        for vacancy in vacancies:
            self.db.add_vacancy(vacancy)
        header = "Сохранение данных"
        description = f"Страница [{page + 1}] сохранена в базу данных."
        footer = [
            {
                "key": "<",
                "text": "назад",
                "action": self.online_search_vacancy,
                "args": kwargs}
        ]
        widget = WidgetCLI(header=header, description=description, footer=footer)
        widget.show()

    def advanced_search_vacancy(self):
        """
        ru: Поиск вакансий с параметрами.
        en: Search for vacancies with parameters.
        """
        parameters = {}
        header = "[П]араметры [П]оиска"
        # step 1 name
        description = "Введите название вакансии:"
        widget = WidgetCLIField(
            header=header,
            description=description,
            callback=lambda x: parameters.update({"text": x})
        )
        widget.show()
        # step 2 salary
        description = "Показать вакансии только с указанной зарплатой?"
        items = [
            {"text": "Да", "action": lambda: parameters.update({"only_with_salary": True}), "args": {}},
            {"text": "Нет", "action": lambda: parameters.update({"only_with_salary": False}), "args": {}},
        ]
        widget = WidgetCLI(header=header, description=description, items=items)
        widget.show()
        # step 3 schedule
        description = "Выберите график работы:"
        items = [
            {"text": "Полный день", "action": lambda: parameters.update({"schedule": "fullDay"}), "args": {}},
            {"text": "Сменный график", "action": lambda: parameters.update({"schedule": "shift"}), "args": {}},
            {"text": "Гибкий график", "action": lambda: parameters.update({"schedule": "flexible"}), "args": {}},
            {"text": "Удаленная работа", "action": lambda: parameters.update({"schedule": "remote"}), "args": {}},
            {"text": "Вахтовый метод", "action": lambda: parameters.update({"schedule": "flyInFlyOut"}), "args": {}}
        ]
        widget = WidgetCLI(header=header, description=description, items=items)
        widget.show()
        # step 4 experience
        description = "Выберите опыт работы:"
        items = [
            {"text": "Нет опыта", "action": lambda: parameters.update({"experience": "noExperience"}), "args": {}},
            {
                "text": "От 1 года до 3 лет",
                "action": lambda: parameters.update({"experience": "between1And3"}),
                "args": {}
            },
            {"text": "От 3 до 6 лет", "action": lambda: parameters.update({"experience": "between3And6"}), "args": {}},
            {"text": "Более 6 лет", "action": lambda: parameters.update({"experience": "moreThan6"}), "args": {}}
        ]
        widget = WidgetCLI(header=header, description=description, items=items)
        widget.show()
        # step 5 employment
        description = "Выберите тип занятости:"
        items = [
            {"text": "Полная занятость", "action": lambda: parameters.update({"employment": "full"}), "args": {}},
            {"text": "Частичная занятость", "action": lambda: parameters.update({"employment": "part"}), "args": {}},
            {"text": "Проектная работа", "action": lambda: parameters.update({"employment": "project"}), "args": {}},
            {"text": "Стажировка", "action": lambda: parameters.update({"employment": "probation"}), "args": {}},
            {"text": "Волонтёрство", "action": lambda: parameters.update({"employment": "volunteer"}), "args": {}}
        ]
        widget = WidgetCLI(header=header, description=description, items=items)
        widget.show()

        self.online_search_vacancy(**parameters)

    def quick_search_employer(self):
        """
        ru: Быстрый поиск работодателя.
        en: Quick search for employer.
        """
        header = "[Б]ыстрый [П]оиск"
        description = "Введите название работодателя:"
        widget = WidgetCLIField(header, description, self.online_search_employer)
        widget.show()

    def online_search_employer(self, text: str, page: int = 0, **kwargs):
        try:
            data = self.find_employer.find(text=text, page=page, **kwargs)
        except ConnectionError as e:
            os.system("clear")
            input(f"Проблема с интернетом. Нажмите любую клавишу")
            self.menu_online()
        except ApiQueryError as e:
            os.system("clear")
            input(f"{e}. Нажмите любую клавишу.")
            self.menu_online()
        except Exception as e:
            os.system("clear")
            input(f"{e}. Нажмите любую клавишу.")
            self.menu_online()
        employers = data["items"]
        page = data["page"]
        pages = data["pages"]
        found = data["found"]
        obj_list = HHGenerateEmployersList(employers).generate()
        header = f"Результаты поиска работодателей '{text}':"
        description = (f"Найдено {found} работодателей.\n{page + 1}"
                       f" страница из {pages}.\nВыберите работодателя для просмотра.")
        items = [
            {
                "text": str(obj),
                "action": self.show_info_employer,
                "args": {"employer": obj, "text": text, "page": page}
            } for obj in obj_list
        ]

        next_page = {
            "key": ">>",
            "text": "следующая страница",
            "action": self.online_search_employer,
            "args": {"page": page + 1, "text": text} | kwargs
        }
        prev_page = {
            "key": "<<",
            "text": "предыдущая страница",
            "action": self.online_search_employer,
            "args": {"page": page - 1, "text": text} | kwargs
        }
        footer = [
            {"key": "q", "text": "выйти", "action": self.menu_online, "args": {}},
            {
                "key": "s",
                "text": "сохранить страницу",
                "action": self.save_page_employers,
                "args": {"employers": obj_list, "page": page, "text": text} | kwargs}
        ]
        if page > 0:
            footer.append(prev_page)
        if page < pages:
            footer.append(next_page)
        widget = WidgetCLI(header, description, items, footer)
        widget.show()

    def show_info_employer(self, employer: HHEmployer, **kwargs):
        try:
            employer_info = HHInfoEmployer(employer.id_).info()
        except ConnectionError as e:
            os.system("clear")
            input(f"Проблема с интернетом. Нажмите любую клавишу")
            self.online_search_employer(**kwargs)
        except ApiQueryError as e:
            os.system("clear")
            input(f"{e}. Нажмите любую клавишу.")
            self.online_search_employer(**kwargs)
        except Exception as e:
            os.system("clear")
            input(f"{e}. Нажмите любую клавишу.")
            self.online_search_employer(**kwargs)
        employer_description = self.html2txt(employer_info["description"])
        header = f"Информация о работодателе «{employer.name}»:"
        description = f"{employer_description}"
        footer = [
            {
                "key": "<",
                "text": "назад",
                "action": self.online_search_employer,
                "args": kwargs
            }
        ]
        widget = WidgetCLI(header=header, description=description, footer=footer)
        widget.show()

    def save_page_employers(self, employers: list[HHEmployer], **kwargs):
        print("Сохранение данных...")
        page = kwargs.get("page", 0)
        for employer in employers:
            self.db.add_employer(employer)
        header = "Сохранение данных"
        description = f"Страница [{page + 1}] сохранена в базу данных."
        footer = [
            {
                "key": "<",
                "text": "назад",
                "action": self.online_search_employer,
                "args": kwargs
            }
        ]
        widget = WidgetCLI(header=header, description=description, footer=footer)
        widget.show()

    def find_vacancy_local(self, page: int = 0):
        """
        ru: Вывод вакансий из локальной базы данных.
            Разбивка по 10 вакансий на страницу.
        en: Output of vacancies from a local database.
            Breakdown by 10 vacancies per page.
        """
        vacancies = self.db.get_vacancies_objects()
        pages = len(vacancies) // 10
        obj_list = [vacancy for vacancy in vacancies[page * 10:page * 10 + 10]]
        header = "Список вакансий:"
        description = f"Страница {page + 1} из {pages + 1}."
        items = [
            {
                "text": f"Вакансия: {str(obj.name)}\n Зарплата: {str(obj.salary)}\n Работодатель: {str(obj.employer)}",
                "action": self.show_info_vacancy_local,
                "args": {"vacancy": obj, "page": page}
            } for obj in obj_list
        ]
        next_page = {
            "key": ">>",
            "text": "следующая страница",
            "action": self.find_vacancy_local,
            "args": {"page": page + 1}
        }
        prev_page = {
            "key": "<<",
            "text": "предыдущая страница",
            "action": self.find_vacancy_local,
            "args": {"page": page - 1}
        }
        footer = [
            {"key": "q", "text": "выйти", "action": self.menu_local, "args": {}}
        ]
        if 0 < page < pages:
            footer.append(prev_page)
        if page < pages:
            footer.append(next_page)

        widget = WidgetCLI(header=header, description=description, items=items, footer=footer)
        widget.show()

    def show_info_vacancy_local(self, vacancy: HHVacancy, page: int):
        if not vacancy.description:
            try:
                vacancy_info = HHInfoVacancy(vacancy.id_).info()
                vacancy.description = vacancy_info["description"]
                self.save_vacancy_info(vacancy, vacancy_info["description"])
            except ConnectionError as e:
                vacancy.description = "Проблема с интернетом. Попробуйте позже."
            except ApiQueryError as e:
                vacancy.description = f"{e}. Попробуйте позже."
            except Exception as e:
                vacancy.description = f"{e}. Попробуйте позже."
        header = f"Информация о вакансии «{vacancy.name}»:"
        description = f"Зарплата: {str(vacancy.salary) if vacancy.salary else 'не указана'}\n" \
                      f"Работодатель: {str(vacancy.employer)}\n\n{self.html2txt(vacancy.description)}"
        footer = [
            {
                "key": "<",
                "text": "назад",
                "action": self.find_vacancy_local,
                "args": {"page": page}
            }
        ]
        widget = WidgetCLI(header=header, description=description, footer=footer)
        widget.show()

    def find_employer_local(self, page: int = 0):
        """
        ru: Вывод работодателей из локальной базы данных.
            Разбивка по 10 работодателей на страницу.
        en: Output of employers from a local database.
            Breakdown by 10 employers per page.
        """
        employers = self.db.get_employers_objects()
        pages = len(employers) // 10
        obj_list = [employer for employer in employers[page * 10:page * 10 + 10]]
        header = "Список работодателей:"
        description = f"Страница {page + 1} из {pages + 1}."
        items = [
            {
                "text": str(obj),
                "action": self.show_info_employer_local,
                "args": {"employer": obj, "page": page}
            } for obj in obj_list
        ]
        next_page = {
            "key": ">>",
            "text": "следующая страница",
            "action": self.find_employer_local,
            "args": {"page": page + 1}
        }
        prev_page = {
            "key": "<<",
            "text": "предыдущая страница",
            "action": self.find_employer_local,
            "args": {"page": page - 1}
        }
        footer = [
            {"key": "q", "text": "выйти", "action": self.menu_local, "args": {}}
        ]
        if 0 < page < pages:
            footer.append(prev_page)
        if page < pages:
            footer.append(next_page)

        widget = WidgetCLI(header=header, description=description, items=items, footer=footer)
        widget.show()

    def show_info_employer_local(self, employer: HHEmployer, page: int):
        if not employer.description:
            try:
                employer_info = HHInfoEmployer(employer.id_).info()
                employer.description = employer_info["description"]
                self.save_employer_info(employer, employer_info["description"])
            except ConnectionError as e:
                employer.description = "Проблема с интернетом. Попробуйте позже."
            except ApiQueryError as e:
                employer.description = f"{e}. Попробуйте позже."
            except Exception as e:
                employer.description = f"{e}. Попробуйте позже."
        header = f"Информация о работодателе «{employer.name}»:"
        description = f"{self.html2txt(employer.description)}"
        footer = [
            {
                "key": "<",
                "text": "назад",
                "action": self.find_employer_local,
                "args": {"page": page}
            }
        ]
        widget = WidgetCLI(header=header, description=description, footer=footer)
        widget.show()

    def save_vacancy_info(self, vacancy: HHVacancy, description: str):
        """
        ru: Сохранение информации о вакансии в локальную базу данных.
        en: Saving information about a vacancy to a local database.
        """
        vacancy_id = vacancy.id_
        if not self.db.check_value('vacancy', 'id',  vacancy_id):
            self.db.add_vacancy(vacancy)
        else:
            self.db.update_values(
                table='vacancy',
                column='description',
                value=vacancy_id,
                ref_column='id',
                new_value=description
            )

    def save_employer_info(self, employer: HHEmployer, description: str):
        """
        ru: Сохранение информации о работодателе в локальную базу данных.
        en: Saving information about an employer to a local database.
        """
        employer_id = employer.id_
        if not self.db.check_value('employer', 'id', employer_id):
            self.db.add_employer(employer)
        else:
            self.db.update_values(
                table='employer',
                column='description',
                value=employer_id,
                ref_column='id',
                new_value=description
            )

    def html2txt(self, html: str):
        try:
            text = self.convert_html.handle(html)
        except AttributeError as e:
            text = html
        return text

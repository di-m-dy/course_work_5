"""
ru: Модуль для запуска приложений
"""
import os

import requests

from src.app.config import DEFAULT_EMPLOYERS_LIST
from src.app.hh_database import DBManager
from src.hh.hh_parser import HHFindVacancy, HHFindEmployer, HHInfoVacancy, HHInfoEmployer, HHDictionaries
from src.hh.hh_objects import (
    HHVacancy,
    HHEmployer,
    HHArea,
    HHExperience,
    HHEmployment,
    HHSchedule,
    HHSalary,
    HHEmployerUrlLogo, HHSalaryCurrency
)
from src.hh.hh_generate import HHGenerateVacanciesList, HHGenerateEmployersList


class TestParser:
    def __init__(self, emp_list: list = DEFAULT_EMPLOYERS_LIST):
        """
        ru: Инициализация класса
        :param dbname:
        :param host:
        :param port:
        :param user:
        :param password:
        """
        self.employer_list = emp_list
        self.dictionaries = HHDictionaries()
        self.db = DBManager()

    def update_dictionaries(self):
        data_dictionaries = self.dictionaries.find()
        for experience in data_dictionaries["experience"]:
            experience = HHExperience.create(
                id_=experience["id"],
                name=experience["name"]
            )
            if not self.db.check_value("experience", "id", experience.id_):
                self.db.add_experience(experience)
            else:
                self.db.update_values(
                    table="experience",
                    column="name",
                    new_value=experience.name,
                    ref_column="id",
                    value=experience.id_
                )

        for employment in data_dictionaries["employment"]:
            employment = HHEmployment.create(
                id_=employment["id"],
                name=employment["name"]
            )
            if not self.db.check_value("employment", "id", employment.id_):
                self.db.add_employment(employment)
            else:
                self.db.update_values(
                    table="employment",
                    column="name",
                    new_value=employment.name,
                    ref_column="id",
                    value=employment.id_
                )

        for schedule in data_dictionaries["schedule"]:
            schedule = HHSchedule.create(
                id_=schedule["id"],
                name=schedule["name"]
            )
            if not self.db.check_value("schedule", "id", schedule.id_):
                self.db.add_schedule(schedule)
            else:
                self.db.update_values(
                    table="schedule",
                    column="name",
                    new_value=schedule.name,
                    ref_column="id",
                    value=schedule.id_
                )

        for currency in data_dictionaries["currency"]:
            currency = HHSalaryCurrency.create(
                code=currency["code"],
                abbr=currency["abbr"],
                name=currency["name"],
                default=currency["default"],
                rate=currency["rate"],
                in_use=currency["in_use"]
            )
            if not self.db.check_value("currency", "code", currency.code):
                self.db.add_salary_currency(currency)
            else:
                self.db.update_values(
                    table="currency",
                    column="abbr",
                    new_value=currency.abbr,
                    ref_column="code",
                    value=currency.code,

                )
                self.db.update_values(
                    table="currency",
                    column="name",
                    new_value=currency.name,
                    ref_column="code",
                    value=currency.code,
                )
                self.db.update_values(
                    table="currency",
                    column="\"default\"",
                    new_value=currency.default,
                    ref_column="code",
                    value=currency.code,
                )
                self.db.update_values(
                    table="currency",
                    column="rate",
                    new_value=currency.rate,
                    ref_column="code",
                    value=currency.code,
                )
                self.db.update_values(
                    table="currency",
                    column="in_use",
                    new_value=currency.in_use,
                    ref_column="code",
                    value=currency.code,
                )

    def save_vacancies(self, url: str):
        """
        ru: Получение вакансий по ключевому слову
        """
        response = requests.get(url)
        data = response.json()["items"]
        for vacancy in HHGenerateVacanciesList(data).generate():
            self.db.add_vacancy(vacancy)

    def save_employers(self):
        """
        ru: Получение работодателей по ключевому слову
        """
        self.update_dictionaries()
        for employer in self.employer_list:
            data = HHInfoEmployer(employer).info()
            employer = HHEmployer.create(
                id_=data["id"],
                name=data["name"],
                alternate_url=data["alternate_url"],
                logo_urls=data["logo_urls"],
                accredited_it_employer=data["accredited_it_employer"],
                description=data["description"],
                site_url=data["site_url"],
                vacancies_url=data["vacancies_url"],
            )
            self.db.add_employer(employer)
            self.save_vacancies(employer.additional["vacancies_url"])

    def get_all_vacancies(self, count: int = 10):
        print("ДЕМОНСТРАЦИЯ РАБОТЫ МЕТОДА get_all_vacancies\n")
        print("Получение всех вакансий\n")
        data = self.db.get_all_vacancies()
        result = []
        for vacancy in data[:count]:
            employer = f"Работодатель: {vacancy[0]}\n"
            name = f"Вакансия: {vacancy[1]}\n"
            salary_sep = '-' if vacancy[3] and vacancy[2] else ''
            salary = f"Зарплата: {vacancy[2] if vacancy[2] else ''}{salary_sep}{vacancy[3] if vacancy[3] else ''}\n" if \
                vacancy[2] or vacancy[3] else ''
            currency = f"Валюта: {vacancy[4]}\n" if vacancy[4] else ''
            site = f"Ссылка: {vacancy[5]}\n"
            result.append(f"{employer}{name}{salary}{currency}{site}\n" + "-" * 20 + "\n")
        return '\n'.join(result)

    def get_companies_and_vacancies_count(self, count: int | None = None):
        print("ДЕМОНСТРАЦИЯ РАБОТЫ МЕТОДА get_companies_and_vacancies_count\n")
        print("Получение компаний и количества вакансий\n")
        data = self.db.get_companies_and_vacancies_count()
        result = []
        data = data[:count] if count else data
        for company in data[:count]:
            name = f"Компания: {company[0]}\n"
            count = f"Количество вакансий: {company[1]}\n"
            result.append(f"{name}{count}\n" + "-" * 20 + "\n")
        return '\n'.join(result)

    def get_avg_salary(self):
        print("ДЕМОНСТРАЦИЯ РАБОТЫ МЕТОДА get_avg_salary\n")
        print("Получение средней зарплаты\n")
        data = self.db.get_avg_salary()
        result = []
        for salary in data[-1]:
            avg = f"Средняя зарплата: {salary}\n"
            result.append(f"{avg}\n" + "-" * 20 + "\n")
        return '\n'.join(result)

    def get_vacancies_with_higher_salary(self, count: int | None = None):
        print("ДЕМОНСТРАЦИЯ РАБОТЫ МЕТОДА get_vacancies_with_higher_salary\n")
        print("Получение вакансий с зарплатой выше средней\n")
        data = self.db.get_vacancies_with_higher_salary()
        result = []
        data = data[:count] if count else data
        for vacancy in data:
            employer = f"Работодатель: {vacancy[0]}\n"
            name = f"Вакансия: {vacancy[1]}\n"
            salary_sep = '-' if vacancy[3] and vacancy[2] else ''
            salary = f"Зарплата: {vacancy[2] if vacancy[2] else ''}{salary_sep}{vacancy[3] if vacancy[3] else ''}\n" if \
                vacancy[2] or vacancy[3] else ''
            currency = f"Валюта: {vacancy[4]}\n" if vacancy[4] else ''
            site = f"Ссылка: {vacancy[5]}\n"
            result.append(f"{employer}{name}{salary}{currency}{site}\n" + "-" * 20 + "\n")
        return '\n'.join(result)

    def get_vacancies_with_keyword(self, keyword: str, count: int | None = None):
        print("ДЕМОНСТРАЦИЯ РАБОТЫ МЕТОДА get_vacancies_with_keyword\n")
        print("Получение вакансий по ключевому слову\n")
        data = self.db.get_vacancies_with_keyword(keyword)
        result = []
        data = data[:count] if count else data
        for vacancy in data:
            employer = f"Работодатель: {vacancy[0]}\n"
            name = f"Вакансия: {vacancy[1]}\n"
            salary_sep = '-' if vacancy[3] and vacancy[2] else ''
            salary = f"Зарплата: {vacancy[2] if vacancy[2] else ''}{salary_sep}{vacancy[3] if vacancy[3] else ''}\n" if \
                vacancy[2] or vacancy[3] else ''
            currency = f"Валюта: {vacancy[4]}\n" if vacancy[4] else ''
            site = f"Ссылка: {vacancy[5]}\n"
            result.append(f"{employer}{name}{salary}{currency}{site}\n" + "-" * 20 + "\n")
        return '\n'.join(result)

    def commands_run(self):
        demo_get_all_vacancies = "[ 1 ] Вывести все вакансии"
        demo_get_companies_and_vacancies_count = "[ 2 ] Вывести компании и количество вакансий"
        demo_get_avg_salary = "[ 3 ] Вывести среднюю зарплату"
        demo_get_vacancies_with_higher_salary = "[ 4 ] Вывести вакансии с зарплатой выше средней"
        demo_get_vacancies_with_keyword = "[ 5 ] Вывести вакансии по ключевому слову"
        quit_command = "[ 0 ] Выйти"
        command_list = (f"{demo_get_all_vacancies}\n"
                        f"{demo_get_companies_and_vacancies_count}\n"
                        f"{demo_get_avg_salary}\n"
                        f"{demo_get_vacancies_with_higher_salary}\n"
                        f"{demo_get_vacancies_with_keyword}\n\n"
                        "Введите команду: "
                        )
        user_input = input(f"Выберите действие:\n{command_list}\n")
        if user_input == "1":
            print(self.get_all_vacancies())
            continue_command = input("Продолжить?\nВведите (y/n): ")
            if continue_command == "y":
                self.commands_run()
            return
        elif user_input == "2":
            print(self.get_companies_and_vacancies_count())
            continue_command = input("Продолжить?\nВведите (y/n): ")
            if continue_command == "y":
                self.commands_run()
            return
        elif user_input == "3":
            print(self.get_avg_salary())
            continue_command = input("Продолжить?\nВведите (y/n): ")
            if continue_command == "y":
                self.commands_run()
            return
        elif user_input == "4":
            print(self.get_vacancies_with_higher_salary())
            continue_command = input("Продолжить?\nВведите (y/n): ")
            if continue_command == "y":
                self.commands_run()
            return
        elif user_input == "5":
            keyword = input("Введите ключевое слово: ")
            print(self.get_vacancies_with_keyword(keyword))
            continue_command = input("Продолжить?\nВведите (y/n): ")
            if continue_command == "y":
                self.commands_run()
            return
        elif user_input == "0":
            return
        else:
            print("Некорректный ввод")
            continue_command = input("Продолжить?\nВведите (y/n): ")
            if continue_command == "y":
                self.commands_run()
            return

    def start(self):
        print("Идет загрузка данных...")
        self.db.create_tables()
        self.save_employers()
        os.system('clear')
        self.commands_run()


if __name__ == "__main__":
    app_test = TestParser()
    app_test.start()

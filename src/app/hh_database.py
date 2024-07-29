"""
ru: Модуль для работы с базой данных.
"""
from src.database.postgres_db import PostgresDB
from src.app.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER, DEFAULT_EMPLOYERS_LIST, SQL_SCRIPTS_PATH
from src.hh.hh_objects import (
    HHSchedule,
    HHExperience,
    HHEmployment,
    HHVacancy,
    HHArea,
    HHEmployer,
    HHEmployerUrlLogo,
    HHSalary,
    HHSalaryCurrency
)


class DBManager(PostgresDB):
    """
    Менеджер базы данных.
    """

    def __init__(self):
        """
        Инициализация класса.
        """
        dbname = DB_NAME
        user = DB_USER
        password = DB_PASSWORD
        host = DB_HOST
        port = DB_PORT
        super().__init__(dbname, user, password, host, port)
        self.create_tables()

    def create_tables(self):
        """
        ru: Создание таблиц.
        """
        with open(SQL_SCRIPTS_PATH) as file:
            self._query(file.read())

    def get_employers_objects(self) -> list[HHEmployer]:
        """
        ru: Получение объектов работодателей.
        """
        data = self._query_fetchall("SELECT "
                                    "e.id, e.name, "
                                    "e.alternate_url, e.accredited_it_employer, "
                                    "e.description, e.site_url, "
                                    "eul.original, eul.size_90, eul.size_240 "
                                    "FROM employer AS e "
                                    "LEFT JOIN employer_url_logo AS eul ON e.id = eul.employer_id")
        employers = []
        for employer in data:
            employer_url_logo = HHEmployerUrlLogo.create(**{
                "original": employer[6],
                "size_90": employer[7],
                "size_240": employer[8]
            })
            employers.append(HHEmployer.create(**{
                "id_": employer[0],
                "name": employer[1],
                "alternate_url": employer[2],
                "accredited_it_employer": employer[3],
                "description": employer[4],
                "site_url": employer[5],
                "logo_urls": employer_url_logo.get_dict()
            }))
        return employers

    def get_vacancies_objects(self) -> list[HHVacancy]:
        """
        ru: Получение объектов вакансий.
        """
        data = self._query_fetchall("SELECT "
                                    "v.id, v.name, v.created_at, v.published_at, v.alternate_url, "  # 0 - 4
                                    "v.employer_id, v.area_id, v.description, v.experience_id, v.employment_id, "  # 5 - 9
                                    "v.schedule_id, "  # 10
                                    "e.name, e.alternate_url, e.accredited_it_employer, e.description, e.site_url, "  # 11 - 15
                                    "a.id, a.name, a.url, "  # 16 - 18
                                    "ex.id, ex.name, "  # 19 - 20
                                    "em.id, em.name, "  # 21 - 22
                                    "sch.id, sch.name, "  # 23 - 24
                                    "s.from, s.to, s.currency_code, s.gross, "  # 25 - 28
                                    "c.code, c.abbr, c.name, c.default, c.rate, c.in_use, "  # 29 - 34
                                    "eul.original, eul.size_90, eul.size_240 "  # 35 - 37
                                    "FROM vacancy AS v "
                                    "LEFT JOIN employer AS e ON v.employer_id = e.id "
                                    "LEFT JOIN area AS a ON v.area_id = a.id "
                                    "LEFT JOIN experience AS ex ON v.experience_id = ex.id "
                                    "LEFT JOIN employment AS em ON v.employment_id = em.id "
                                    "LEFT JOIN schedule AS sch ON v.schedule_id = sch.id "
                                    "LEFT JOIN salary AS s ON v.id = s.vacancy_id "
                                    "LEFT JOIN currency AS c ON s.currency_code = c.code "
                                    "LEFT JOIN employer_url_logo AS eul ON e.id = eul.employer_id "
                                    "ORDER BY v.id")
        vacancies = []
        for vacancy in data:
            employer_url_logo = HHEmployerUrlLogo.create(**{
                "original": vacancy[35],
                "size_90": vacancy[36],
                "size_240": vacancy[37]
            })
            employer = HHEmployer.create(**{
                "id_": vacancy[5],
                "name": vacancy[11],
                "alternate_url": vacancy[12],
                "accredited_it_employer": vacancy[13],
                "description": vacancy[14],
                "site_url": vacancy[15],
                "logo_urls": employer_url_logo.get_dict()
            })
            area = HHArea.create(**{
                "id_": vacancy[16],
                "name": vacancy[17],
                "url": vacancy[18]
            })
            experience = HHExperience.create(**{
                "id_": vacancy[19],
                "name": vacancy[18]
            })
            employment = HHEmployment.create(**{
                "id_": vacancy[21],
                "name": vacancy[22]
            })
            schedule = HHSchedule.create(**{
                "id_": vacancy[23],
                "name": vacancy[24]
            })
            salary = HHSalary.create(**{
                "from_": vacancy[25],
                "to": vacancy[26],
                "currency": vacancy[27],
                "gross": vacancy[28]
            })
            salary_currency = HHSalaryCurrency.create(**{
                "code": vacancy[29],
                "abbr": vacancy[30],
                "name": vacancy[31],
                "default": vacancy[32],
                "rate": vacancy[33],
                "in_use": vacancy[34]
            })
            vacancies.append(HHVacancy.create(**{
                "id_": vacancy[0],
                "name": vacancy[1],
                "created_at": vacancy[2],
                "published_at": vacancy[3],
                "alternate_url": vacancy[4],
                "employer": employer,
                "area": area,
                "description": vacancy[7],
                "experience": experience,
                "employment": employment,
                "schedule": schedule,
                "salary": salary,
                "salary_currency": salary_currency
            }))

        return vacancies

    def get_all_vacancies(self) -> list:
        """
        Получает список всех вакансий с указанием:
            - название компании
            - название вакансии
            - зарплата
            - валюта
            - ссылка на вакансию
        """
        return self._query_fetchall("SELECT "
                                    "e.name, v.name, s.from, s.to, c.name, v.alternate_url "
                                    "FROM vacancy AS v "
                                    "JOIN employer e ON v.employer_id = e.id "
                                    "LEFT JOIN salary s ON v.id = s.vacancy_id "
                                    "LEFT JOIN currency c ON s.currency_code = c.code")

    def get_companies_and_vacancies_count(self):
        """
        Список компаний и количество вакансий у каждой.
        """
        return self._query_fetchall("SELECT e.name, COUNT(v.id) "
                                    "FROM employer e "
                                    "LEFT JOIN vacancy v ON e.id = v.employer_id "
                                    "GROUP BY e.name "
                                    "ORDER BY COUNT(v.id) DESC")

    def get_avg_salary(self):
        """
        ru: Получение средней зарплаты.
        """
        return self._query_fetchall("SELECT ROUND(((AVG(s.from) + AVG(s.to)) / 2), 2)"
                                    "FROM salary s")

    def get_vacancies_with_higher_salary(self):
        """
        ru: Получение вакансий с зарплатой выше средней.
        """
        return self._query_fetchall("SELECT e.\"name\", v.name, s.from, s.to, c.name, v.alternate_url "
                                    "FROM vacancy AS v "
                                    "JOIN employer e "
                                    "on v.employer_id = e.id "
                                    "LEFT JOIN salary s "
                                    "ON v.id = s.vacancy_id "
                                    "LEFT JOIN currency c "
                                    "ON s.currency_code = c.code "
                                    "WHERE round(((s.from + s.to) / 2), 2) > ("
                                    "SELECT ROUND(((AVG(s.from) + AVG(s.to)) / 2), 2)"
                                    "FROM salary s)")

    def get_vacancies_with_keyword(self, keyword: str):
        """
        ru: Получение вакансий по ключевому слову.
        """
        return self._query_fetchall("SELECT e.\"name\", v.name, s.from, s.to, c.name, v.alternate_url "
                                    "FROM vacancy AS v "
                                    "JOIN employer e "
                                    "on v.employer_id = e.id "
                                    "LEFT JOIN salary s "
                                    "ON v.id = s.vacancy_id "
                                    "LEFT JOIN currency c "
                                    "ON s.currency_code = c.code "
                                    f"WHERE v.name COLLATE \"ru_RU.UTF-8\" ILIKE '%{keyword}%'")

    def add_schedule(self, schedule: HHSchedule):
        """
        ru: Добавление графика работы.
        """
        if self.check_value("schedule", "id", schedule.id_):
            return

        self._query(
            "INSERT INTO schedule (id, name)"
            "VALUES (%s, %s)",
            (schedule.id_, schedule.name)
        )

    def add_experience(self, experience: HHExperience):
        """
        ru: Добавление опыта работы.
        """
        if self.check_value("experience", "id", experience.id_):
            return

        self._query(
            "INSERT INTO experience (id, name)"
            "VALUES (%s, %s)",
            (experience.id_, experience.name)
        )

    def add_employment(self, employment: HHEmployment):
        """
        ru: Добавление типа занятости.
        """
        if self.check_value("employment", "id", employment.id_):
            return

        self._query(
            "INSERT INTO employment (id, name)"
            "VALUES (%s, %s)",
            (employment.id_, employment.name)
        )

    def add_area(self, area: HHArea):
        """
        ru: Добавление региона.
        """
        if self.check_value("area", "id", area.id_):
            return

        self._query(
            "INSERT INTO area (id, name, url)"
            "VALUES (%s, %s, %s)",
            (area.id_, area.name, area.url)
        )

    def add_employer(self, employer: HHEmployer):
        """
        ru: Добавление работодателя.
        """
        if self.check_value("employer", "id", employer.id_):
            return
        self._query(
            "INSERT INTO employer"
            "(id, name, alternate_url, accredited_it_employer, description, site_url)"
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (employer.id_, employer.name, employer.alternate_url,
             employer.accredited_it_employer, employer.description, employer.site_url)
        )

        self.add_employer_url_logo(employer.id_, employer.logo_urls)

    def add_employer_url_logo(self, employer_id: str, employer: HHEmployerUrlLogo):
        """
        ru: Добавление логотипа работодателя.
        """
        self._query(
            "INSERT INTO employer_url_logo"
            "(employer_id, original, size_90, size_240)"
            "VALUES (%s, %s, %s, %s)",
            (employer_id, employer.original, employer.size90, employer.size240)
        )

    def add_salary_currency(self, currency: HHSalaryCurrency):
        """
        ru: Добавление валюты зарплаты.
        """
        if self.check_value("currency", "code", currency.code):
            return
        self._query(
            "INSERT INTO currency"
            "(code, abbr, name, \"default\", rate, in_use)"
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (currency.code, currency.abbr, currency.name, currency.default, currency.rate, currency.in_use)
        )

    def add_salary(self, vacancy_id: str, salary: HHSalary):
        """
        ru: Добавление зарплаты.
        """
        if self.check_value("salary", "vacancy_id", vacancy_id):
            return
        self._query(
            "INSERT INTO salary"
            "(vacancy_id, \"from\", \"to\", currency_code, gross)"
            "VALUES (%s, %s, %s, %s, %s)",
            (vacancy_id, salary.from_, salary.to, salary.currency, salary.gross)
        )

    def add_vacancy(self, vacancy: HHVacancy):
        """
        ru: Добавление вакансии.
        """
        if self.check_value("vacancy", "id", vacancy.id_):
            return
        self.add_schedule(vacancy.schedule)
        self.add_employment(vacancy.employment)
        self.add_experience(vacancy.experience)
        self.add_area(vacancy.area)
        self.add_employer(vacancy.employer)
        self._query(
            "INSERT INTO vacancy"
            "(id, name, created_at, published_at, alternate_url, employer_id, area_id, description, "
            "experience_id, employment_id, schedule_id)"
            f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (vacancy.id_, vacancy.name, vacancy.created_at, vacancy.published_at, vacancy.alternate_url,
             vacancy.employer.id_,
             vacancy.area.id_, vacancy.description, vacancy.experience.id_, vacancy.employment.id_,
             vacancy.schedule.id_)
        )
        if vacancy.salary:
            self.add_salary(vacancy.id_, vacancy.salary)

    def update_values(self, table: str, column: str, value: str, ref_column: str, new_value: str):
        """
        ru: Обновление значения.
        """
        self._query(
            f"UPDATE {table} SET {column} = %s WHERE {ref_column} = %s",
            (new_value, value)
        )

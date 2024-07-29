"""
Модуль содержит необходимые классы для объектов работы с данными:
    - Vacancy: описание вакансии
    - Employer: описание работодателя
    - Salary: описание зарплаты
    - Area: описание локации
    - Experience: описание опыта работы
    - Employment: описание типа занятости
    - Schedule: описание графика работы
"""
import datetime
from src.bases.base_objects import JobObject


class HHSchedule(JobObject):
    """
    ru: Класс для создания объекта графика работы.
    en: Class for creating a work schedule object.
    """

    def __init__(
            self,
            id_: str,
            name: str
    ):
        """
        :param id_: string, Id графика работы
        :param name: string, Название графика работы
        """
        self.id_ = id_
        self.name = name
        super().__init__(id_=id_, name=name)

    def __str__(self):
        return f"График работы: {self.name}"


class HHExperience(JobObject):
    """
    ru: Класс для создания объекта опыта работы.
    en: Class for creating a work experience object.
    """

    def __init__(
            self,
            id_: str,
            name: str
    ):
        """
        :param id_: string, Id опыта работы
        :param name: string, Название опыта работы
        """
        self.id_ = id_
        self.name = name
        super().__init__(id_=id_, name=name)

    def __str__(self):
        return f"Опыт работы: {self.name}"


class HHEmployment(JobObject):
    """
    ru: Класс для создания объекта типа занятости.
    en: Class for creating an employment type object.
    """

    def __init__(
            self,
            id_: str,
            name: str
    ):
        """
        :param id_: string, Id типа занятости
        :param name: string, Название типа занятости
        """
        self.id_ = id_
        self.name = name
        super().__init__(id_=id_, name=name)

    def __str__(self):
        return f"Тип занятости: {self.name}"


class HHArea(JobObject):
    """
    ru: Класс для создания объекта локации.
    en: Class for creating a location object.
    """

    def __init__(
            self,
            id_: str,
            name: str,
            url: str,
    ):
        """
        :param id_: string, Id локации
        :param name: string, Название локации
        """
        self.id_ = id_
        self.name = name
        self.url = url
        super().__init__(id_=id_, name=name, url=self.url)

    def __str__(self):
        return f"Регион: {self.name}"


class HHSalaryCurrency(JobObject):
    """
    ru: Класс для создания объекта валюты зарплаты.
    en: Class for creating a salary currency object.
    """

    def __init__(
            self,
            code: str,
            abbr: str,
            name: str,
            default: bool,
            rate: float,
            in_use: bool
    ):
        """
        :param code: string, код валюты
        :param abbr: string, аббревиатура валюты
        :param name: string, Название валюты
        :param default: boolean, Валюта по умолчанию
        :param rate: float, курс валюты к рублю
        :param in_use: boolean, валюта используется
        """
        self.code = code
        self.abbr = abbr
        self.name = name
        self.default = default
        self.rate = rate
        self.in_use = in_use
        super().__init__(
            code=self.code,
            abbr=self.abbr,
            name=self.name,
            default=self.default,
            rate=self.rate,
            in_use=self.in_use
        )

    def __str__(self):
        return self.name


class HHSalary(JobObject):
    """
    ru: Класс для создания объекта зарплаты.
    en: Class for creating a salary object.
    """

    def __init__(
            self,
            from_: int | None,
            to: int | None,
            currency: str,
            gross: bool = False,
    ):
        """
        :param from_: integer, Зарплата от
        :param to: integer, Зарплата до
        :param currency: string, Валюта
        :param gross: boolean, Налог
        """
        self.from_ = from_
        self.to = to
        self.gross = gross
        self.currency = str
        super().__init__(from_=from_, to=to, currency=currency, gross=gross)

    def __lt__(self, other):
        if not other:
            return False
        self_list = [self.from_, self.to]
        other_list = [other.from_, other.to]
        if all(self_list) and all(other_list):
            return sum(self_list) / 2 < sum(other_list) / 2
        elif all(self_list) and any(other_list):
            return sum(self_list) / 2 < (other.from_ or other.to)
        elif any(self_list) and all(other_list):
            return (self.from_ or self.to) < sum(other_list) / 2
        return (self.from_ or self.to) < (other.from_ or other.to)

    def __gt__(self, other):
        if not other:
            return True
        self_list = [self.from_, self.to]
        other_list = [other.from_, other.to]
        if all(self_list) and all(other_list):
            return sum(self_list) / 2 > sum(other_list) / 2
        elif all(self_list) and any(other_list):
            return sum(self_list) / 2 > (other.from_ or other.to)
        elif any(self_list) and all(other_list):
            return (self.from_ or self.to) > sum(other_list) / 2
        return (self.from_ or self.to) > (other.from_ or other.to)

    def __str__(self):
        if self.from_ and self.to:
            return f"Зарплата: от {self.from_} до {self.to} {self.currency}"
        elif self.from_:
            return f"Зарплата: от {self.from_} {self.currency}"
        elif self.to:
            return f"Зарплата: до {self.to} {self.currency}"
        else:
            return "Уровень дохода не указан"


class HHEmployerUrlLogo(JobObject):
    """
    ru: Класс для создания объекта логотипа работодателя.
    en: Class for creating an employer logo object.
    """

    def __init__(
            self,
            **kwargs
    ):
        """
        :param original: string, Оригинальный размер логотипа
        :param 90: string, Размер 90x90
        :param 240: string, Размер 240x240
        """
        self.original = kwargs.get("original")
        self.size90 = kwargs.get("90")
        self.size240 = kwargs.get("240")
        super().__init__(
            original=self.original,
            size90=self.size90,
            size240=self.size240
        )

    def get_dict(self) -> dict:
        return {
            "original": self.original,
            "90": self.size90,
            "240": self.size240
        }


class HHEmployer(JobObject):
    """
    ru: Класс для coздания объекта работодателя.
    en: Class for creating an employer object.
    """

    def __init__(
            self,
            id_: str,
            name: str,
            alternate_url: str,
            logo_urls: dict | HHEmployerUrlLogo = None,
            accredited_it_employer: bool = False,
            description: str | None = None,
            site_url: str | None = None,
            **kwargs

    ):
        """
        :param id_: string, Id работодателя
        :param name: string, Название работодателя
        :param alternate_url: string, Ссылка на работодателя
        :param logo_urls: dict, Логотип работодателя
        :param accredited_it_employer: boolean, Аккредитованный it-работодатель
        :param description: string, Описание работодателя
        :param site_url: string, Сайт работодателя
        """
        self.additional = kwargs
        self.id_ = id_
        self.name = name
        self.site_url = site_url
        self.alternate_url = alternate_url
        self.logo_urls = logo_urls if isinstance(logo_urls, HHEmployerUrlLogo) else HHEmployerUrlLogo(
            **logo_urls) if logo_urls else None
        self.accredited_it_employer = accredited_it_employer
        self.description = description
        super().__init__(
            id_=self.id_,
            name=self.name,
            alternate_url=self.alternate_url,
            logo_urls=self.logo_urls,
            accredited_it_employer=self.accredited_it_employer,
            description=self.description,
            site_url=self.site_url,
            additional=self.additional
        )

    def __str__(self):
        url = f"\nСсылка работодателя: {self.alternate_url}" if self.alternate_url else ""
        return f"Работодатель: {self.name}{url}"


class HHVacancy(JobObject):
    """
    ru: Класс для создания объекта вакансии.
    en: Class for creating a vacancy object.
    """

    def __init__(
            self,
            id_: str,
            name: str,
            created_at: str,
            published_at: str,
            alternate_url: str,
            employer: dict | HHEmployer,
            salary: dict | HHSalary,
            area: dict | None,
            experience: dict | None,
            employment: dict | None,
            schedule: dict | None,
            description: str | None = None,
            **kwargs
    ):
        """
        :param id_: string, Id вакансии
        :param name: string, Название вакансии
        :param created_at: string, Дата создания вакансии
        :param published_at: string, Дата публикации вакансии
        :param alternate_url: string, Ссылка на вакансию
        :param employer: dict, Работодатель
        :param salary: dict, Зарплата
        :param area: dict, Локация
        :param experience: dict, Опыт работы
        :param employment: dict, Тип занятости
        :param schedule: dict, График работы
        :param description: string, Описание вакансии
        :param kwargs: dict, Дополнительные параметры
        """
        self.employer = employer if isinstance(employer, HHEmployer) else HHEmployer.create(**employer)
        self.salary = salary if isinstance(salary, HHSalary) else HHSalary.create(**salary) if salary else None
        self.name = name
        self.created_at = created_at
        self.published_at = published_at
        self.id_ = id_
        self.alternate_url = alternate_url
        self.area = area if isinstance(area, HHArea) else HHArea.create(**area) if area else None
        self.experience = experience if isinstance(experience, HHExperience) \
            else HHExperience.create(**experience) if experience else None
        self.employment = employment if isinstance(employment, HHEmployment) \
            else HHEmployment.create(**employment) if employment else None
        self.schedule = schedule if isinstance(schedule, HHSchedule) \
            else HHSchedule.create(**schedule) if schedule else None
        self.description = description
        self.additional = kwargs
        super().__init__(
            id_=id_,
            description=self.description,
            name=self.name,
            area=self.area,
            salary=self.salary,
            published_at=self.published_at,
            created_at=self.created_at,
            alternate_url=self.alternate_url,
            employer=self.employer,
            schedule=self.schedule,
            experience=self.experience,
            employment=self.employment,
            additional=self.additional
        )

    def __str__(self):
        name = f"Вакансия: {self.name}" if self.name else ""
        date_to_other_view = datetime.datetime.fromisoformat(self.published_at).strftime("%d-%m-%Y")
        date = f"\nОпубликовано: {date_to_other_view}" if self.published_at else ""
        url = f"\nСсылка вакансии: {self.alternate_url}" if self.alternate_url else ""
        return f"{name}{date}{url}"

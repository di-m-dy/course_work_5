"""
ru: Модуль для описания пользовательских исключений пр работе с API.
"""


class ApiError(Exception):
    """
    ru: Базовый класс для пользовательских исключений.
    en: Base class for user errors.
    """
    pass


class ApiBaseError(ApiError):
    """
    ru: Класс ошибки для базового класса API.
    en: Error class for the base API class.
    """

    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else "Base error"

    def __str__(self):
        return self.message


class ApiQueryError(ApiBaseError):
    """
    ru: Класс ошибки для запроса к API.
    en: Error class for API request.
    """

    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else "Query error"


class AttrIntersectionError(ApiBaseError):
    """
    ru: Класс ошибки для пересечения аттрибутов.
    en: Error class for attribute intersection.
    """

    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else "Attributes intersect"


class AttrValueRestrictionError(ApiBaseError):
    """
    ru: Класс ошибки для аттрибута у которого еть ограничение значения.
    en: Error class for an attribute that has a value restriction.
    """

    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else "Restriction value"

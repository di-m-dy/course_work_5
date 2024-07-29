"""
ru: Модуль для конфигураций приложения
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ru: Подключение переменных окружения
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# ru: Список id работодателей по умолчанию (для тестов)
DEFAULT_EMPLOYERS_LIST = [
    2324020,  # ru: Точка
    1740,  # ru: Яндекс
    3529,  # ru: Сбер
    4195724,  # ru: 2GIS
    78638,  # ru: T-банк
    1057,  # ru: Лаборатория Касперского
    41862,  # ru: Контур
    4649269,  # ru: T1
    1122462,  # ru:  Skyeng
    633069,  # ru:  Selectel
]
# ru: Путь к SQL скриптам
SQL_SCRIPTS_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "create_tables.sql")

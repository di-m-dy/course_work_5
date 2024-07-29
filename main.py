"""
ru: Главный модуль проекта для запуска.
"""
from src.app.hh_ui_cli import UserInterface

if __name__ == "__main__":
    app = UserInterface()
    app.start()

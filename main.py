"""
ru: Главный модуль проекта для запуска приложения.
en: Main file of the project for running the application.
"""
from src.app.hh_app import UserInterface as UI_APP
from src.app.hh_test_cw5 import TestParser as TEST_APP

if __name__ == "__main__":
    text = """Выберите режим:
    
    [ 1 ] - <Тестовый режим>: демонстрация работы методов из задания курсовой работы #5
    
    [ 2 ] - <Рабочий режим>: приложение, начатое в курсовой #4,
                             в котором интегрированы все методы из задания курсовой работы #5
    """
    print(text)
    user_input = input("\nВыбор режима: ")
    if user_input == "1":
        TEST_APP().start()
    elif user_input == "2":
        UI_APP().start()

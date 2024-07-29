"""
ru: Модуль с базовыми интерфейсами
"""
import os
import sys
from abc import ABC, abstractmethod


class WidgetCLIBase(ABC):
    """
    ru: Абстрактный класс для работы с CLI.
        Определяет методы для отображения окна и получения колбэка.
    en: Abstract class for working with CLI.
        Defines methods for displaying a window and getting a callback.
    """

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def get_callback(self, key: str):
        pass


class WidgetCLI(WidgetCLIBase):
    """
    ru: Виджет для работы с CLI.
    en: Widget for working with CLI.
    """

    def __init__(self, header: str, description: str, items: list[dict] = None, footer: list[dict] = None):
        """
        :param header: заголовок
        :param description: описание
        :param items: элементы массива для отображения [{"text": str, "action": function, "args": dict}]
        :param footer: дополнительные функции внизу страницы [{"key": str, "text": str, "action": function, "args": dict}]
        """
        self.header = header
        self.description = description
        self.items = items.copy() if items else []
        self.footer = footer.copy() if footer else []
        self.callbacks = {}

    @staticmethod
    def clear():
        """
        ru: Очистка экрана.
        en: Clear the screen.
        """
        os.system("clear")

    @staticmethod
    def stop():
        """
        ru: Завершение программы.
        en: Program termination.
        """
        os.system("clear")
        sys.exit()

    @staticmethod
    def draw_line_header():
        """
        ru: Отрисовка линии для заголовка.
        en: Drawing a line for the header.
        """
        print("+" * 70)

    @staticmethod
    def draw_line_items():
        """
        ru: Отрисовка линии для элементов.
        en: Drawing a line for items.
        """
        print("-" * 70)

    def print_header(self):
        """
        ru: Вывод заголовка.
        en: Output header.
        """
        self.draw_line_header()
        print(self.header)
        self.draw_line_header()
        print('\n')

    def print_description(self):
        """
        ru: Вывод описания.
        en: Output description.
        """
        print(self.description)

    def print_items(self):
        """
        ru: Вывод элементов.
        en: Output items.
        """
        print('\n')
        self.draw_line_items()
        print('\n')
        for i, item in enumerate(self.items):
            print(f"[{i + 1}] {item['text']}\n")
        self.draw_line_items()
        print('\n')

    def print_footer(self):
        """
        ru: Вывод футера.
        en: Output footer.
        """
        for item in self.footer:
            print(f"[{item['key']}] {item['text']}")

    def show(self):
        """
        ru: Отображение окна.
        en: Display window.
        """
        self.clear()
        self.print_header()
        self.print_description()
        if self.items:
            self.print_items()
            self.callbacks = {str(i + 1): item for i, item in enumerate(self.items)}
        if self.footer:
            self.print_footer()
            self.callbacks.update({item["key"]: item for item in self.footer})
        if self.callbacks:
            self.get_callback(input())

    def invalid_input(self):
        """
        ru: Вывод сообщения об ошибке.
        en: Output error message.
        """
        self.clear()
        print("Неверный ввод! Попробуйте еще раз.")
        input("Нажмите любую клавишу.")

    def get_callback(self, key: str):
        """
        ru: Получение коллбэка по ключу.
        en: Getting a callback by key.
        """
        key = key.lower().strip()
        if key == "exit":
            self.clear()
            self.stop()
        elif key in self.callbacks:
            arguments = self.callbacks[key].get("args")
            if arguments:
                self.callbacks[key]["action"](**arguments)
            else:
                self.callbacks[key]["action"]()
        else:
            self.invalid_input()
            self.show()


class WidgetCLIField(WidgetCLI):
    """
    ru: Виджет для работы с CLI с полем ввода.
    en: Widget for working with CLI with an input field.
    """

    def __init__(self, header: str, description: str, callback: callable):
        """
        :param header: заголовок
        :param description: описание
        :param callback: функция коллбэк для обработки ввода
        """
        super().__init__(header, description)
        self.header = header
        self.description = description
        self.callback = callback

    def show(self):
        """
        ru: Отображение окна.
        en: Display window.
        """
        self.clear()
        self.print_header()
        self.print_description()
        self.get_callback(input())

    def get_callback(self, key: str):
        """
        ru: Получение коллбэка по ключу.
        en: Getting a callback by key.
        """
        if key == "exit":
            self.clear()
            self.stop()
        else:
            self.callback(key)

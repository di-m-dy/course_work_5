# HH API PARSER v0.1
![pic](static_readme/logo.jpeg)

## Description
Парсер вакансий с hh.ru. Позволяет получить информацию о вакансиях с платформы hh.ru в России, сохранять ее в файл и позволяет удобно работать с ней: добавлять, фильтровать, удалять.
## Features
- Получение информации о вакансиях с hh.ru
- Полуение информации о работодателях
- Возможность фильтрации и сортировки вакансий
- Сохранение информации в базу данных
- Взаимодействие с пользователем через консоль

## Architecture
### Пакет [bases](src/bases) 
Пакет содержит базовые модули для работы с API.
- модуль [base_parser](src/bases/base_parser.py) - базовый класс для работы с API
- модуль [base_parser_exceptions](src/bases/base_parser_exceptions.py) - базовые исключения для работы с API
- модуль [base_objects](src/bases/base_objects.py) - базовые объекты для работы с API
- модуль [base_generate](src/bases/base_generate.py) - базовые классы для генерации объектов из данных API
### Пакет [hh](src/hh)
Пакет содержит модули для работы с API hh.ru.
- модуль [hh_parser](src/hh/hh_parser.py) - класс для работы с API hh.ru
- модуль [hh_objects](src/hh/hh_objects.py) - объекты для работы с API hh.ru
- модуль [hh_generate](src/hh/hh_generate.py) - классы для генерации объектов из данных API hh.ru
### Пакет [database](src/database)
Пакет содержит модули для работы с базой данных.
- модуль [base_db](src/database/base_db.py) - базовый модуль для работы с базой данных
- модуль [postgres_db](src/database/postgres_db.py) - модуль для работы с базой данных PostgreSQL
### Пакет [ui](src/ui)
Пакет содержит модули для работы с пользователем.
- модуль [ui_cli](src/ui/ui_cli.py) - модуль для работы с пользователем через консоль
### Пакет [app](src/app)
Пакет содержит модули для работы всего приложения.
- модуль [config](src/app/config.py) - модуль для работы с конфигурацией
- модуль [hh_database](src/app/hh_database.py) - модуль для работы с базой данныx
- модуль [hh_app](src/app/hh_app.py) - модуль для работы основного приложения (update cw_4)
- модуль [hh_test_cw5](src/app/hh_test_cw5.py) - модуль для тестирования методов по заданию cw_5
- дериктория [sql_scripts](src/app/sql_scripts) - директория для sql скриптов (создание таблиц и заполнение данными)

### Модуль [main](main.py)
Основной модуль для запуска приложения.
Можно выбрать режим работы:
- <Тестовый режим>: демонстрация работы методов из задания курсовой работы #5
- <Рабочий режим>: приложение, начатое в курсовой #4, в котором интегрированы все методы из задания курсовой работы #5

## Run project

```bash
python main.py
```




## REQUIREMENTS
- Python 3.12
- requests
- python-dotenv
- html2text
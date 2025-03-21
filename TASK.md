[Перейти: [README.md]](README.md)

[Перейти: [Комментарии к курсовой #5]](NOTES.md)

# Курсовая работа #5
## Основные шаги проекта

Получить данные о работодателях и их вакансиях с сайта `hh.ru`. Для этого используйте публичный API `hh.ru` и библиотеку 
`requests`.

- Выбрать не менее 10 интересных вам компаний, от которых вы будете получать данные о вакансиях по API.

- Спроектировать таблицы в БД PostgreSQL для хранения полученных данных о работодателях и их вакансиях. 
Для работы с БД используйте библиотеку `psycopg2`.

- Реализовать код, который заполняет созданные в БД PostgreSQL таблицы данными о работодателях и их вакансиях.
Создать класс DBManager для работы с данными в БД.

## Класс DBManager
Создайте класс `DBManager`, который будет подключаться к БД PostgreSQL и иметь следующие методы:

 
- `get_companies_and_vacancies_count()` — получает список всех компаний и количество вакансий у каждой компании.
 
- `get_all_vacancies()` — получает список всех вакансий с указанием названия компании, 
названия вакансии и зарплаты и ссылки на вакансию.
 
- `get_avg_salary()` — получает среднюю зарплату по вакансиям.
 
- `get_vacancies_with_higher_salary()` — получает список всех вакансий, 
у которых зарплата выше средней по всем вакансиям.
 
- `get_vacancies_with_keyword()` — получает список всех вакансий, 
- в названии которых содержатся переданные в метод слова, например python.

Класс DBManager должен использовать библиотеку `psycopg2` для работы с БД.


## Детали оформления решения
- Проект выложен на GitHub.
- Оформлен файл README.md с информацией, о чем проект, как его запустить и как с ним работать.
- Есть `Python-модуль` для создания и заполнения данными таблиц БД.
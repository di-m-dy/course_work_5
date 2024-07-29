-- area: таблица для локации

-- Drop table

-- DROP TABLE area;

CREATE TABLE IF NOT EXISTS area (
	id VARCHAR(50) NOT NULL, -- id локации - первичный ключ
	"name" VARCHAR(250) NOT NULL, -- название локации
	url VARCHAR(250) NOT NULL, -- ссылка на локацию
	CONSTRAINT area_pk PRIMARY KEY (id)
);

-- currency: таблица для валюты зарплаты

-- Drop table

-- DROP TABLE currency;

CREATE TABLE IF NOT EXISTS currency (
	code VARCHAR(50) NOT NULL, -- код валюты
	abbr VARCHAR(30) NOT NULL, -- аббривиатуры
	"name" VARCHAR(250) NOT NULL, -- название валюты
	"default" BOOL NOT NULL, -- по умолчанию
	rate NUMERIC NOT NULL, -- курс к рублю
	in_use bool NOT NULL,
	CONSTRAINT currency_pk PRIMARY KEY (code)
);

-- employer: таблица для работодателей

-- Drop table

-- DROP TABLE employer;

CREATE TABLE IF NOT EXISTS employer (
	id VARCHAR(50) NOT NULL, -- id работодателя из api.hh.ru - первичный ключ
	"name" VARCHAR(250) NOT NULL, -- название работодателя
	alternate_url VARCHAR(250) NOT NULL, -- ссылка на работодателя
	accredited_it_employer BOOL NOT NULL, -- наличие it аккредитации
	description TEXT, -- описание работодателя
	site_url VARCHAR(250), -- сайт работодателя
	CONSTRAINT employer_pk PRIMARY KEY (id)
);

-- employment: таблица для типа занятости

-- Drop table

-- DROP TABLE employment;

CREATE TABLE IF NOT EXISTS employment (
	id VARCHAR(50) NOT NULL, -- id типа занаятости - первичный ключ
	"name" VARCHAR(250) NOT NULL, -- название типа занятости
	CONSTRAINT employment_pk PRIMARY KEY (id)
);

-- experience: таблица для опыта работы

-- Drop table

-- DROP TABLE experience;

CREATE TABLE IF NOT EXISTS experience (
	id VARCHAR(50) NOT NULL, -- id опыта работы
	"name" VARCHAR(250) NOT NULL, -- название опыта работы
	CONSTRAINT experience_pk PRIMARY KEY (id)
);

-- schedule: таблица для графика работы

-- Drop table

-- DROP TABLE schedule;

CREATE TABLE IF NOT EXISTS schedule (
	id VARCHAR(50) NOT NULL, -- id графика работы - первичный ключ
	"name" VARCHAR(250) NOT NULL, -- название графика работы
	CONSTRAINT schedule_pk PRIMARY KEY (id)
);

-- employer_url_logo: таблица для ссылок на изображения лого

-- Drop table

-- DROP TABLE employer_url_logo;

CREATE TABLE IF NOT EXISTS employer_url_logo (
	employer_id VARCHAR(50) NOT NULL, -- id работодателя - превичный ключ и внешний ключ на таблицу employer
	original VARCHAR(250), -- оригинальное изображение
	size_90 VARCHAR(250), -- размер 90
	size_240 VARCHAR(250), -- размер 240
	CONSTRAINT employer_url_logo_pk PRIMARY KEY (employer_id),
	CONSTRAINT employer_url_logo_employer_fk FOREIGN KEY (employer_id) REFERENCES employer(id) ON DELETE CASCADE
);

-- vacancy: таблица для вакансий

-- Drop table

-- DROP TABLE vacancy;

CREATE TABLE IF NOT EXISTS vacancy (
	id VARCHAR(50) NOT NULL, -- id вакансии с api.hh.ru
	"name" VARCHAR(250) NOT NULL, -- название вакансии
	created_at DATE NOT NULL, -- дата создания
	published_at DATE NOT NULL, -- дата публикации
	alternate_url VARCHAR(250) NOT NULL, -- ссылка на вакансию
	employer_id VARCHAR(50) NOT NULL, -- id работодателя - внешний ключ на таблицу employer
	area_id VARCHAR(50), -- локация внешний ключ на таблицу area
	experience_id VARCHAR(50), -- опыт работы внешний ключ на таблицу experince
	employment_id VARCHAR(50), -- тип занятости внешний ключ на таблицу employment
	schedule_id VARCHAR(50), -- график работы внешний ключ на таблицу schedule
	description TEXT, -- описание вакансии
	CONSTRAINT vacancy_pk PRIMARY KEY (id),
	CONSTRAINT vacancy_area_fk FOREIGN KEY (area_id) REFERENCES area(id) ON DELETE SET NULL,
	CONSTRAINT vacancy_employer_fk FOREIGN KEY (employer_id) REFERENCES employer(id),
	CONSTRAINT vacancy_employment_fk FOREIGN KEY (employment_id) REFERENCES employment(id) ON DELETE SET NULL,
	CONSTRAINT vacancy_experience_fk FOREIGN KEY (experience_id) REFERENCES experience(id) ON DELETE SET NULL,
	CONSTRAINT vacancy_schedule_fk FOREIGN KEY (schedule_id) REFERENCES schedule(id) ON DELETE SET NULL
);

-- salary: таблица зарплат для вакансий

-- Drop table

-- DROP TABLE salary;

CREATE TABLE IF NOT EXISTS salary (
	vacancy_id VARCHAR(50) NOT NULL, -- id вакансии первичный ключ и внешний ключ на таблицы vacancy
	"from" INTEGER NULL, -- зарплата от
	"to" INTEGER NULL, -- зарплата до
	currency_code VARCHAR(50) NOT NULL, -- валюта зарплаты внешний ключ на таблицу currency
	gross BOOL, -- налог
	CONSTRAINT salary_pk PRIMARY KEY (vacancy_id),
	CONSTRAINT salary_currency_fk FOREIGN KEY (currency_code) REFERENCES currency(code) ON DELETE SET NULL,
	CONSTRAINT salary_vacancy_fk FOREIGN KEY (vacancy_id) REFERENCES vacancy(id) ON DELETE CASCADE
);
# from itemadapter import ItemAdapter
# Импорт необходимых модулей
from pymongo import MongoClient
import pymongo

# Импортируем библиотеку hashlib для генерации уникальных идентификаторов
import hashlib

# Импортируем класс DuplicateKeyError из модуля pymongo.errors для обработки дубликатов ключей
from pymongo.errors import DuplicateKeyError

# Импорт модуля для работы с папками
import os

# Импорт библиотеки для работы с JSON-форматом
import json


# Создание папки json_folder для хранения файлов json
if not os.path.exists('./json_folder'):
    os.mkdir('./json_folder')

# Определяем контейнер для json файла
JSON_FILE_PATH = './json_folder/vacancies.json'


class JobparserPipeline:

    def __init__(self):
        # Устанавливаем соединение с MongoDB
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancyParser

    def process_item(self, item, spider):
        # Обработка информации о городе
        if 'hh.ru' not in item['url']:
            # Если не hh.ru, обрабатываем город
            item['city'] = item['city'].replace(',', '').split()[0]
        elif 'hh.ru' in item['url'] and item['city'] is not None:
            # Если hh.ru и город указан, оставляем как есть
            item['city'] = item['city']
        elif item['city'] is None:
            # Если город не указан ни в одном поле, указываем 'no data'
            item['city'] = 'no data'
        else:
            item['city'] = 'no data'

        if 'hh.ru' in item['url']:
            # Если источник hh.ru, обрабатываем данные о работодателе и зарплате
            item['employer'] = ' '.join([el.replace('\xa0', '') for el in item['employer']]) if \
                len(item['employer']) > 1 else item['employer'][0]
            salary_data = [int(el.replace('\xa0', '')) for el in item['salary'] if '\xa0' in el]

            if not salary_data:
                # Если данные о зарплате отсутствуют
                item['min_salary'] = 'no data'
                item['max_salary'] = 'no data'
                item['currency'] = 'no data'
            elif len(salary_data) == 2 and ' до ' in item['salary']:
                # Если указан диапазон зарплаты (до)
                item['max_salary'] = salary_data[1]
                item['min_salary'] = salary_data[0]
                item['currency'] = item['salary'][-3]
            elif len(salary_data) == 1 and 'до ' in item['salary']:
                # Если указана только максимальная зарплата (до)
                item['max_salary'] = salary_data[0]
                item['currency'] = item['salary'][-3]
            elif len(salary_data) == 1 and 'от ' in item['salary']:
                # Если указана только минимальная зарплата (от)
                item['min_salary'] = salary_data[0]
                item['currency'] = item['salary'][-3]
            item['experience'] = item['experience_unedited'][2]
        elif 'hh.ru' not in item['url']:
            # Если источник не hh.ru (предположительно superjob.ru), обрабатываем данные о работодателе и зарплате
            item['employer'] = item['employer']
            item['experience'] = item['experience_unedited'][-2]
            salary_data = list(map(int, filter(None, [el.replace('₽', '').replace('\xa0', '')
                                                      for el in item['salary'] if '\xa0' in el])))
            currency_sj = [el.replace('\xa0', '') for el in item['salary'] if '\xa0' in el]
            if not salary_data:
                # Если данные о зарплате отсутствуют
                item['min_salary'] = 'no data'
                item['max_salary'] = 'no data'
                item['currency'] = 'no data'
            elif len(salary_data) == 2:
                # Если указан диапазон зарплаты
                item['max_salary'] = salary_data[1]
                item['min_salary'] = salary_data[0]
                item['currency'] = item['salary'][-3]
            elif len(salary_data) == 1 and 'до' in item['salary']:
                # Если указана только максимальная зарплата (до)
                item['max_salary'] = salary_data[0]
                item['currency'] = list(filter(None, currency_sj))[0][-1]
            elif len(salary_data) == 1 and 'от' in item['salary']:
                # Если указана только минимальная зарплата (от)
                item['min_salary'] = salary_data[0]
                item['currency'] = list(filter(None, currency_sj))[0][-1]

        # Удаление ненужных полей
        del item['experience_unedited']
        del item['salary']
        del item['city_2']

        # Создание уникального индекса на основе хеширования
        item['unique_index'] = \
            hashlib.sha256(f"{item['name']}_{item['url']}".encode()).hexdigest()

        collection = self.mongo_base[spider.name]

        # Конвертация JobparserItem в словарь
        item_dict = dict(item)

        # Сохранение данных в JSON-файл
        with open(JSON_FILE_PATH, 'a') as file:
            json.dump(item_dict, file)

        try:
            # Вставка данных в коллекцию и создание уникального индекса
            collection.insert_one(item)
            collection.create_index([('unique_index', pymongo.ASCENDING)], name='unique_id_index', unique=True)

        except pymongo.errors.DuplicateKeyError:
            print(f"Запись с таким id: {item.get('_id')} уже существует")
            # Обработка ошибок дубликатов ключей
            pass
        except Exception as e:
            # Обработка других исключений
            print(f"Произошла ошибка: {e}")

        return item

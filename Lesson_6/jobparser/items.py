# Импорт модуля scrapy, необходимого для работы с веб-скрапингом
import scrapy


# Определение класса для элемента, который будет извлекаться из веб-страницы
class JobparserItem(scrapy.Item):
    # Определение полей для элемента, которые будут извлекаться и сохраняться
    name = scrapy.Field()  # Название вакансии
    employer = scrapy.Field()  # Название работодателя
    experience_unedited = scrapy.Field()  # Опыт (в необработанном виде)
    experience = scrapy.Field()  # Опыт (обработанный)
    city = scrapy.Field()  # Город (вариант 1)
    city_2 = scrapy.Field()  # Город (вариант 2)
    metro = scrapy.Field()  # Ближайшее метро
    max_salary = scrapy.Field()  # Максимальная зарплата
    min_salary = scrapy.Field()  # Минимальная зарплата
    url = scrapy.Field()  # URL вакансии
    salary = scrapy.Field()  # Зарплата
    currency = scrapy.Field()  # Валюта
    unique_index = scrapy.Field()  # Уникальный индекс (может быть использован для идентификации)
    _id = scrapy.Field()  # Идентификатор элемента (может быть использован для MongoDB и т. д.)

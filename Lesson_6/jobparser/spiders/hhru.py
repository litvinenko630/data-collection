# Импорт необходимых модулей из библиотеки Scrapy
import scrapy
from scrapy.http import HtmlResponse  # Модуль для работы с HTML-ответами
from jobparser.items import JobparserItem  # Импорт класса JobparserItem из модуля items


# Определение паука для парсинга hh.ru
class HhruSpider(scrapy.Spider):
    name = "hhru"  # Имя паука
    allowed_domains = ["hh.ru"]  # Разрешенные домены для парсинга
    start_urls = ["https://hh.ru/search/vacancy?text=python&area=1", "https://hh.ru/search/vacancy?text=python&area=2"]
    # Начальные URL для парсинга (вакансии с ключевым словом "python" в разных регионах)

    # Метод для обработки стартовых URL и извлечения ссылок на вакансии
    def parse(self, response: HtmlResponse, **kwargs):
        next_page = response.xpath("//a[contains(@data-qa, 'pager-next')]/@href").get()
        # Извлечение ссылки на следующую страницу
        if next_page:
            yield response.follow(next_page, callback=self.parse)  # Переход на следующую страницу

        links = response.xpath("//a[contains(@class, 'serp-item__title')]/@href").getall()
        # Извлечение всех ссылок на вакансии на текущей странице
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)  # Переход на страницу вакансии

    # Метод для обработки страницы вакансии
    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()  # Извлечение названия вакансии
        # Извлечение имени работодателя
        employer = response.xpath("//a[@data-qa = 'vacancy-company-name']//text()").getall()
        # Извлечение необработанного описания опыта
        experience_unedited = response.xpath("//p[@class = 'vacancy-description-list-item']//text()").getall()
        # Извлечение обработанного описания опыта
        experience = response.xpath("//p[@class = 'vacancy-description-list-item']//text()").getall()
        # Извлечение необработанного варианта адреса (города)
        city_2 = response.xpath("//span[contains(@data-qa, 'vacancy-view-raw-address')]/text()").get()
        # Извлечение первого варианта адреса (города)
        city = response.xpath("//p[contains(@data-qa, 'vacancy-view-location')]/text()").get()
        # Извлечение названия ближайшей станции метро
        metro = response.xpath("//span[@class = 'metro-station']//text()").get()
        url = response.url  # URL текущей страницы
        # Извлечение информации о зарплате
        salary = response.xpath("//div[contains(@data-qa, 'vacancy-salary')]//text()").getall()
        # Извлечение информации о валюте зарплаты
        currency = response.xpath("//div[contains(@data-qa, 'vacancy-salary')]//text()").getall()

        # Создание и отправка объекта JobparserItem с извлеченными данными
        yield JobparserItem(name=name, employer=employer, experience_unedited=experience_unedited,
                            experience=experience, city=city, metro=metro,
                            url=url, salary=salary, city_2=city_2, currency=currency)

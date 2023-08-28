# Импорт необходимых модулей из библиотеки Scrapy
import scrapy
from scrapy.http import HtmlResponse  # Модуль для работы с HTML-ответами
from jobparser.items import JobparserItem  # Импорт класса JobparserItem из модуля items


# Определение паука для парсинга superjob.ru
class SuperjbSpider(scrapy.Spider):
    name = "superjb"  # Имя паука
    allowed_domains = ["superjob.ru"]  # Разрешенные домены для парсинга
    start_urls = ["https://www.superjob.ru/vacancy/search/?keywords=Python",
                  "https://spb.superjob.ru/vacancy/search/?keywords=Python"]
    # Начальные URL для парсинга (вакансии с ключевым словом "Python" в разных регионах)

    # Метод для обработки стартовых URL и извлечения ссылок на вакансии
    def parse(self, response: HtmlResponse, **kwargs):
        next_page = response.xpath("//a[contains(@class, 'f-test-link-Dalshe')]/@href").get()
        # Извлечение ссылки на следующую страницу
        if next_page:
            yield response.follow(next_page, callback=self.parse)  # Переход на следующую страницу

        links = response.xpath("//a[contains(@class, '_2_Rn8')]/@href").getall()
        # Извлечение всех ссылок на вакансии на текущей странице
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)  # Переход на страницу вакансии

    # Метод для обработки страницы вакансии
    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()  # Извлечение названия вакансии
        # Извлечение имени работодателя
        employer = response.xpath("//div[contains(@class, '_2kYdL J9071 _1DzI0')]//text()").get()
        # Извлечение необработанного опыта
        experience_unedited = response.xpath("//span[contains(@class, '_2OTmA _1tEEc _10ByY')]/text()").getall()
        # Извлечение обработанного опыта
        experience = response.xpath("//span[contains(@class, '_2OTmA _1tEEc _10ByY')]/text()").getall()
        # Извлечение необработанного варианта адреса (города)
        city_2 = response.xpath("//div[contains(@class, 'f-test-address')]//text()").get()
        # Извлечение первого варианта адреса (города)
        city = response.xpath("//div[contains(@class, 'f-test-address')]//text()").get()
        # Извлечение названия ближайшей станции метро
        metro = response.xpath("//span[contains(@class, '_1WBzR')]//text()").get()
        url = response.url  # URL текущей страницы
        # Извлечение информации о зарплате
        salary = response.xpath("//span[contains(@class, '_4Gt5t')]//text()").getall()
        # Извлечение информации о валюте зарплаты
        currency = response.xpath("//span[contains(@class, '_4Gt5t')]//text()").getall()

        # Создание и отправка объекта JobparserItem с извлеченными данными
        yield JobparserItem(name=name, employer=employer, experience=experience,
                            experience_unedited=experience_unedited, city=city, metro=metro,
                            url=url, salary=salary, city_2=city_2, currency=currency)

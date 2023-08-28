# Импорт необходимых модулей из библиотеки Scrapy
from scrapy.crawler import CrawlerProcess  # Модуль для запуска краулеров
from scrapy.utils.reactor import install_reactor  # Модуль для установки реактора (асинхронного движка)
from scrapy.utils.log import configure_logging  # Модуль для настройки логирования
from scrapy.utils.project import get_project_settings  # Модуль для получения настроек проекта

# Импорт созданных пауков (spiders)
from jobparser.spiders.hhru import HhruSpider  # Паук для парсинга HeadHunter
from jobparser.spiders.superjb import SuperjbSpider  # Паук для парсинга SuperJob

# Основной блок кода, который будет выполнен, если скрипт запущен как основной файл
if __name__ == '__main__':
    # Установка асинхронного реактора для Twisted (необходимо для асинхронной работы)
    install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')

    # Настройка логирования для Scrapy
    configure_logging()

    # Создание экземпляра CrawlerProcess с настройками проекта
    process = CrawlerProcess(get_project_settings())

    # Запуск паука HhruSpider (парсинг HeadHunter)
    process.crawl(HhruSpider)

    # Запуск паука SuperjbSpider (парсинг SuperJob)
    process.crawl(SuperjbSpider)

    # Запуск процесса скрапинга
    process.start()

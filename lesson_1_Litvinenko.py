import os
import requests
import json
from PIL import Image
from IPython.display import display
import warnings

warnings.filterwarnings('ignore')

# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного
# пользователя, сохранить JSON-вывод в файле *.json.


def get_repositories(username):

    # Выполняем GET-запрос к API GitHub, используя эндпоинт /users/<username>/repos
    response = requests.get(f"https://api.github.com/users/{username}/repos")

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Парсим JSON-ответ
        data = response.json()
        # Проверяем наличие папки json
        if not os.path.isdir("json"):
            os.mkdir("json")

        # Открываем файл для записи
        with open("./json/repositories.json", "w") as file:
            # Записываем JSON-данные в файл
            json.dump(data, file, indent=4)

        # Получаем список имен репозиториев
        repository_names = [repo['name'] for repo in data][:8]
        return repository_names

    else:
        print(f"Ошибка при выполнении запроса: {response.status_code}")


def print_repository_names(repository_names):
    # Выводим список имен репозиториев
    for number, name in enumerate(repository_names, 1):
        print(f'{number}. {name}')


username = "twitterdev"
repository_names = get_repositories(username)
print_repository_names(repository_names)


# 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое,
# требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

# Указываем токен доступа
api_key = 'live_FNOBhwfIoVUYU11iL0MRQqIELoUwfGNsNZVzpegXLqJWBVy2YJJpa4q3ZXrikenM'

# Устанавливаем URL и заголовок авторизации
url = f'https://api.thecatapi.com/v1/images/search?limit=10&breed_ids=beng&api_key={api_key}'

# Выполняем GET-запрос
response = requests.get(url)

# Проверяем успешность запроса
if response.status_code == 200:
    # Получаем данные о пользователе в формате JSON
    data = response.json()
else:
    print(f"Ошибка при выполнении запроса: {response.status_code}")

images = [image for image in data]


def load_and_resize_image(url, width, height):
    # Получаем изображение по URL-адресу, изменяем его размеры и сохраняем
    response = requests.get(url, stream=True)
    response.raw.decode_content = True
    img = Image.open(response.raw)
    img = img.resize((width, height), Image.Resampling.LANCZOS)

    # Проверяем режим изображения и преобразуем в режим RGB, если RGBA
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    # Сохраняем изображение и отображаем его в блокноте
    img.save(filename)
    display(img)


for image in images:
    filename = f"./json/{image['id']}.jpg"
    # Изменяем размеры изображения и сохраняем его в файловой системе
    load_and_resize_image(image['url'], image['width'] // 2, image['height'] // 2)

    with open("./json/bengal_cats.json", "w") as file:
        # Записываем JSON-данные в файл
        json.dump(data, file, indent=4)

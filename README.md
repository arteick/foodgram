![status workflow](https://github.com/arteick/foodgram/actions/workflows/main.yml/badge.svg)
# Foodgram
https://ilovefood.zapto.org

## Описание проекта

Foodgram - продуктовый помощник/социальная сеть, где пользователи могут публиковать рецепты своих любимых блюд, подписываться на публикации других авторов, добавлять рецепты в избранное или в корзину для покупок, чтобы потом скачать удобный список со всеми необходимыми продуктами.

#### Установка
_Далее идут команды, которые можно выполнпить в терминале  ОС Linux_

#### Склонируйте репозиторий на свой компьютер:
```git clone <ссылка>```

Создайте файл .env и заполните его своими данными. Все необходимые переменные перечислены в файле .env.example, находящемся в корневой директории проекта.

#### Создание Docker-образов
* Замените username на свой логин на DockerHub:

```
cd frontend
docker build -t username/foogdram_frontend .
cd ../backend
docker build -t username/foogdram_backend .
cd ../nginx
docker build -t username/foogdram_gateway .
```

* Загрузите образы на DockerHub:

```
docker push username/foogdram_frontend
docker push username/foogdram_backend
docker push username/foogdram_gateway
```

#### Деплой на сервере
* Подключитесь к удаленному серверу
* Создайте на сервере директорию foogdram:

    ```mkdir foogdram```

* Установите Docker Compose на сервер:
```
sudo apt update
sudo apt install curl
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt install docker-compose
```
* Скопируйте файлы docker-compose.prod.yml и .env в директорию foogdram/ на сервере. Для заполнения своего файла .env используйте файл с примером заполнения - .env.example


* Запустите Docker Compose в режиме демона:

```
sudo docker-compose up -d
```
* Выполните миграции, загрузите фикстуры, соберите статические файлы бэкенда и скопируйте их в /backend_static/static/:

```
sudo docker compose -f docker-compose.prod.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.prod.yml exec backend python manage.py loaddata db.json
sudo docker compose -f docker-compose.prod.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.prod.yml exec backend cp -r /app/collected_static/. /backend_static/static/
```


* Установите веб-сервер. В примере будет использоваться веб-сервер nginx.
```
sudo apt install nginx -y
sudo systemctl start nginx
```
* Измените файл конфигурации Nginx в редакторе:
```sudo nano /etc/nginx/sites-enabled/default```

```
location / {
    proxy_set_header Host $http_host;
    proxy_pass http://127.0.0.1:8000;
}
```
* Проверьте правильность конфигурации Nginx:

    ```sudo nginx -t```

* Перезапустите Nginx:

    ```sudo service nginx reload```

#### Настройка CI/CD
В проекте для поддержания прицнипа CI/CD используется технология GitHub Actions.
В репозитории уже настроен процесс автоматиации.

Файл workflow уже написан и находится в директории:
```foogdram/.github/workflows/main.yml```

Для работы workflow добавьте секреты в GitHub Actions:
```DOCKER_USERNAME``` - имя пользователя в DockerHub
```DOCKER_PASSWORD``` - пароль пользователя в DockerHub
```HOST``` - IP-адрес сервера
```USER``` - имя пользователя
```SSH_KEY``` - содержимое приватного SSH-ключа (cat ~/.ssh/id_rsa)
```SSH_PASSPHRASE``` - пароль для SSH-ключа
```TELEGRAM_TO``` - id пользователя, которому бот отправит сообщения о деплое
```TELEGRAM_TOKEN``` - токен телеграм бота


#### Foodgram REST API
Платформа Foodgram имеет REST API, список доступных эндпоинтов доступен по адресу ilovefood.zapto.org/api/, также вы можете ознакомиться с документацией по API по [ссылке](https://ilovefood.zapto.org/api/docs/).

__Вот несколько примеров запросов к API:__

Эндпоинт: [https://ilovefood.zapto.org/api/recipes]()
Метод: GET
Ответ API:

```
{
    "count": 123,
    "next": "http://foodgram.example.org/api/recipes/?page=4",
    "previous": "http://foodgram.example.org/api/recipes/?page=2",
  - "results": [
      - {
            "id": 0,
          - "tags": [
                {
                    "id": 0,
                    "name": "Завтрак",
                    "slug": "breakfast"
                }
            ],
          - "author": {
                "email": "user@example.com",
                "id": 0,
                "username": "string",
                "first_name": "Вася",
                "last_name": "Иванов",
                "is_subscribed": false,
                "avatar": "http://foodgram.example.org/media/users/image.png"
            },
          - "ingredients": [
                {
                "id": 0,
                "name": "Картофель отварной",
                "measurement_unit": "г",
                "amount": 1
                }
            ],
            "is_favorited": true,
            "is_in_shopping_cart": true,
            "name": "string",
            "image": "http://foodgram.example.org/media/recipes/images/image.png",
            "text": "string",
            "cooking_time": 1
        }
    ]
}
```

Эндпоинт: [https://ilovefood.zapto.org/api/recipes/download_shopping_cart/]()
Метод: GET
Ответ API: ```Файл с расширением .txt со списком ингридиентов для рецептов```

Эндпоинт: [https://ilovefood.zapto.org/api/ingredients/]()
Метод: GET
Ответ API: 
```
[
  {
    "id": 0,
    "name": "Капуста",
    "measurement_unit": "кг"
  },
  {
    "id": 1,
    "name": "Морковь",
    "measurement_unit": "кг"
  },
  {
    "id": 2,
    "name": "Сахар",
    "measurement_unit": "г"
  }
]
```
#### Технологии
```Python``` ```Django``` ```Django Rest Framework``` ```PostgreSQL``` ```Nginx``` ```Gunicorn``` ```Docker``` ```GitHub Actions``` ```Continuous Integration``` ```Continuous Deployment```

---
_Автор_ - [arteick](https://github.com/arteick)

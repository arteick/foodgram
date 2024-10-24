# Foodgram

## Описание проекта

Foodgram - продуктовый помощник/социальная сеть, где пользователи могут публиковать рецепты своих любимых блюд, подписываться на публикации других авторов, добавлять рецепты в избранное или в корзину для покупок, чтобы потом скачать удобный список со всеми необходимыми продуктами.

#### Установка
_Далее идут команды, которые можно выполнпить в терминале  ОС Linux_

#### Склонируйте репозиторий на свой компьютер:
```git clone ...```

Создайте файл .env и заполните его своими данными. Все необходимые переменные перечислены в файле .env.example, находящемся в корневой директории проекта.

#### Создание Docker-образов
* Замените username на свой логин на DockerHub:

```
cd frontend
docker build -t username/foogdram_frontend .
cd ../backend
docker build -t username/foogdram_backend .
cd ../infra
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
* Скопируйте файлы docker-compose.production.yml и .env в директорию foogdram/ на сервере. Для заполнения своего файла .env используйте файл с примером заполнения - .env.example


* Запустите Docker Compose в режиме демона:

```
sudo docker-compose -f /home/YOUR_USERNAME/foogdram/docker-compose.production.yml up -d
```
* Выполните миграции, соберите статические файлы бэкенда и скопируйте их в /backend_static/static/:

```
sudo docker-compose -f /home/YOUR_USERNAME/foogdram/docker-compose.production.yml exec backend python manage.py migrate
sudo docker-compose -f /home/YOUR_USERNAME/foogdram/docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker-compose -f /home/YOUR_USERNAME/foogdram/docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
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

Для работы workflow доавьте секреты в GitHub Actions:
```DOCKER_USERNAME``` - имя пользователя в DockerHub
```DOCKER_PASSWORD``` - пароль пользователя в DockerHub
```HOST``` - IP-адрес сервера
```USER``` - имя пользователя
```SSH_KEY``` - содержимое приватного SSH-ключа (cat ~/.ssh/id_rsa)
```SSH_PASSPHRASE``` - пароль для SSH-ключа


#### Технологии
Python 3.9, Django, DRF, PostgreSQL, Docker, GitHub Actions

---
_Автор_ - [arteick](https://github.com/arteick)

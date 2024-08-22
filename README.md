# Данный проект реализцуется для изуения авторизации и аунтификации


>Требование
 
    • Git
    • Python 3.12 или выше

>Клонируем репозиторий куда удобно

    git clone https://github.com/Surutandess/users.git
>Установка нужных зависемостей для проекта

    pip install poetry
    poetry install
> Для получения приватного ключа
    openssl genrsa -out jwt-private.pem 2048

> Для получения публичнего ключа
    openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
>Запуск проекта

    python3 main.py

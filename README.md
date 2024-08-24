# Данный проект реализцуется для изуения авторизации и аунтификации


>Требование
 
    • Git
    • Docker
    • Docker compose
    
>Клонируем репозиторий куда удобно

    git clone https://github.com/Surutandess/users.git

> Для получения приватного ключа обязательно в деректории certificates
    
    openssl genrsa -out jwt-private.pem 2048

> Для получения публичнего ключа обязательно в деректории certificates
    
    openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem

>Запуск проекта
    docker compose up

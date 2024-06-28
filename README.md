# Blogicum

## Блогикум — это дом для творческих людей. Это — сообщество людей, для которых нет грани между ведением блога и дружбой в социальных сетях.

### Технологии
Python 3.9
Django 3.2.16

### Запуск проекта в dev-режиме
1. Создайте виртуальное окружение
- Linux/macOS

    ```
    python3 -m venv venv
    ```
- Windows

    ```
    python -m venv venv
    ```
2. Активируйте виртуальное окружение
- Linux/macOS

    ```
    source venv/bin/activate
    ```
- Windows

    ```
    source venv/Scripts/activate
    ```
3. Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
4. В папке с файлом manage.py выполните миграции:
```
python manage.py migrate
```
5. В директории с файлом manage.py выполните команду:
```
python manage.py runserver
```
Проект доступен по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Автор
***VanZep***
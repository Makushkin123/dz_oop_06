### Задание
*Задание*: реализовать декларативный язык описания и систему валидации запросов к HTTP API сервиса скоринга.
Шаблон уже есть в api.py, тесты в test.py, функционал подсчета скора в scoring.py. 
API необычно тем, что пользователи дергают методы POST запросами. 
Чтобы получить результат пользователь отправляет в POST запросе валидный JSON определенного формата на локейшн /method. 


### Cтэк: 
Python,FastAPI, Pydantic

### Установка

1. Клонируйте репозиторий.
2. Создайте виртуальное окружение с помощью Poetry: poetry shell
3. Установите зависимости: poetry install

### Запуск

1. Перейдите в директорию проекта.
2. Запустите скрипт python main.py
3. Запуск тестов pytest -v

Telegram-бот, который строит маршрут между двумя адресами, используя Google Geocoding API и Google Directions API.
Пользователь вводит адрес отправления и назначения — бот возвращает расстояние и примерное время в пути.

 Возможности

Запрашивает у пользователя два адреса

Определяет координаты через Google Geocoding API

Строит автомобильный маршрут через Directions API

Возвращает:

расстояние (в км)

время в пути (в минутах)

?? Технологии

Python 3.x

python-telegram-bot (v20+)

Google Maps Geocoding API

Google Directions API

requests

Асинхронные обработчики Telegram

?? Установка
1. Клонируй проект
git clone https://github.com/your/repo.git
cd repo

2. Установи зависимости
pip install -r requirements.txt

3. Укажи API-ключи

Вставь свой токен Telegram и ключ Google API в код или в .env (рекомендуется).

Пример .env:

TELEGRAM_TOKEN=your_telegram_token
GOOGLE_API_KEY=your_maps_api_key

?? Запуск
python bot.py

?? Как работает бот
1. Команда /start

Запускает диалог и просит ввести адрес отправления.

2. Функция geocode(address)

Использует Google Geocoding API, чтобы преобразовать текстовый адрес в координаты:

url = "https://maps.googleapis.com/maps/api/geocode/json"
params = {"address": address, "key": GOOGLE_MAPS_API_KEY}


Возвращает [lat, lng].

3. Функция get_route(coord_from, coord_to)

Отправляет запрос в Directions API:

url = "https://maps.googleapis.com/maps/api/directions/json"
params = {
    "origin": f"{coord_from[0]},{coord_from[1]}",
    "destination": f"{coord_to[0]},{coord_to[1]}",
    "mode": "driving",
    "language": "ru",
    "key": GOOGLE_MAPS_API_KEY,
}


Возвращает:

расстояние в км

время в пути в минутах

4. Бот отправляет результат:
?? Маршрут от 'A' до 'B':
?? Расстояние: 12.45 км
? Время в пути: 18.3 мин

?? Структура проекта
.
??? bot.py
??? README.md
??? requirements.txt

?? 
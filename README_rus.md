## Описание приложения

Это веб-приложение предназначено для получения актуальных погодных данных.
Основные функции:
Запрашивает данные через API OpenWeatherMap (https://api.openweathermap.org/data/2.5/weather).
Размещено на сайте https://propogoda.ru.
Разработано на Python с использованием фреймворка Flask.
Автоматическое обновление информации каждый час.


## Инструкция по установке и запуску:

# Обновление пакетов
apt update && apt upgrade -y
# Установка Python и зависимостей
apt install python3 python3-pip python3-venv -y
# Установите Nginx и инструменты
apt install nginx -y
# Склонируйте репозиторий или загрузите файлы
git clone https://github.com/Marat1234qwer/web_app_weather /var/www
cd /var/www/web_app_weather
# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate
# Установите зависимости
pip install -r requirements.txt
# Запуск
python3 server.ru

После запуска приложение будет доступно по IP-адресу сервера (например, http://ваш_IP:5000).


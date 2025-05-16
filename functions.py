from datetime import datetime
import requests
import time
import cities


API_KEY = '' # получаем на https://openweathermap.org/
UPDATE_INTERVAL = 3600  # 1 час в секундах
REQUEST_DELAY = 1       # Задержка между запросами групп
weather_cache = {
    'last_update': 0,
    'major': [],
    'central': [],
    'north_west': [],
    'southern': [],
    'north_caucasian': [],
    'privolzhsky': [],
    'ural': [],
    'siberian': [],
    'far_eastern': [],
}

CITY_GROUPS = cities.CITY_GROUPS
RUSSIAN_NAMES = cities.RUSSIAN_NAMES


def fetch_weather_group(city_ids):
    """Запрос погоды для группы городов"""
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/group",
            params={
                'id': ','.join(map(str, city_ids)),
                'units': 'metric',
                'appid': API_KEY,
                'lang': 'ru'
            }
        )
        response.raise_for_status()
        return response.json().get('list', [])
    except Exception as e:
        print(f"Ошибка запроса: {str(e)}")
        return []


def update_cache():
    """Обновление кэша данных с задержкой между группами"""
    now = time.time()
    if now - weather_cache['last_update'] < UPDATE_INTERVAL:
        return
    try:
        major_data = fetch_weather_group(CITY_GROUPS['major'])
        time.sleep(1)
        central_data = fetch_weather_group(CITY_GROUPS['central'])
        time.sleep(1)
        north_west_data = fetch_weather_group(CITY_GROUPS['north_west'])
        time.sleep(1)
        southern_data = fetch_weather_group(CITY_GROUPS['southern'])
        time.sleep(1)
        north_caucasian_data = fetch_weather_group(CITY_GROUPS['north_caucasian'])
        time.sleep(1)
        privolzhsky_data = fetch_weather_group(CITY_GROUPS['privolzhsky'])
        time.sleep(1)
        ural_data = fetch_weather_group(CITY_GROUPS['ural'])
        time.sleep(1)
        siberian_data = fetch_weather_group(CITY_GROUPS['siberian'])
        time.sleep(1)
        far_eastern_data = fetch_weather_group(CITY_GROUPS['far_eastern'])

        time.sleep(REQUEST_DELAY)
        weather_cache.update({
            'last_update': now,
            'major': major_data,
            'southern': southern_data,
            'central': central_data,
            'north_west': north_west_data,
            'north_caucasian': north_caucasian_data,
            'privolzhsky': privolzhsky_data,
            'ural': ural_data,
            'siberian': siberian_data,
            'far_eastern': far_eastern_data,
        })
    except Exception as e:
        print(f"Ошибка обновления кэша: {str(e)}")


def format_city_data(raw_data):
    """Форматирование данных о городах"""
    # time.sleep(1)
    return [{
        'name': RUSSIAN_NAMES.get(city.get('id'), city.get('name', 'Неизвестно')),
        'temp': city['main']['temp']
    } for city in raw_data]


def search_city(city_name):
    """Поиск погоды для отдельного города"""
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                'q': city_name,
                'units': 'metric',
                'appid': API_KEY,
                'lang': 'ru'
            }
        )
        response.raise_for_status()
        data = response.json()
        return {
            'name': data['name'],
            'temp': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind': data['wind']['speed']
        }
    except Exception as e:
        print(f"Ошибка поиска: {str(e)}")
        return None


def get_city_by_ip(ip):
    """Определение города по IP-адресу"""
    try:
        IP_GEOLOCATION_API = f"http://ip-api.com/json/{ip}?fields=status,message,city"
        response = requests.get(
            IP_GEOLOCATION_API.format(ip=ip),
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        if data['status'] == 'success':
            return data['city']
        return None
    except Exception as e:
        print(f"Ошибка IP-геолокации: {str(e)}")
        return None


def format_city_data(raw_data):
    """Форматирование данных о городах"""
    formatted = []
    for city in raw_data:
        try:
            city_info = {
                'name': RUSSIAN_NAMES.get(
                    city.get('id'),
                    city.get('name', 'Неизвестно')
                ),
                'temp': city.get('main', {}).get('temp', 'N/A')
            }
            formatted.append(city_info)
        except KeyError as e:
            print(f"Ошибка форматирования города: {e}")
    return formatted


def process_forecast_data(data):
    """Обработка данных прогноза"""
    processed = []
    if not data or 'list' not in data:
        return processed
    for entry in data['list']:
        try:
            dt = datetime.fromtimestamp(entry['dt'])
            temp = entry.get('main', {})
            weather = entry.get('weather', [{}])[0]
            processed.append({
                'date': dt.strftime('%d.%m.%Y'),
                'weekday': dt.strftime('%A'),
                'temp_day': round(temp.get('temp', 0)),
                'temp_night': round(temp.get('temp_min', 0)),
                'description': weather.get('description', '').capitalize(),
                'icon': weather.get('icon', ''),
                'humidity': temp.get('humidity', 0),
                'wind': entry.get('wind', {}).get('speed', 0)
            })
        except Exception as e:
            print(f"Ошибка обработки прогноза: {e}")
    return processed


def get_weekly_forecast(city):
    """Получение прогноза на неделю через OpenWeatherMap API"""
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params={
                'q': city,
                'units': 'metric',
                'appid': API_KEY,
                'lang': 'ru',
                'cnt': 40  # 5 дней * 8 интервалов = 40 записей
            }
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка запроса прогноза: {e}")
        return None


def get_daily_forecast(city):
    """Получение прогноза на ближайшие 24 часа с группировкой по времени суток"""
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params={
                'q': city,
                'units': 'metric',
                'appid': API_KEY,
                'lang': 'ru',
                'cnt': 12  # 36 часов (12 интервалов по 3 часа)
            }
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка запроса прогноза: {e}")
        return None


def group_by_time_period(data):
    """Группировка данных по времени суток"""
    periods = {
        'night': {'start': 0, 'end': 6, 'data': [], 'name': 'Ночь'},
        'morning': {'start': 6, 'end': 12, 'data': [], 'name': 'Утро'},
        'day': {'start': 12, 'end': 18, 'data': [], 'name': 'День'},
        'evening': {'start': 18, 'end': 24, 'data': [], 'name': 'Вечер'}
    }
    for entry in data.get('list', []):
        dt = datetime.fromtimestamp(entry['dt'])
        hour = dt.hour
        for period in periods.values():
            if period['start'] <= hour < period['end']:
                period['data'].append(entry)
                break
    return periods


def calculate_period_stats(period):
    """Расчет средних значений для периода"""
    if not period['data']:
        return None
    temps = [item['main']['temp'] for item in period['data']]
    feels_like = [item['main']['feels_like'] for item in period['data']]
    humidity = [item['main']['humidity'] for item in period['data']]
    wind = [item['wind']['speed'] for item in period['data']]
    last_entry = period['data'][-1]
    return {
        'name': period['name'],
        'temp': round(sum(temps)/len(temps)),
        'feels_like': round(sum(feels_like)/len(feels_like)),
        'humidity': round(sum(humidity)/len(humidity)),
        'wind': round(sum(wind)/len(wind), 1),
        'icon': last_entry['weather'][0]['icon'],
        'description': last_entry['weather'][0]['description'].capitalize()
    }

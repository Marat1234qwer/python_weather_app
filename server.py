from flask import Flask, render_template, request
import time
from functions import search_city, get_weekly_forecast, process_forecast_data, group_by_time_period, calculate_period_stats, \
    update_cache, format_city_data, get_city_by_ip, weather_cache


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    search_result = None
    forecast = None
    error = None
    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        if city:
            search_result = search_city(city)
            forecast_data = get_weekly_forecast(city)
            if forecast_data and forecast_data.get('cod') == '200':
                forecast = {
                    'city': forecast_data.get('city', {}).get('name', city),
                    'days': process_forecast_data(forecast_data)[::8]  # Берем по одному значению в день
                }
                grouped_data = group_by_time_period(forecast_data)
                daily_forecast = {
                    'city': forecast_data['city']['name'],
                    'periods': [calculate_period_stats(p) for p in grouped_data.values()]
                }
                daily_forecast['periods'] = [p for p in daily_forecast['periods'] if p]
            if not search_result and not forecast:
                error = "Город не найден. Проверьте название."
    else:
        try:
            # ip = request.remote_addr
            # city = get_city_by_ip(ip)
            city = 'Moscow'
            if city:
                search_result = search_city(city)
                forecast_data = get_weekly_forecast(city)
                if forecast_data:
                    forecast = {
                        'city': city,
                        'days': process_forecast_data(forecast_data)[::8]
                    }
                grouped_data = group_by_time_period(forecast_data)
                daily_forecast = {
                    'city': forecast_data['city']['name'],
                    'periods': [calculate_period_stats(p) for p in grouped_data.values()]
                }
                daily_forecast['periods'] = [p for p in daily_forecast['periods'] if p]

        except Exception as e:
            print(f"Ошибка автоматического определения: {e}")

    update_cache()

    return render_template(
        'index.html',
        major_cities=format_city_data(weather_cache['major']),
        central_cities=format_city_data(weather_cache['central']),
        north_west_cities=format_city_data(weather_cache['north_west']),
        southern_cities=format_city_data(weather_cache['southern']),
        north_caucasian_cities=format_city_data(weather_cache['north_caucasian']),
        privolzhsky_cities=format_city_data(weather_cache['privolzhsky']),
        ural_cities=format_city_data(weather_cache['ural']),
        siberian_cities=format_city_data(weather_cache['siberian']),
        far_eastern_cities=format_city_data(weather_cache['far_eastern']),
        update_time=time.ctime(weather_cache['last_update']),
        search_result=search_result,
        forecast=forecast,
        daily_forecast=daily_forecast,
        error=error
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

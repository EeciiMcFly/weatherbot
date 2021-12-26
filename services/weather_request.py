from typing import Type

import requests as req
import json

from services.weatherInfo import WeatherInfo


class WeatherRequester():
    weather_api_key = ''
    lang = 'ru'

    def get_weather(city_name: str) -> Type[WeatherInfo]:
        url_weather_key = 'http://api.openweathermap.org/data/2.5/weather?' \
                          f'q={city_name}&appid={WeatherRequester.weather_api_key}&lang={WeatherRequester.lang}&units=metric'
        resp_loc = req.get(url_weather_key)
        if resp_loc.status_code != 200:
            return None
        json_data = json.loads(resp_loc.text)
        weather = json_data['weather'][0]
        main = json_data['main']
        wind = json_data['wind']

        weather_info = WeatherInfo
        weather_info.temp = main['temp']
        weather_info.temp_like = main['feels_like']
        weather_info.weather_class = weather['main']
        weather_info.weather_description = weather['description']
        weather_info.wind_speed = wind['speed']

        return weather_info




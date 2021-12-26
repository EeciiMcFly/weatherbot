import os
import telebot

from dotenv import load_dotenv
from services.weather_request import WeatherRequester
from services.weatherInfo import WeatherInfo

load_dotenv(".env")
token = os.environ.get('BOT_TOKEN')

weather_requester = WeatherRequester
weather_requester.weather_api_key = os.environ.get('WEATHER_TOKEN')
weather_requester.lang = os.environ.get('TEXT_LANG')
bot = telebot.TeleBot(token)


@bot.message_handler(command=['/start', '/help'])
def send_welcome(message):
    process_start(message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    message_text = message.text.lower()

    if (message_text == '/start'):
        process_start(message)
        return

    weather_info = weather_requester.get_weather(message_text)
    if weather_info is None:
        bot.send_message(message.from_user.id, f'Город с названием {message_text} не найден. Попробуйте снова.')
        return

    answer = construct_weather_answer(message_text, weather_info)
    bot.send_message(message.from_user.id, answer)


def process_start(message):

    bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}.' +
                     f' Я - бот, который расскажет тебе о погоде на данный момент в любом городе.' +
                     f' Для этого достаточно ввести наименование города, и я узнаю погоду для тебя.')


def construct_weather_answer(city_name: str, weather_info: WeatherInfo) -> str:
    rounded_temp = round(weather_info.temp)
    rounded_temp_like = round(weather_info.temp_like)
    answer = f'В городе {city_name.capitalize()} сейчас {weather_info.weather_description}.'
    answer = answer + f' Температура воздуха {rounded_temp} градусов цельсия, ощущается как {rounded_temp_like}.'
    answer += f' Скорость ветра {weather_info.wind_speed} м/с.'
    return answer


bot.polling(none_stop=True)

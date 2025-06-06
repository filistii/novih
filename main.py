import telebot
import requests

TOKEN = '7174618825:AAH4yLxwA461rKfCUPc3ldCgj36-mRpCcJ4'
YANDEX_API_KEY = '395d583f-a699-4374-90f5-d7bc56fa299c'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Отправь геолокацию — подскажу, что рядом.")

@bot.message_handler(content_types=['location'])
def location(message):
    latitude = message.location.latitude
    longitude = message.location.longitude

    url = 'https://search-maps.yandex.ru/v1/'
    params = {
        'apikey': YANDEX_API_KEY,
        'text': 'еда',
        'lang': 'ru_RU',
        'll': f'{longitude},{latitude}',
        'type': 'biz',
        'results': 5
    }

    try:
        res = requests.get(url, params=params)
        if res.status_code != 200:
            bot.send_message(message.chat.id, f"Ошибка {res.status_code}")
            return

        data = res.json()
        features = data.get('features', [])
        if not features:
            bot.send_message(message.chat.id, "Ничего не нашлось.")
            return

        for place in features:
            name = place['properties']['CompanyMetaData']['name']
            address = place['properties']['CompanyMetaData']['address']
            bot.send_message(message.chat.id, f"{name}\n{address}")

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

# === Запуск ===
if __name__ == '__main__':
    bot.remove_webhook()
    bot.polling(none_stop=True)

import telebot
import requests

# Замените на свой токен и API ключ
TOKEN = '7174618825:AAH4yLxwA461rKfCUPc3ldCgj36-mRpCcJ4'
YANDEX_API_KEY = '395d583f-a699-4374-90f5-d7bc56fa299c'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Отправь мне свою геопозицию, и я подберу места рядом.")

@bot.message_handler(content_types=['location'])
def handle_location(message):
    latitude = message.location.latitude
    longitude = message.location.longitude

    url = 'https://search-maps.yandex.ru/v1/'
    params = {
        'apikey': YANDEX_API_KEY,
        'text': 'еда',  # можно менять под настроение
        'lang': 'ru_RU',
        'll': f'{longitude},{latitude}',
        'type': 'biz',
        'results': 5
    }

    try:
        response = requests.get(url, params=params)
        print("STATUS:", response.status_code)
        print("RESPONSE TEXT:", response.text)

        if response.status_code != 200:
            bot.send_message(message.chat.id, f"Ошибка: статус {response.status_code}")
            return

        data = response.json()
        features = data.get('features', [])

        if not features:
            bot.send_message(message.chat.id, "Ничего не нашлось рядом 😢")
            return

        for feature in features:
            name = feature['properties']['CompanyMetaData']['name']
            address = feature['properties']['CompanyMetaData']['address']
            bot.send_message(message.chat.id, f"{name}\n{address}")

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при получении данных: {e}")
        print("ОШИБКА:", e)

# Запуск polling без конфликтов
if __name__ == '__main__':
    try:
        bot.delete_webhook()
    except:
        pass
    bot.polling(none_stop=True)

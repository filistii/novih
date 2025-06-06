import telebot
import requests

# Вставь сюда токен своего бота
TOKEN = '7174618825:AAH4yLxwA461rKfCUPc3ldCgj36-mRpCcJ4'
bot = telebot.TeleBot(TOKEN)

# Вставь сюда API ключ от Yandex Places
YANDEX_API_KEY = '395d583f-a699-4374-90f5-d7bc56fa299c'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Отправь мне свою геопозицию, и я подскажу интересные места рядом 🌍")

@bot.message_handler(content_types=['location'])
def handle_location(message):
    latitude = message.location.latitude
    longitude = message.location.longitude

    url = "https://search-maps.yandex.ru/v1/"
    params = {
        'apikey': YANDEX_API_KEY,
        'text': 'кафе',  # можешь заменить на 'парк', 'музей', 'бар' и т.д.
        'lang': 'ru_RU',
        'll': f"{longitude},{latitude}",
        'type': 'biz',
        'results': 3,
        'spn': '0.01,0.01'
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'features' in data and data['features']:
        reply = "📍 Вот что нашлось рядом:\n\n"
        for place in data['features']:
            name = place['properties']['name']
            address = place['properties']['CompanyMetaData']['address']
            reply += f"🍽 {name}\n📍 {address}\n\n"
    else:
        reply = "Ничего не нашёл поблизости. Попробуй другое место."

    bot.send_message(message.chat.id, reply)

bot.polling()

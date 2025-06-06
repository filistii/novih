import telebot
import requests

# 🔐 Вставь свой токен Telegram
TELEGRAM_TOKEN = "7174618825:AAH4yLxwA461rKfCUPc3ldCgj36-mRpCcJ4"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# 🔑 Вставь сюда API-ключ от Яндекс Карт (Places API)
YANDEX_API_KEY = "395d583f-a699-4374-90f5-d7bc56fa299c"

# 📡 Удаление Webhook (иначе будет ошибка 409)
requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/deleteWebhook")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(message.chat.id, "Отправь мне свою геопозицию, и я подскажу интересные места рядом.")


@bot.message_handler(content_types=['location'])
def handle_location(message):
    latitude = message.location.latitude
    longitude = message.location.longitude

    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}"
    }

    categories = ["cafe", "park", "museum"]  # типы заведений
    results = []

    for category in categories:
        url = (
            f"https://search-maps.yandex.ru/v1/?text={category}&"
            f"ll={longitude},{latitude}&"
            f"spn=0.01,0.01&"
            f"results=3&type=biz&lang=ru_RU"
        )
        response = requests.get(url, headers=headers)

        try:
            places = response.json().get("features", [])
            for place in places:
                name = place["properties"]["CompanyMetaData"]["name"]
                address = place["properties"]["CompanyMetaData"].get("address", "Адрес не указан")
                results.append(f"📍 {name}\n📫 {address}")
        except Exception as e:
            results.append(f"Ошибка при получении данных: {str(e)}")

    reply = "\n\n".join(results) if results else "Ничего не найдено рядом."
    bot.send_message(message.chat.id, reply)


if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)

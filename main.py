import telebot

TOKEN = 'твой_токен_сюда'
bot = telebot.TeleBot(TOKEN)

# Очистка webhook перед запуском polling
bot.remove_webhook()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь свои координаты, и я подберу места рядом.")

@bot.message_handler(content_types=['location'])
def handle_location(message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    # Здесь твоя логика подбора мест (заглушка)
    reply = f"Получены координаты: {latitude}, {longitude}. Скоро подберу места!"
    bot.send_message(message.chat.id, reply)

@bot.message_handler(func=lambda m: True)
def ask_for_location(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button = telebot.types.KeyboardButton(text="Отправить местоположение", request_location=True)
    markup.add(button)
    bot.send_message(message.chat.id, "Пожалуйста, отправь свои координаты", reply_markup=markup)

if __name__ == '__main__':
    bot.polling(none_stop=True)

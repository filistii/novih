import telebot
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(message.chat.id, "Привет! Отправь свою геолокацию, и я подскажу интересные места рядом.")

@bot.message_handler(content_types=['location'])
def handle_location(message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    bot.send_message(message.chat.id, f"Ты находишься здесь: {latitude}, {longitude} 🌍")

bot.polling()

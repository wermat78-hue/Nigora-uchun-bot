import os
import telebot
from google import genai
from threading import Thread
from flask import Flask  # Render portni topishi uchun kerak

# Kichik veb-server yaratamiz
app = Flask('')

@app.route('/')
def home():
    return "Bot ishlamoqda!"

def run_web_server():
    # Render avtomatik beradigan PORT'ni o'qiymiz, bo'lmasa 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Kalitlarni o'qish
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
ai_client = genai.Client(api_key=GEMINI_API_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom aka! Men SI bilan bog'langan botman. Savolingizni bering!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.text
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Xatolik bo'ldi, qaytadan yozib ko'ring.")
        print(f"Xato: {e}")

if __name__ == "__main__":
    # Veb-serverni alohida oqimda (thread) fonda ishga tushiramiz
    server_thread = Thread(target=run_web_server)
    server_thread.start()
    
    # Botni ishga tushiramiz
    print("Bot tayyor...")
    bot.infinity_polling()

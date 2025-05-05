from flask import Flask
import threading
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

app = Flask(__name__)

# === Telegram Bot Initialization ===
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")  # добавь переменную в Environment на Render
bot = Bot(token=TELEGRAM_TOKEN)
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# === Handlers ===
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я бот.")

dispatcher.add_handler(CommandHandler("start", start))

# === One-time startup logic ===
started = False
lock = threading.Lock()

@app.before_request
def initialize():
    global started
    with lock:
        if not started:
            print(">>> Запускаем Telegram бота")
            threading.Thread(target=updater.start_polling, daemon=True).start()
            started = True

# === Flask route for health check ===
@app.route('/')
def home():
    return "Bot is running!"

# === Run the Flask app ===
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

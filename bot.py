import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# === Bot initialization (v20+ style) ===
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# === Command handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот работает.")

application.add_handler(CommandHandler("start", start))

# === Run bot in background on first request ===
started = False
lock = threading.Lock()

@app.before_request
def start_bot():
    global started
    with lock:
        if not started:
            print(">>> Запуск Telegram бота")
            threading.Thread(target=application.run_polling, daemon=True).start()
            started = True

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

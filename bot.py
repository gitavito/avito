import os
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

app = Flask(__name__)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# === Обработчик команды /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот работает!")

# === Flask маршрут ===
@app.route('/')
def home():
    return "Bot is alive!"

# === Запуск Flask в отдельном потоке ===
def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# === Основной async запуск бота ===
async def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    # Запускаем polling без завершения asyncio loop
    await application.run_polling(close_loop=False)

if __name__ == '__main__':
    # Flask — в отдельном потоке
    Thread(target=run_flask).start()

    # Telegram бот
    asyncio.run(main())

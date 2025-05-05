import os
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# === Команда бота ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот работает.")

# === Flask маршрут для проверки ===
@app.route('/')
def home():
    return "Bot is alive!"

# === Запуск бота ===
if __name__ == '__main__':
    import asyncio

    async def main():
        app_bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        app_bot.add_handler(CommandHandler("start", start))

        # Запускаем Flask в отдельной задаче
        from threading import Thread
        Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))).start()

        # Запускаем Telegram бота (async run)
        await app_bot.run_polling()

    asyncio.run(main())

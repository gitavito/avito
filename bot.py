from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import os

TOKEN = "7639773519:AAESWhB_vQH5g1cA1vIqhYN3PgVpAbaL1AM"
WEBHOOK_URL = "https://antilogo-bot.onrender.com/webhook"

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот успешно запущен 🚀")

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Вот список доступных команд:\n/start — запустить бота\n/help — помощь")

# Подключаем команды
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

# Главная страница
@app.route("/")
def home():
    return "Бот работает!"

# Обработка Webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Установка Webhook при первом запросе
def before_first():
    # сюда вставь нужный тебе код, который должен выполняться перед первым запросом
    print("Бот запущен и готов к работе.")

def set_webhook():
    application.bot.set_webhook(WEBHOOK_URL)

# Запуск сервера Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.environ.get("TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

app = Flask(__name__)
bot = Bot(token=TOKEN)

application = Application.builder().token(TOKEN).build()

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я работаю ✅")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Список команд:\n/start — запустить бота\n/help — помощь")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

# Главная страница
@app.route("/")
def home():
    return "Бот работает!"

# Webhook при старте
@app.before_first_request
def before_first():
    print("Бот запущен и готов к работе.")
    application.bot.set_webhook(WEBHOOK_URL)

# Webhook-обработка
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Запуск Flask-сервера
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging

# Включаем логирование (для Render логов)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Ответ на команду /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот успешно работает! 🟢")

# Точка входа
def main():
    # Замени здесь на свой токен
    TOKEN = "ВСТАВЬ_СЮДА_СВОЙ_ТОКЕН"

    app = ApplicationBuilder().token(TOKEN).build()

    # Обработка команды /start
    app.add_handler(CommandHandler("start", start))

    # Запуск бота
    app.run_polling()

if __name__ == "__main__":
    main()

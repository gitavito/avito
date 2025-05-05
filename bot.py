import os
import requests
from bs4 import BeautifulSoup
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from PIL import Image
from io import BytesIO

TOKEN = "7639773519:AAESWhB_vQH5g1cA1vIqhYN3PgVpAbaL1AM"

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "avito" not in text:
        await update.message.reply_text("Пришли ссылку на Avito")
        return

    await update.message.reply_text("Обрабатываю ссылку...")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(text, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        images = []
        for img_tag in soup.find_all("img"):
            src = img_tag.get("src") or img_tag.get("data-src")
            if src and "avatars" in src and src.endswith(".jpg"):
                images.append(src)

        if not images:
            await update.message.reply_text("Фотографии не найдены.")
            return

        for i, url in enumerate(images):
            img_data = requests.get(url).content
            image = Image.open(BytesIO(img_data))

            # Удаляем водяной знак — обрезаем низ (пример)
            width, height = image.size
            cropped = image.crop((0, 0, width, height - 50))

            output = BytesIO()
            cropped.save(output, format="JPEG")
            output.seek(0)

            await update.message.reply_photo(photo=InputFile(output, filename=f"photo_{i}.jpg"))

    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_link))
app.run_polling()


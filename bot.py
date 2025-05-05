import re
import json
import requests
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from PIL import Image
from io import BytesIO

TOKEN = "7639773519:AAESWhB_vQH5g1cA1vIqhYN3PgVpAbaL1AM"

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "avito" not in url:
        await update.message.reply_text("Пришли ссылку на Avito")
        return

    await update.message.reply_text("Ищу фото...")

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)

        match = re.search(r"window.__initialData__\s*=\s*({.*?});", res.text)
        if not match:
            await update.message.reply_text("Не смог найти данные на странице Avito.")
            return

        data = json.loads(match.group(1))
        images = []
        try:
            images_data = data["props"]["pageProps"]["item"]["images"]
            for img in images_data:
                orig = img.get("fullSizeUrl")
                if orig:
                    images.append(orig)
        except Exception:
            await update.message.reply_text("Ошибка при извлечении изображений.")
            return

        if not images:
            await update.message.reply_text("Фотографии не найдены.")
            return

        for i, img_url in enumerate(images):
            img_data = requests.get(img_url, headers=headers).content
            image = Image.open(BytesIO(img_data))
            width, height = image.size
            cropped = image.crop((0, 0, width, height - 50))

            output = BytesIO()
            cropped.save(output, format="JPEG")
            output.seek(0)
            await update.message.reply_photo(photo=InputFile(output, filename=f"photo_{i}.jpg"))

    except Exception as e:
        await update.message.reply_text(f"Ошибка при обработке: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_link))
app.run_polling()

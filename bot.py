import os
import asyncio
from io import BytesIO
from PIL import Image
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from playwright.async_api import async_playwright

TOKEN = "7639773519:AAESWhB_vQH5g1cA1vIqhYN3PgVpAbaL1AM"

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "avito" not in text:
        await update.message.reply_text("Пришли ссылку на Avito")
        return

    await update.message.reply_text("Парсю фотки...")

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(text, timeout=60000)

            # ждём, пока картинки появятся
            await page.wait_for_selector("img", timeout=15000)

            image_elements = await page.query_selector_all("img")
            images = []

            for img in image_elements:
                src = await img.get_attribute("src")
                if src and "avatars" in src and src.endswith(".jpg"):
                    images.append(src)

            await browser.close()

        if not images:
            await update.message.reply_text("Фотографии не найдены.")
            return

        for i, url in enumerate(images):
            from aiohttp import ClientSession
            async with ClientSession() as session:
                async with session.get(url) as resp:
                    img_data = await resp.read()

            image = Image.open(BytesIO(img_data))
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

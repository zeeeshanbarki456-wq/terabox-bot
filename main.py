from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

import os
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Send TeraBox link")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "terabox" not in url:
        await update.message.reply_text("❌ Please send valid TeraBox link")
        return

    msg = await update.message.reply_text("⏳ Processing...")

    try:
        # API 1
        api1 = f"https://terabox-dl.vercel.app/api?url={url}"
        res = requests.get(api1).json()

        if "download_url" in res:
            link = res["download_url"]
        else:
            # API 2 fallback
            api2 = f"https://terabox-downloader-api.vercel.app/api?url={url}"
            res2 = requests.get(api2).json()
            link = res2.get("download_url")

        if link:
            button = [[InlineKeyboardButton("⬇️ Download", url=link)]]
            reply_markup = InlineKeyboardMarkup(button)

            await msg.edit_text(
                "✅ Your file is ready:",
                reply_markup=reply_markup
            )
        else:
            await msg.edit_text("❌ Failed, try another link")

    except:
        await msg.edit_text("⚠️ Error occurred")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()

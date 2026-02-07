from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI
import os, re

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

ADMIN_IDS = [8184492637]

BAD_WORDS = ["anjing", "bangsat", "kontol", "tolol", "babi"]

def is_bad_word(text):
    return any(word in text.lower() for word in BAD_WORDS)

def contains_link(text):
    return bool(re.search(r"http|www|t.me", text.lower()))

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user_id = message.from_user.id
    text = message.text

    if is_bad_word(text):
        await message.delete()
        return

    if contains_link(text) and user_id not in ADMIN_IDS:
        await message.delete()
        return

    if "xauusd" in text.lower() or "gold" in text.lower():
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Kamu AI analis XAUUSD komunitas Bandit Profit."},
                {"role": "user", "content": text}
            ]
        )
        await message.reply_text(response.choices[0].message.content)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()

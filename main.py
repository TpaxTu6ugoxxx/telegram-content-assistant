import os
import logging
import openai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

# Загружаем токены
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я AI-контент бот. Напиши /пост <тема>, и я сгенерирую пост 💡")

# /пост <тема>
async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = ' '.join(context.args)
    if not topic:
        await update.message.reply_text("⚠️ Укажи тему после команды: /пост <тема>")
        return

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"Напиши креативный Instagram-пост на тему: {topic}"}
        ]
    )

    await update.message.reply_text(response.choices[0].message.content)

# Запускаем приложение
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("post", post))
print("Бот запущен 🚀")
app.run_polling()

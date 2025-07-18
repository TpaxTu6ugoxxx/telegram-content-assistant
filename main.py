import os
import openai
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Загрузка переменных
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")

# /start — приветствие
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет, я твой контент-бот 😊 Напиши /пост <тема>, и я сгенерирую текст для соцсетей.")

# /пост <тема> — генерация с GPT
async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = ' '.join(context.args)
    if not topic:
        await update.message.reply_text("Пожалуйста, укажи тему после команды: /пост <тема>")
        return

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"Напиши пост на тему: {topic}. Стиль — Instagram, разговорный, вдохновляющий."}
        ]
    )

    content = response.choices[0].message.content
    await update.message.reply_text(content)

# Запуск приложения
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("пост", post))
print("Бот запущен 🚀")
app.run_polling()

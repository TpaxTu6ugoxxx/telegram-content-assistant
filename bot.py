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
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я AI-бот для блогеров 😊 Выбери язык и начни генерацию контента!")

# Команда /пост <тема>
async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = ' '.join(context.args)
    if not topic:
        await update.message.reply_text("Укажи тему: /пост <тема>")
        return

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"Напиши пост на тему: {topic}. Стиль: Instagram, дружелюбный."}
        ]
    )
    await update.message.reply_text(response['choices'][0]['message']['content'])

# Запуск приложения
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("пост", post))
print("Бот запущен 🚀")
app.run_polling()

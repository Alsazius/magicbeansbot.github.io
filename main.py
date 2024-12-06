import logging
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Ваш токен и ваш личный чат ID
TOKEN = '8013164614:AAEwW5nkaNQK7JbbRvdFPPySsFj2koVqbkg'
CHAT_ID = '1513738070'  # Ваш личный Telegram ID
KEYWORDS = ['1', '2']  # Ключевые слова для отслеживания

# Регулярное выражение для поиска ссылок
URL_PATTERN = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+!*\\(\\),]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Бот запущен. Я отслеживаю ключевые слова и ссылки.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    # Проверяем наличие ключевых слов или ссылок в сообщении
    if any(keyword in message_text for keyword in KEYWORDS) or re.search(URL_PATTERN, message_text):
        # Пересылаем сообщение вам
        await context.bot.forward_message(chat_id=CHAT_ID, from_chat_id=update.message.chat.id, message_id=update.message.message_id)

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущен.")
    application.run_polling()

if __name__ == '__main__':
    main()
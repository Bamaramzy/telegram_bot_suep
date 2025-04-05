from typing import Final
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
)
from chat_ai import chat_with_gf 
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN: Final = os.getenv('BOT_TOKEN')
BOT_USERNAME: Final = '@suueeeppppbot'

# ✅ /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi, I'm your sweet virtual girlfriend 💖 Just talk to me!")

# ✅ /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You can just chat with me ❤️\nType 'reset' to clear the conversation.")

# ✅ /custom
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command!")

# ✅ Chat handler (menggunakan AI)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    user_id = update.message.chat.id
    print(f'User ({user_id}): {text}')

    response = chat_with_gf(text)  # 🔁 Balasan dari AI DialoGPT
    print(f'GF: {response}')
    await update.message.reply_text(response)

# ✅ Error log
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

# ✅ Run bot
if __name__ == '__main__':
    print('Bot started...')
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)

# py -3.11 main.py gae njalakno bot e
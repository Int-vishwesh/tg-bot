from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
#
#TOKEN = '7591928251:AAGCfZL9EKMbBJL98ZmXK0j-yaNROuHfBmA' 

#insta_saver_free_bot
TOKEN = '7563947895:AAHsGF3rP4j89BA3Eu8sjpDEEFGKvpqAGNI'

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I'm your test bot. Use /help to see what I can do.")

# Command: /help
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "Here are the commands you can use:\n"
        "/start - Start the bot\n"
        "/help - Show available commands\n"
        "/social - Get my social media link\n"
    )
    await update.message.reply_text(help_text)

# Command: /social
async def social(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Follow me on \n Instagram: https://instagram.com/actually.jerry \n youtube: https://youtube.com/@jerry_aryan \n github: https://github.com/Int-vishwesh ")

# Main function to set up the bot
def main():
    # Initialize the bot with your token
    app = Application.builder().token(TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("social", social))

    # Start the bot
    app.run_polling()

if __name__ == '__main__':
    main()

from telegram import Bot
from telegram.ext import Application, CommandHandler
from telegram.utils.request import Request

# Replace with your bot's token
TOKEN = ''

async def start(update, context):
    await update.message.reply_text("Welcome! Type /send to get a file from me.")

async def send_file(update, context):
    # Replace 'OIP.jpg' with the correct local file path
    file_path = 'OIP.jpg'  # Ensure this file exists in your working directory
    
    try:
        # Open the image file in binary mode and send it
        with open(file_path, 'rb') as photo:
            await context.bot.send_photo(chat_id=update.message.chat_id, photo=photo)
    except FileNotFoundError:
        await update.message.reply_text(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

def main():
    # Set up the custom request with a higher timeout (e.g., 30 seconds)
    request = Request(con_pool_size=8, read_timeout=30, connect_timeout=30)

    # Create the Application instance with the custom request
    application = Application.builder().token(TOKEN).request(request).build()
    
    # Command handler to start the bot
    application.add_handler(CommandHandler('start', start))
    
    # Command handler to send a file
    application.add_handler(CommandHandler('send', send_file))
    
    # Start polling for updates
    application.run_polling()

if __name__ == '__main__':
    main()

import os
import logging
import instaloader
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Replace with your bot's token
TOKEN = '7591928251:AAGCfZL9EKMbBJL98ZmXK0j-yaNROuHfBmA'

# Initialize Instaloader
L = instaloader.Instaloader()

# Command: /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome to the GETinsta bot, \n send me a reel URL to download it.😇 \n \n Type /help for more info")

# Command: /help
async def help(update: Update, context: CallbackContext) -> None:
    help_text = (
        "this is a simple reel downloader, without any much difficulties \n FAST, EASY & FREE 🥸 \n Here are the commands you can use:\n"
        "/start - Start the bot\n"
        "/help - Show available commands\n"
        "/social - contact me! social media link\n"
        "to download simply send link anytime  \n"
    )
    await update.message.reply_text(help_text)

# Command: /social
async def social(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("try our website too & Follow on 😽 \n Instagram: https://instagram.com/actually.jerry \n website : https://get-insta.netlify.app \n github: https://github.com/Int-vishwesh \n linkedIN : linkedin.com/in/vishwesh-aryan-608691236")

# Function to handle messages containing reel URLs
async def handle_reel_url(update: Update, context: CallbackContext):
    url = update.message.text  # Get the URL from the message

    # Validate if the message contains an Instagram URL
    if "instagram.com" not in url:
        await update.message.reply_text("This doesn't look like a valid Instagram URL. Please send a valid reel URL.")
        return

    await update.message.reply_text("Downloading your reel, please wait...")

    try:
        # Extract the Post object
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # Fetch the caption
        caption = post.caption or "No caption available."

        # Download the reel
        L.download_post(post, target="reel")

        # Find the downloaded file (assuming MP4 format)
        filename = next(
            file for file in os.listdir("reel") if file.endswith(".mp4")
        )

        # Send the downloaded video back to the user with caption
        with open(os.path.join("reel", filename), 'rb') as video:
            await update.message.reply_video(video=video, caption=f"Caption: {caption}")

        # Clean up downloaded files
        for file in os.listdir("reel"):
            os.remove(os.path.join("reel", file))

    except Exception as e:
        logging.error(f"Error downloading reel: {e}")
        await update.message.reply_text("An error occurred while processing your request. Please ensure the URL is correct and try again.")

def main():
    # Create the Application instance
    application = Application.builder().token(TOKEN).build()
    
    # Command handler for /start
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("social", social))
    
    # Message handler for reel URLs
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reel_url))
    
    # Start polling for updates
    application.run_polling(timeout=30)

if __name__ == '__main__':
    main()

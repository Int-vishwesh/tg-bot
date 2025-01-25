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
    await update.message.reply_text("Welcome to the bot, send me a reel URL to download it.")

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
    
    # Message handler for reel URLs
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reel_url))
    
    # Start polling for updates
    application.run_polling(timeout=30)

if __name__ == '__main__':
    main()

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import instaloader
import os
import tempfile
from urllib.parse import urlparse

#7563947895:AAHsGF3rP4j89BA3Eu8sjpDEEFGKvpqAGNI
# Token should be securely stored in environment variables
TOKEN = os.getenv("7563947895:AAHsGF3rP4j89BA3Eu8sjpDEEFGKvpqAGNI")

# Initialize Instaloader
insta_loader = instaloader.Instaloader()

# Function to download the Instagram reel
async def download_reel(link):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract the shortcode from the link
            post_shortcode = urlparse(link).path.strip("/").split("/")[-1]
            post = instaloader.Post.from_shortcode(insta_loader.context, post_shortcode)
            
            # Download the reel
            insta_loader.download_post(post, target=temp_dir)
            
            # Find the downloaded video file
            for file in os.listdir(temp_dir):
                if file.endswith(".mp4"):
                    return os.path.join(temp_dir, file)
    except Exception as e:
        print(f"Error downloading reel: {e}")
        return None

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! Send me an Instagram reel link, and I'll download and send it back to you.")

# Handler for Instagram reel links
async def handle_reel_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    link = update.message.text.strip()
    chat_id = update.message.chat_id

    if "instagram.com" not in link:
        await update.message.reply_text("Please send a valid Instagram reel link.")
        return

    file_path = await download_reel(link)

    if file_path:
        try:
            with open(file_path, "rb") as video_file:
                await context.bot.send_video(chat_id=chat_id, video=video_file)
        except Exception as e:
            await update.message.reply_text(f"Error sending the video: {e}")
        finally:
            # Ensure file cleanup
            if os.path.exists(file_path):
                os.remove(file_path)
    else:
        await update.message.reply_text("Failed to download the reel. Please check the link and try again.")

# Main function to set up the bot
def main():
    # Initialize the bot with your token
    app = Application.builder().token(TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))

    # Add message handler for Instagram reel links
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reel_link))

    # Start the bot
    app.run_polling()

if __name__ == '__main__':
    main()

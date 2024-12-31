import logging
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Bot Token (Telegram)
TOKEN = '6934514903:AAHLVkYqPEwyIZiyqEhJocOrjDYwTk9ue8Y'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to the Mega Rclone Bot! 😄 Use /rename <folder_url> <new_folder_name> to rename folders.")

# Bulk rename function using Rclone
def bulk_rename(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args) != 2:
            update.message.reply_text("Usage: /rename <folder_url> <new_folder_name>")
            return

        folder_url = context.args[0]
        new_folder_name = context.args[1]

        # Running the Rclone command to rename the folder
        command = f"rclone moveto mega:{folder_url} mega:{new_folder_name}"
        process = subprocess.run(command, shell=True, capture_output=True, text=True)

        if process.returncode == 0:
            update.message.reply_text(f"Folder renamed to: {new_folder_name}")
        else:
            update.message.reply_text(f"Error in renaming: {process.stderr}")
    
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

# Main function to start the bot
def main() -> None:
    try:
        updater = Updater(TOKEN, use_context=True)
        dispatcher = updater.dispatcher

        # Command handlers
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("rename", bulk_rename))

        # Start the bot
        updater.start_polling()
        updater.idle()
    
    except Exception as e:
        logger.error(f"Error in starting the bot: {e}")

if __name__ == '__main__':
    main()

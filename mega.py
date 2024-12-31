from mega import Mega
from telegram.ext import Updater, CommandHandler
import logging
import os

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Mega login credentials
email = 'aapka_email@gmail.com'  # Apna email daalein
password = 'aapka_password'  # Apna password daalein

# Mega instance
mega = Mega()
m = mega.login(email, password)

# Function to handle '/rename' command
def rename(update, context):
    try:
        # Get the arguments from the command
        args = context.args
        if len(args) < 2:
            update.message.reply_text("Usage: /rename <folder_url> <new_folder_name>")
            return

        folder_link = args[0]
        new_name = args[1]

        # Get the folder node using the link
        folder_node = m.get_node(folder_link)

        if folder_node is None:
            update.message.reply_text("Invalid folder link or folder not found.")
            return

        # Rename the folder
        m.rename(folder_node, new_name)
        update.message.reply_text(f"Folder renamed to: {new_name}")
    except Exception as e:
        logger.error(f"Error in renaming: {e}")
        update.message.reply_text("An error occurred while renaming the folder.")

# Start command to initialize bot
def start(update, context):
    update.message.reply_text("Welcome to the Mega Rename Bot! Use /rename <folder_url> <new_folder_name> to rename folders.")

# Main function to set up the bot
def main():
    # Telegram bot API token
    updater = Updater("6934514903:AAHLVkYqPEwyIZiyqEhJocOrjDYwTk9ue8Y", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Command handler for '/start' and '/rename'
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("rename", rename))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

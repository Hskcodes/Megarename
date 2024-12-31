import logging
from mega import Mega
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Bot Token (Telegram)
TOKEN = '6934514903:AAHLVkYqPEwyIZiyqEhJocOrjDYwTk9ue8Y'

# Mega credentials (email aur password yahan dena hoga)
email = 'prior.puffin.fwzf@instantletter.net'  # Apni Mega email yahan daalein
password = 'Lahore123'  # Apna Mega password yahan daalein

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Mega login function
def mega_login():
    try:
        m = Mega()
        m.login(email, password)  # Login to Mega
        return m
    except Exception as e:
        logger.error(f"Error logging in to Mega: {e}")
        return None

# Start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to the Mega Rename Bot! 😄 Use /rename <folder_url> <new_folder_name> to rename folders.")

# Login command to log into Mega account via command
def login(update: Update, context: CallbackContext) -> None:
    m = mega_login()
    if m:
        update.message.reply_text("Successfully logged in to Mega! ✅")
    else:
        update.message.reply_text("Failed to log in to Mega. Please check your credentials.")

# Rename command (Folder and files inside it)
def rename(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args) != 2:
            update.message.reply_text("Usage: /rename <folder_url> <new_folder_name>")
            return

        folder_url = context.args[0]
        new_folder_name = context.args[1]

        m = mega_login()
        if not m:
            update.message.reply_text("Failed to log in to Mega. Please use /login to log in first.")
            return

        folder = m.get_folder(folder_url)
        if not folder:
            update.message.reply_text("Folder not found. Please check the folder URL and try again.")
            return

        m.rename(folder, new_folder_name)
        update.message.reply_text(f"Folder renamed to: {new_folder_name}")

        files = m.get_files_in_folder(folder)
        for file in files:
            new_file_name = f"{new_folder_name}_{file['name']}"
            m.rename(file, new_file_name)

        update.message.reply_text(f"All files inside the folder have been renamed to include: {new_folder_name}")
    
    except Exception as e:
        update.message.reply_text(f"Error in renaming: {e}")

def main() -> None:
    try:
        updater = Updater(TOKEN, use_context=True)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("login", login))
        dispatcher.add_handler(CommandHandler("rename", rename))

        updater.start_polling()
        updater.idle()
    
    except Exception as e:
        logger.error(f"Error in starting the bot: {e}")

if __name__ == '__main__':
    main()

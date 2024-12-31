import logging
from mega import Mega
from telegram import Update  # Yeh line add ki gayi hai
from telegram.ext import Updater, CommandHandler, CallbackContext

# Bot Token (Telegram)
TOKEN = '6934514903:AAHLVkYqPEwyIZiyqEhJocOrjDYwTk9ue8Y'

# Mega credentials (email aur password yahan dena hoga)
email = 'prior.puffin.fwzf@instantletter.net'  # Apni Mega email yahan daalein
password = 'Lahore123'        # Apna Mega password yahan daalein

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Mega login function
def mega_login():
    m = Mega()
    m.login(email, password)
    return m

# Start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to the Mega Rename Bot! 😄 Use /rename <folder_url> <new_folder_name> to rename folders.")

# Login command to login to Mega account via command
def login(update: Update, context: CallbackContext) -> None:
    try:
        # Calling the mega_login function to log in
        m = mega_login()
        update.message.reply_text("Successfully logged in to Mega! ✅")
    except Exception as e:
        update.message.reply_text(f"Error during login: {e}")

# Rename command (Folder and files inside it)
def rename(update: Update, context: CallbackContext) -> None:
    try:
        # Ensure the user provides both folder URL and new folder name
        if len(context.args) != 2:
            update.message.reply_text("Usage: /rename <folder_url> <new_folder_name>")
            return

        folder_url = context.args[0]
        new_folder_name = context.args[1]

        # Log in to Mega
        m = mega_login()

        # Get folder ID and rename folder
        folder = m.get_folder(folder_url)  # Assuming the function is correct for getting folder
        
        # Renaming the main folder
        m.rename(folder, new_folder_name)
        
        # Now rename files inside the folder
        files = m.get_files_in_folder(folder)  # Get files in the folder
        for file in files:
            # Renaming each file
            new_file_name = f"{new_folder_name}_{file['name']}"
            m.rename(file, new_file_name)

        update.message.reply_text(f"Folder and all files inside it have been renamed to: {new_folder_name}")
    except Exception as e:
        update.message.reply_text(f"Error in renaming: {e}")

def main() -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("login", login))  # Added login command
    dispatcher.add_handler(CommandHandler("rename", rename))  # Rename command handler

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop it
    updater.idle()

if __name__ == '__main__':
    main()

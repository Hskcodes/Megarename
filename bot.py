import logging
from mega import Mega
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

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
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Welcome to the Mega Rename Bot! 😄 Use /rename <folder_url> <new_folder_name> to rename folders.")

# Login command to log into Mega account via command
async def login(update: Update, context: CallbackContext) -> None:
    m = mega_login()
    if m:
        await update.message.reply_text("Successfully logged in to Mega! ✅")
    else:
        await update.message.reply_text("Failed to log in to Mega. Please check your credentials.")

# Rename command (Folder and files inside it)
async def rename(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args) != 2:
            await update.message.reply_text("Usage: /rename <folder_url> <new_folder_name>")
            return

        folder_url = context.args[0]
        new_folder_name = context.args[1]

        m = mega_login()
        if not m:
            await update.message.reply_text("Failed to log in to Mega. Please use /login to log in first.")
            return

        # Getting the folder using the URL
        folder = m.find(folder_url)  # Use the `find` method to search for the folder by URL
        if not folder:
            await update.message.reply_text("Folder not found. Please check the folder URL and try again.")
            return

        # Rename the folder
        m.rename(folder, new_folder_name)
        await update.message.reply_text(f"Folder renamed to: {new_folder_name}")

        # Get all files in the folder
        files = m.get_files_in_folder(folder)
        for file in files:
            new_file_name = f"{new_folder_name}_{file['name']}"
            m.rename(file, new_file_name)

        await update.message.reply_text(f"All files inside the folder have been renamed to include: {new_folder_name}")
    
    except Exception as e:
        await update.message.reply_text(f"Error in renaming: {e}")

def main() -> None:
    try:
        # Application object for handling updates
        application = Application.builder().token(TOKEN).build()

        # Add command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("login", login))
        application.add_handler(CommandHandler("rename", rename))

        # Start polling
        application.run_polling()
    
    except Exception as e:
        logger.error(f"Error in starting the bot: {e}")

if __name__ == '__main__':
    main()

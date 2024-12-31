import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
from mega import Mega

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to login to Mega.nz
def mega_login(email, password):
    mega = Mega()
    m = mega.login(email, password)
    return m

# Function to rename files in Mega.nz folder using folder link
def rename_files_in_mega_by_link(m, folder_link, prefix, chat_id, context):
    try:
        # Extract folder ID and key from the link
        folder_id, folder_key = folder_link.split("#")
        folder_id = folder_id.split("/")[-1]

        # Load the folder using Mega.nz API
        folder = m.get_folder(folder_id, folder_key)
        files = folder['files']

        # Counter to rename files sequentially
        counter = 1

        # Rename files
        for file_id, file_info in files.items():
            file_name = file_info['name']
            file_extension = os.path.splitext(file_name)[1]
            new_name = f"{prefix}{counter}{file_extension}"
            m.rename(file_id, new_name)
            counter += 1
        
        context.bot.send_message(chat_id, f"Renaming complete! Files renamed successfully.")
    except Exception as e:
        context.bot.send_message(chat_id, f"Error: {e}")

# Command to start the bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Welcome to Mega File Renamer Bot!\n\n"
        "Commands:\n"
        "/login <email> <password> - Login to Mega.nz\n"
        "/rename <folder_link> <prefix> - Rename files in Mega.nz folder\n"
        "/help - Show this help message",
        reply_markup=ReplyKeyboardMarkup([['/login', '/help']], one_time_keyboard=True)
    )

# Command to show help
def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Commands:\n"
        "/login <email> <password> - Login to Mega.nz\n"
        "/rename <folder_link> <prefix> - Rename files in Mega.nz folder\n"
        "/start - Start the bot\n"
        "/help - Show this help message"
    )

# Command to login to Mega.nz
def login(update: Update, context: CallbackContext):
    try:
        args = context.args
        if len(args) != 2:
            update.message.reply_text("Usage: /login <email> <password>")
            return
        
        email = args[0]
        password = args[1]
        
        # Login to Mega.nz
        update.message.reply_text("Logging in to Mega.nz...")
        mega = mega_login(email, password)
        context.user_data['mega'] = mega  # Save Mega instance in user_data for current user
        
        update.message.reply_text(f"Logged in successfully to Mega.nz account: {email}")

    except Exception as e:
        update.message.reply_text(f"Error: {e}")

# Command to rename files in Mega.nz folder
def rename(update: Update, context: CallbackContext):
    try:
        args = context.args
        if len(args) != 2:
            update.message.reply_text("Usage: /rename <folder_link> <prefix>")
            return
        
        folder_link = args[0]
        prefix = args[1]

        # Ensure user is logged in to Mega.nz
        if 'mega' not in context.user_data:
            update.message.reply_text("You need to login first using /login <email> <password>")
            return
        
        # Rename files in Mega using folder link
        mega = context.user_data['mega']
        update.message.reply_text(f"Renaming files in Mega.nz folder '{folder_link}' with prefix '{prefix}'...")
        rename_files_in_mega_by_link(mega, folder_link, prefix, update.effective_chat.id, context)

    except Exception as e:
        update.message.reply_text(f"Error: {e}")

# Main function to run the bot
def main():
    # Telegram bot token
    updater = Updater("6934514903:AAHLVkYqPEwyIZiyqEhJocOrjDYwTk9ue8Y", use_context=True)
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("login", login))
    dispatcher.add_handler(CommandHandler("rename", rename))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

import os
from mega import Mega
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MEGA_EMAIL = os.getenv("MEGA_EMAIL")
MEGA_PASSWORD = os.getenv("MEGA_PASSWORD")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Initialize Mega.nz API
mega = Mega()
mega_account = mega.login(MEGA_EMAIL, MEGA_PASSWORD)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Send me a Mega.nz folder link and the new file name pattern. Example:\n\n<mega.nz_folder_link> <new_file_name_pattern>"
    )

def rename_files_in_folder(update: Update, context: CallbackContext) -> None:
    try:
        message = update.message.text.split()
        
        if len(message) < 2:
            update.message.reply_text("Please provide both the Mega.nz folder link and the new file name pattern.")
            return

        folder_link = message[0]
        new_name_pattern = " ".join(message[1:])

        # Get folder ID from Mega.nz link
        folder_metadata = mega_account.get_public_file(folder_link)

        # Get folder node ID
        folder_node_id = folder_metadata['node_id']

        # Get all files in the folder
        files_in_folder = mega_account.get_files(folder_node_id)

        # Loop through files and rename them
        for idx, file in enumerate(files_in_folder):
            # Construct new file name based on the pattern
            new_name = f"{new_name_pattern}_{idx + 1}"

            # Rename the file
            mega_account.rename(file['node_id'], new_name)
        
        update.message.reply_text(f"All files in the folder have been successfully renamed.")

    except Exception as e:
        update.message.reply_text(f"An error occurred: {str(e)}")

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, rename_files_in_folder))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
    

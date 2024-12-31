# Function to handle login command
def login(update: Update, context: CallbackContext):
    try:
        global mega_instance
        if mega_instance is None:
            mega_login()  # Login to Mega if not logged in yet
            update.message.reply_text("Logged in successfully to Mega! 🎉")
        else:
            update.message.reply_text("Already logged in to Mega! ✅")
    except Exception as e:
        update.message.reply_text(f"Error logging in: {str(e)}")

# Function to rename folder and its files
def rename_folder(update, context):
    try:
        if mega_instance is None:
            update.message.reply_text("Please log in first using /login command. 🔑")
            return

        folder_url = context.args[0]  # Folder URL
        new_name = context.args[1]  # New folder name

        # Find the folder using the URL
        folder = mega_instance.find(folder_url)

        if folder:
            # Rename the folder
            mega_instance.rename(folder, new_name)
            update.message.reply_text(f"Folder renamed to {new_name} ✅")

            # Get all files in the folder
            files = mega_instance.get_files_in_folder(folder)

            # Rename each file inside the folder
            for idx, file in enumerate(files):
                new_file_name = f"{new_name}_{idx + 1}_{file['name']}"
                mega_instance.rename(file, new_file_name)
                update.message.reply_text(f"Renamed file: {new_file_name} 📝")
            
            update.message.reply_text(f"All files inside {new_name} have been renamed and sorted. 📂")

        else:
            update.message.reply_text("Folder not found! ❌")

    except Exception as e:
        update.message.reply_text(f"An error occurred: {str(e)} ⚠️")

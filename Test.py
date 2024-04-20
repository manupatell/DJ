import pymongo
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# MongoDB connection
client = pymongo.MongoClient("mongodb+srv://Manu:Manu@manu.mudmj2s.mongodb.net/?retryWrites=true&w=majority")
db = client["telegram_bot"]
channels_collection = db["channels"]
groups_collection = db["groups"]

# Telegram bot token
TOKEN = "7028442734:AAEPswaEPv7hZk6ArX5nyX_MtA3IhGGPk78"
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Authorized user ID
AUTHORIZED_USER_ID = 6704116482


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I'm your Telegram bot.")


def save_chat_id(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    chat_type = update.message.chat.type
    if chat_type in ("group", "supergroup"):
        groups_collection.insert_one({"_id": chat_id})
        update.message.reply_text(f"Group ID {chat_id} saved successfully!")
    elif chat_type == "channel":
        channels_collection.insert_one({"_id": chat_id})
        update.message.reply_text(f"Channel ID {chat_id} saved successfully!")


def broadcast(update: Update, context: CallbackContext):
    authorized_user_id = update.effective_user.id
    if authorized_user_id != AUTHORIZED_USER_ID:
        update.message.reply_text("You are not authorized to use this command.")
        return

    message = "This is a broadcast message."
    for chat in channels_collection.find():
        chat_id = chat["_id"]
        try:
            context.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"Failed to send message to channel ID {chat_id}: {e}")

    for chat in groups_collection.find():
        chat_id = chat["_id"]
        try:
            context.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"Failed to send message to group ID {chat_id}: {e}")


start_handler = CommandHandler("start", start)
save_chat_id_handler = MessageHandler(Filters.status_update.new_chat_members, save_chat_id)
broadcast_handler = CommandHandler("broadcast", broadcast)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(save_chat_id_handler)
dispatcher.add_handler(broadcast_handler)

updater.start_polling()
updater.idle()

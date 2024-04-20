import pymongo
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# MongoDB connection
client = pymongo.MongoClient("mongodb+srv://Manu:Manu@manu.mudmj2s.mongodb.net/?retryWrites=true&w=majority")
db = client["telegram_bot"]
collection = db["channels_and_groups"]

# Telegram bot token
TOKEN = "7028442734:AAEPswaEPv7hZk6ArX5nyX_MtA3IhGGPk78"
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I'm your Telegram bot.")


def save_chat_id(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    chat_type = update.message.chat.type
    if chat_type in ("group", "supergroup", "channel"):
        collection.insert_one({"_id": chat_id, "type": chat_type})
        update.message.reply_text(f"Chat ID {chat_id} saved successfully!")


def broadcast(update: Update, context: CallbackContext):
    message = "This is a broadcast message."
    for chat in collection.find():
        chat_id = chat["_id"]
        try:
            context.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"Failed to send message to chat ID {chat_id}: {e}")


start_handler = CommandHandler("start", start)
save_chat_id_handler = MessageHandler(Filters.status_update.new_chat_members, save_chat_id)
broadcast_handler = CommandHandler("broadcast", broadcast)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(save_chat_id_handler)
dispatcher.add_handler(broadcast_handler)

updater.start_polling()
updater.idle()

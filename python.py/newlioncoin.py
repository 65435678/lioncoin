import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import random

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = os.getenv('BOT_TOKEN', '7288087434:AAEFE2pPVSOqNBJm479Fy7lIf0qMNkMXo-I')
bot = telebot.TeleBot(BOT_TOKEN)

# Store user data (this is a simple way for demonstration)
user_data = {}

# Define the keyboard layout with emojis
def main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🏠 Home", callback_data='home'),
        InlineKeyboardButton("📝 Task", callback_data='task'),
        InlineKeyboardButton("💰 Wallet", callback_data='wallet'),
        InlineKeyboardButton("💵 Earn", callback_data='earn'),
        InlineKeyboardButton("💸 Withdraw", callback_data='withdraw'),
        InlineKeyboardButton("💳 Deposit", callback_data='deposit'),
        InlineKeyboardButton("🔗 Refer", callback_data='refer')
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    # Check if user data already exists, if not, initialize it
    if user_id not in user_data:
        referral_link = f"t.me/lionecoin73bot?ref={user_id}"
        user_data[user_id] = {
            'referral_link': referral_link,
            'earned_today': 0.02000,  # Example earnings for today
            'total_balance': 0.0,      # Initialize total balance
            'deposit_addresses': {
                'LTC': "ON BULT",
                'USDT': "UQBLPI49iof-fQFTR_HEPpUcLDdIPpAYY9GD4emddUKmSqnI",
                'NOT': "ON BULT",
                'BTC': "ON BULT",
                'TON': "UQBLPI49iof-fQFTR_HEPpUcLDdIPpAYY9GD4emddUKmSqnI"
            }
        }
    
    bot.reply_to(message, "Welcome to LionCoin 🦁✨", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    user_id = call.from_user.id

    # Ensure user data exists before accessing it
    if user_id not in user_data:
        bot.answer_callback_query(call.id, "User data not found. Please start the bot again.")
        return

    if call.data == 'home':
        bot.answer_callback_query(call.id, "You are in Home 🏡")
    elif call.data == 'task':
        bot.send_message(call.message.chat.id,
                         "🔔 **Task:** Follow our Telegram channel for more updates!\n"
                        "👉 [t.me/lionecoin](YOUR_CHANNEL_LINK) 👈\n"
                         "Note: Following the channel helps you stay updated with the latest news and offers!", 
                          parse_mode='Markdown') 
    elif call.data == 'wallet':
        total_balance = user_data[user_id]['total_balance']
        bot.send_message(call.message.chat.id, 
                         f"Your total balance is **{total_balance:.5f} LionCoin**. 💰✨", 
                         parse_mode='Markdown')
    elif call.data == 'earn':
        # Simulate earning process
        earned_amount = random.uniform(0.01, 0.05)  # Random earning between 0.01 and 0.05
        user_data[user_id]['earned_today'] += earned_amount
        user_data[user_id]['total_balance'] += earned_amount
        bot.send_message(call.message.chat.id, 
                         f"You have earned **{earned_amount:.5f} LionCoin** today come back another day 💵✨\n"
                         f"Your new total balance is **{user_data[user_id]['total_balance']:.5f} LionCoin*🦁*.", 
                         parse_mode='Markdown')
    elif call.data == 'withdraw':
        bot.send_message(call.message.chat.id, 
                         "Please enter the amount you want to withdraw 💸💸 (only numbers):")
        bot.register_next_step_handler(call.message, process_withdrawal)
    elif call.data == 'deposit':
        deposit_info = "\n".join([f"{currency}: **{address}**" for currency, address in user_data[user_id]['deposit_addresses'].items()])
        bot.send_message(call.message.chat.id, 
                         f"Please deposit to the following addresses for fast withdrawals🤑:\n{deposit_info}\n\n"
                         "Note: Deposits will take approximately **10 minutes** to process.👌", 
                         parse_mode='Markdown')
    elif call.data == 'refer':
        referral_link = user_data[user_id]['referral_link']
        bot.send_message(call.message.chat.id, 
                         f"Refer your friends using this link: {referral_link} \n\n"
                         "You will earn a **20% commission** for every successful referral! 🎉💰", 
                         parse_mode='Markdown')

def process_withdrawal(message):
    user_id = message.from_user.id
    try:
        amount = float(message.text)
        if amount <= 0:
            bot.send_message(message.chat.id, "Please enter a valid amount greater than 0.")
            return
        if amount > user_data[user_id]['total_balance']:
            bot.send_message(message.chat.id, "You do not have enough balance to withdraw this amount.😔")
            return
        
        # Here you would typically process the withdrawal (e.g., send to a wallet)
        user_data[user_id]['total_balance'] -= amount  # Deduct the amount from total balance
        deposit_address = user_data[user_id]['deposit_addresses']  # Get deposit addresses
        bot.send_message(message.chat.id, 
                         f"You have successfully requested to withdraw **{amount:.5f} LionCoin**! 💸\n"
                         f"Please deposit to the following addresses for a fast withdrawal:\n"
                         f"LTC: *{deposit_address['LTC']}*\n"
                         f"USDT: *{deposit_address['USDT']}*\n"
                         f"NOT: *{deposit_address['NOT']}*\n"
                         f"BTC: *{deposit_address['BTC']}*\n"
                         f"TON: *{deposit_address['TON']}*\n"
                         f"Your new balance is **{user_data[user_id]['total_balance']:.5f} LionCoin**.", 
                         parse_mode='Markdown')
    except ValueError:
        bot.send_message(message.chat.id, "Invalid input. Please enter a numeric value.")

# Start polling for messages
bot.polling()

# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# async def coaching_selected(update, context):
#     # Extract callback query:
#     query = update.callback_query    
#     await query.answer()
#     #Get selected coaching:
#     coaching_key = query.data
#     # Store it so the next handler (phone input) knows which coaching user chose:
#     context.user_data["selected_coaching"] = coaching_key
#     # Ask user to enter phone number:
#     await query.message.reply_text("Please enter your 10-digit phone number:")

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def coaching_selected(update, context):
    query = update.callback_query
    await query.answer()

    # Extract coaching key from callback_data
    raw_key = query.data               # e.g. "coaching_pw"
    coaching_key = raw_key.replace("coaching_", "")  # "pw"

    # Store clean coaching key
    context.user_data["selected_coaching"] = coaching_key

    # Ask for phone number
    await query.message.reply_text("Please enter your 10-digit phone number:")

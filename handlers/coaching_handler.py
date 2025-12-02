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


#-----------------------------------------------------------------------------

# from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# async def coaching_selected(update, context):
#     query = update.callback_query
#     await query.answer()

#     # Extract coaching key from callback_data
#     raw_key = query.data               # e.g. "coaching_pw"
#     coaching_key = raw_key.replace("coaching_", "")  # "pw"

#     # Store clean coaching key
#     context.user_data["selected_coaching"] = coaching_key

#     # Ask for phone number
#     await query.message.reply_text("Please enter your 10-digit phone number:")
#-------------------------------------------------------------------------------------------------

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.database import update_user, get_user

async def coaching_selected(update, context):
    query = update.callback_query
    await query.answer()

    # Extract coaching key from callback_data
    raw_key = query.data               # e.g. "coaching_pw"
    coaching_key = raw_key.replace("coaching_", "")  # "pw"

    telegram_id = update.effective_user.id

    # 1. Check if user exists
    user = get_user(telegram_id)

    # 2. Create or update user
    if user:
        update_user(telegram_id, {"selected_coaching": coaching_key})
    else:
        # Optional: store minimal data until phone is provided
        update_user(telegram_id, {"telegram_id": telegram_id, "selected_coaching": coaching_key})

    # 3. Ask for phone number
    await query.message.reply_text("Please enter your 10-digit phone number:")
#-----------------------------------------------------------------------------
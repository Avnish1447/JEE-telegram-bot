from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.database import update_user, get_user
from utils.keyboards import build_class_keyboard


async def coaching_selected(update, context):
    query = update.callback_query
    await query.answer()

    # Extract coaching key from callback_data
    raw_key = query.data               # e.g. "coaching_pw"
    coaching_key = raw_key.replace("coaching_", "")  # "pw"

    telegram_id = update.effective_user.id

    # 1. Check if user exists
    user = get_user(telegram_id)

    # 2. Create or update user with selected coaching
    if user:
        update_user(telegram_id, {"selected_coaching": coaching_key})
    else:
        # Create new user with coaching selection
        update_user(telegram_id, {"telegram_id": telegram_id, "selected_coaching": coaching_key})
        user = get_user(telegram_id)  # Refresh user data

    # 3. Check if user already has a phone number
    if user and user.get("phone"):
        # User already has phone - skip to class selection
        keyboard = build_class_keyboard()
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "✅ Welcome back!\n\nPlease select your class:",
            reply_markup=reply_markup
        )
    else:
        # User doesn't have phone - ask for it
        await query.edit_message_text("Please enter your 10-digit phone number:")
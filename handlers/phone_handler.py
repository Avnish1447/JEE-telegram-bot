from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from utils.validators import normalize_phone
from utils.database import update_user
from utils.keyboards import build_batch_keyboard


async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the phone number the user sends after selecting a coaching.
    Validates, normalizes, stores it, and moves the user to batch selection.
    """
    telegram_id = update.message.from_user.id
    user_input = update.message.text.strip()

    # Validate and normalize phone
    phone = normalize_phone(user_input)
    if not phone:
        await update.message.reply_text(
            "The phone number you entered is invalid.\n"
            "Please enter a valid 10-digit mobile number:"
        )
        return

    # Retrieve previously selected coaching
    coaching_key = context.user_data.get("selected_coaching")
    if not coaching_key:
        await update.message.reply_text(
            "Please start again using /start.\n"
            "Your coaching selection was not found."
        )
        return

    # Store user
    update_user(
        telegram_id,
        {
            "telegram_id": telegram_id,
            "phone": phone,
            "selected_coaching": coaching_key,
        },
    )

    # Ask the user to select batch
    keyboard = build_batch_keyboard(coaching_key)

    await update.message.reply_text(
        "Great! Now select your batch:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

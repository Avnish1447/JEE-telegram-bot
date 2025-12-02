from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from utils.validators import normalize_phone, is_valid_phone_number, user_is_eligible
from utils.database import get_user, update_user
from utils.keyboards import build_class_keyboard


async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the user's phone number input.
    Updates existing user record or creates a minimal one.
    Checks eligibility before proceeding to class selection.
    """

    phone_input = update.message.text.strip()
    telegram_id = update.effective_user.id

    # 1️⃣ Normalize and validate phone
    phone = normalize_phone(phone_input)
    if not phone:
        await update.message.reply_text(
            "The phone number you entered is invalid. Please enter a valid 10-digit phone number:"
        )
        return

    # 2️⃣ Get user from database to check coaching selection
    user = get_user(telegram_id)
    if not user or not user.get("selected_coaching"):
        await update.message.reply_text(
            "Error: coaching selection not found. Please /start again."
        )
        return
    
    selected_coaching = user.get("selected_coaching")
    
    # 3️⃣ Update phone number in database
    update_user(telegram_id, {"phone": phone})

    # 4️⃣ Check eligibility (max 2 groups, 24h cooldown)
    eligible, reason = user_is_eligible(phone)
    if not eligible:
        await update.message.reply_text(reason)
        return

    # 5️⃣ Show class selection (Class 11, 12, or Dropper)
    keyboard = build_class_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "✅ Phone number recorded!\n\nPlease select your class:",
        reply_markup=reply_markup
    )


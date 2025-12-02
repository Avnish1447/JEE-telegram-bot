from telegram import Update
from telegram.ext import ContextTypes
from utils.database import get_user, update_user
from utils.keyboards import build_batch_keyboard
from telegram import InlineKeyboardMarkup


async def class_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles when a user selects their class (11, 12, or Dropper).
    Stores the selection and shows class-specific batch options.
    """
    query = update.callback_query
    await query.answer()
    
    telegram_id = query.from_user.id
    
    # Parse callback_data: "class_11", "class_12", or "class_dropper"
    callback_data = query.data
    if not callback_data.startswith("class_"):
        await query.edit_message_text("Invalid class selection. Please /start again.")
        return
    
    # Extract class value
    student_class = callback_data.replace("class_", "")  # "11", "12", or "dropper"
    
    # Get user from database
    user = get_user(telegram_id)
    if not user:
        await query.edit_message_text("User not found. Please /start again.")
        return
    
    # Store student class in database
    update_user(telegram_id, {"student_class": student_class})
    
    # Get coaching to show batch options
    selected_coaching = user.get("selected_coaching")
    if not selected_coaching:
        await query.edit_message_text("Coaching not found. Please /start again.")
        return
    
    # Show class-specific batch selection
    keyboard = build_batch_keyboard(selected_coaching, student_class)
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Display class name nicely
    class_display = {
        "11": "Class 11",
        "12": "Class 12",
        "dropper": "Dropper"
    }.get(student_class, student_class)
    
    await query.edit_message_text(
        f"✅ {class_display} selected!\n\nNow please select your batch:",
        reply_markup=reply_markup
    )

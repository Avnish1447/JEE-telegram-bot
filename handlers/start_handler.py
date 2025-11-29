from telegram import InlineKeyboardButton, InlineKeyboardMarkup
async def start(update, context):
    
    keyboard = [
        [InlineKeyboardButton("PW", callback_data="coaching_pw")],
        [InlineKeyboardButton("Allen", callback_data="coaching_allen")],
        [InlineKeyboardButton("Aakash", callback_data="coaching_aakash")],
        [InlineKeyboardButton("Resonance", callback_data="coaching_resonance")],
        [InlineKeyboardButton("FIITJEE", callback_data="coaching_fiitjee")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome to the JEE Simplified !\nPlease select your coaching institute:",reply_markup=reply_markup
    )
import os
import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

from handlers.start_handler import start
from handlers.coaching_handler import coaching_selected
from handlers.phone_handler import handle_phone
from handlers.invite_handler import handle_new_member
from handlers.class_handler import class_selected

from utils.database import init_db
init_db()

TOKEN = "8366729083:AAEw0jVUWkzrxpn8wNRU_KHGwVWNETRJZ9g"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    
    app = ApplicationBuilder().token(TOKEN).build()


    # 1️⃣ Start Command
    
    app.add_handler(CommandHandler("start", start))

    
    # 2️⃣ Coaching Selection Handler
    
    app.add_handler(CallbackQueryHandler(coaching_selected, pattern=r"^coaching_"))

    
    # 3️⃣ Class Selection Handler (Class 11, 12, or Dropper)
    
    app.add_handler(CallbackQueryHandler(class_selected, pattern=r"^class_"))

    
    # 4️⃣ Phone Number Handler
    # (Runs ONLY after coaching is chosen)
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_phone))

    
    # 5️⃣ Handle New Members (Invite Join)
    
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_member))

    
    # Error Handler
    
    async def on_error(update, context):
        logger.exception("Unhandled exception: %s", context.error)

    app.add_error_handler(on_error)

    app.run_polling()


if __name__ == "__main__":
    main()

from telegram import Update
from telegram.ext import ContextTypes
from utils.database import get_user, update_user
from utils.database import get_user_by_phone 

from utils.security import kick_user, safe_notify
from utils.constants import COACHINGS, INVITE_MAP
from utils.logging_utils import log_join_attempt
from datetime import datetime


async def handle_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Triggered whenever someone joins a group.
    Validates the user based on the invite link & stored bot data.
    """

    message = update.message
    chat = update.effective_chat

    if not message or not message.new_chat_members:
        return

    new_member = message.new_chat_members[0]
    telegram_id = new_member.id
    invite_link_used = message.invite_link

    # 1. Ensure invite link exists
    if invite_link_used is None:
        await kick_user(chat.id, telegram_id, context)
        return

    invite_key = invite_link_used.invite_link

    # 2. Map invite → (coaching, batch)
    coaching_key, batch_key = INVITE_MAP.get(invite_key, (None, None))
    if coaching_key is None:
        await kick_user(chat.id, telegram_id, context)
        return

    # 3. Load user from DB
    user = get_user(telegram_id)

    # Log attempt
    log_join_attempt(
        telegram_id=telegram_id,
        username=new_member.username,
        coaching=coaching_key,
        batch=batch_key,
        status="attempt"
    )

    # 4. Validation
    if not user:
        await kick_user(chat.id, telegram_id, context)
        await safe_notify(
            telegram_id,
            "You are not registered in the system.\n"
            "Please verify through the bot before joining a group.",
            context
        )
        return

    if not user.get("phone"):
        await kick_user(chat.id, telegram_id, context)
        await safe_notify(
            telegram_id,
            "Phone number verification missing.\nUse /start in the bot to complete the setup.",
            context
        )
        return

    if user.get("selected_coaching") != coaching_key:
        await kick_user(chat.id, telegram_id, context)
        await safe_notify(
            telegram_id,
            f"You tried joining a coaching you're not approved for.\n"
            f"Assigned coaching: {user.get('selected_coaching')}",
            context
        )
        return

    if user.get("banned", 0):
        await kick_user(chat.id, telegram_id, context)
        await safe_notify(
            telegram_id,
            "You are banned from this coaching group.",
            context
        )
        return

    # 5. Passed all checks → allow
    await message.reply_text(
        f"✨ Welcome {new_member.first_name}!\n"
        f"Coaching: {COACHINGS[coaching_key]['name']}\n"
        f"Batch: {batch_key}\n"
        "You have been successfully verified."
    )

    # Update DB: increment last join time, if needed
    update_user(telegram_id, {"last_join_time": datetime.utcnow().isoformat()})

    # Log success
    log_join_attempt(
        telegram_id=telegram_id,
        username=new_member.username,
        coaching=coaching_key,
        batch=batch_key,
        status="success"
    )

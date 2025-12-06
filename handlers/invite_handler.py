from telegram import Update
from telegram.ext import ContextTypes
from utils.database import get_user, update_user, increment_groups_join
from utils.database import get_user_by_phone 

from utils.security import kick_user, safe_notify
from utils.constants import COACHINGS, get_coaching_by_group_id
from utils.logging_utils import log_join_attempt
from datetime import datetime


async def handle_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Triggered whenever someone joins a group.
    Validates the user based on their stored coaching/class and the group they're joining.
    """

    message = update.message
    chat = update.effective_chat

    if not message or not message.new_chat_members:
        return

    new_member = message.new_chat_members[0]
    telegram_id = new_member.id
    group_id = chat.id

    # 1. Map group_id to coaching and class
    coaching_key, class_key = get_coaching_by_group_id(group_id)
    
    if coaching_key is None:
        # Group not configured in COACHINGS
        await kick_user(chat.id, telegram_id, context)
        await safe_notify(
            telegram_id,
            "This group is not configured in the system. Please contact admin.",
            context
        )
        return

    # 2. Load user from DB
    user = get_user(telegram_id)

    # Log attempt
    log_join_attempt(
        telegram_id=telegram_id,
        username=new_member.username,
        coaching=coaching_key,
        batch=class_key,  # Using class_key as batch for logging compatibility
        status="attempt"
    )

    # 3. Validation
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

    if user.get("student_class") != class_key:
        await kick_user(chat.id, telegram_id, context)
        await safe_notify(
            telegram_id,
            f"You tried joining a class you're not approved for.\n"
            f"Assigned class: {user.get('student_class')}",
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

    # 4. Passed all checks → allow
    class_display = {
        "11": "Class 11",
        "12": "Class 12",
        "dropper": "Dropper"
    }.get(class_key, class_key)
    
    await message.reply_text(
        f"✨ Welcome {new_member.first_name}!\n"
        f"Coaching: {COACHINGS[coaching_key]['name']}\n"
        f"Class: {class_display}\n"
        "You have been successfully verified."
    )

    # 5. Update DB: increment groups_join counter and update last join time
    increment_groups_join(telegram_id)

    # Log success
    log_join_attempt(
        telegram_id=telegram_id,
        username=new_member.username,
        coaching=coaching_key,
        batch=class_key,
        status="success"
    )

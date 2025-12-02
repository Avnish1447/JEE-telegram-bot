

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from utils.validators import user_is_eligible
from utils.database import get_user, update_user, increment_groups_join
from utils.constants import COACHINGS


async def batch_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles when a user selects a batch:
      - Stores selected batch in DB
      - Checks eligibility (max 2 groups, 24h rule)
      - Generates invite link (placeholder or real)
      - Sends final confirmation
    """

    query = update.callback_query
    await query.answer()
    telegram_id = query.from_user.id

    # Parse callback_data: "batch_<coaching>_<class>_<batch>"
    # Example: "batch_allen_11_A" or "batch_pw_dropper_B"
    callback_data = query.data
    if not callback_data.startswith("batch_"):
        await query.edit_message_text("Invalid batch selection. Please restart with /start.")
        return ConversationHandler.END

    # Split the callback data
    parts = callback_data.split("_")
    if len(parts) < 4:
        await query.edit_message_text("Invalid batch format. Please restart with /start.")
        return ConversationHandler.END
    
    # Extract: coaching, class, batch
    # parts = ["batch", "allen", "11", "A"]
    coaching_key = parts[1]
    student_class = parts[2]
    batch_letter = parts[3]
    
    # Construct full batch name for storage
    batch_full = f"{student_class}_{batch_letter}"  # e.g., "11_A", "dropper_B"

    # Fetch user from database
    user = get_user(telegram_id)
    if not user:
        await query.edit_message_text("User not found. Please restart with /start.")
        return ConversationHandler.END

    phone = user.get("phone")
    user_coaching = user.get("selected_coaching")
    user_class = user.get("student_class")
    
    if not user_coaching or not phone or not user_class:
        await query.edit_message_text(
            "Incomplete registration. Please restart with /start and complete phone verification."
        )
        return ConversationHandler.END

    # Eligibility check
    eligible, reason = user_is_eligible(phone)
    if not eligible:
        await query.edit_message_text(f"❌ You cannot join right now.\nReason: {reason}")
        return ConversationHandler.END

    # Save selected batch in DB
    update_user(telegram_id, {"selected_batch": batch_full})

    # Fetch coaching config
    coaching = COACHINGS.get(coaching_key)
    if not coaching:
        await query.edit_message_text("Invalid coaching configuration. Please contact admin.")
        return ConversationHandler.END

    group_id = coaching.get("group_id")

    # Determine invite URL
    if group_id is None or str(group_id).startswith("-100123456789"):
        # Placeholder/testing environment
        invite_url = "https://t.me/+PLACEHOLDER_INVITE_LINK"
    else:
        # Production: create real invite link
        try:
            invite_link = await context.bot.create_chat_invite_link(
                chat_id=group_id,
                member_limit=1
            )
            invite_url = invite_link.invite_link

            # Update user's groups_join and last_join_time
            increment_groups_join(telegram_id)

        except Exception as e:
            await query.edit_message_text(
                f"⚠️ Failed to generate invite link.\nError: {e}\n\n"
                "Ensure the bot is admin in the group and group_id is configured correctly."
            )
            return ConversationHandler.END

    # Format class and batch for display
    class_display = {
        "11": "Class 11",
        "12": "Class 12",
        "dropper": "Dropper"
    }.get(student_class, student_class)
    
    batch_display = f"{class_display} - Batch {batch_letter}"

    # Send final confirmation
    await query.edit_message_text(
        f"🎉 **You're eligible!**\n\n"
        f"📚 Coaching: *{coaching['name']}*\n"
        f"🎒 Class: *{class_display}*\n"
        f"🏷 Batch: *{batch_display}*\n"
        f"📞 Phone: `{phone}`\n\n"
        f"Here is your **one-time invite link**:\n{invite_url}",
        parse_mode="Markdown"
    )

    return ConversationHandler.END

from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.database import get_user, update_user, increment_groups_join
from utils.validators import user_is_eligible
from utils.constants import COACHINGS


async def class_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles when a user selects their class (11, 12, or Dropper).
    Stores the selection, checks eligibility, and generates invite link immediately.
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
    
    # Get user's coaching and phone
    selected_coaching = user.get("selected_coaching")
    phone = user.get("phone")
    
    if not selected_coaching or not phone:
        await query.edit_message_text(
            "Incomplete registration. Please restart with /start and complete phone verification."
        )
        return
    
    # Store student class in database
    update_user(telegram_id, {"student_class": student_class})
    
    # Check eligibility (max 2 groups, 24h cooldown)
    eligible, reason = user_is_eligible(phone)
    if not eligible:
        await query.edit_message_text(f"❌ You cannot join right now.\nReason: {reason}")
        return
    
    # Get coaching configuration
    coaching = COACHINGS.get(selected_coaching)
    if not coaching:
        await query.edit_message_text("Invalid coaching configuration. Please contact admin.")
        return
    
    # Get group_id for the selected class
    class_data = coaching.get("classes", {}).get(student_class)
    if not class_data:
        await query.edit_message_text(f"No group found for {student_class}. Please contact admin.")
        return
    
    group_id = class_data.get("group_id")
    
    # Determine invite URL
    # Check if this is a placeholder group_id (all placeholders start with -100123456789)
    is_placeholder = group_id is None or (group_id < 0 and str(group_id).startswith("-100123456789"))
    
    if is_placeholder:
        # Placeholder/testing environment - don't try to create real invite link
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
            return
    
    # Format class for display
    class_display = {
        "11": "Class 11",
        "12": "Class 12",
        "dropper": "Dropper"
    }.get(student_class, student_class)
    
    # Send final confirmation
    await query.edit_message_text(
        f"🎉 **You're eligible!**\n\n"
        f"📚 Coaching: *{coaching['name']}*\n"
        f"🎒 Class: *{class_display}*\n"
        f"📞 Phone: `{phone}`\n\n"
        f"Here is your **one-time invite link**:\n{invite_url}",
        parse_mode="Markdown"
    )

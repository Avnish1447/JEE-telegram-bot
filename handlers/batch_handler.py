from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from utils.validators import user_is_eligible
from utils.database import save_user_join, get_user
from utils.keyboards import build_batch_keyboard
from utils.constants import COACHINGS



async def batch_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Called when the user selects a batch button.
    Handles:
    - Storing selected batch
    - Eligibility check
    - Creating invite link
    - Returning final message
    """

    query = update.callback_query
    await query.answer()

    telegram_id = query.from_user.id

    # Parse callback_data: format is "batch_{coaching}_{batch}"
    # Example: "batch_pw_batch_1"
    callback_data = query.data
    parts = callback_data.split("_")
    
    # Extract coaching and batch from callback_data
    # Format: batch_<coaching>_batch_<number>
    if len(parts) >= 4 and parts[0] == "batch":
        coaching_key = parts[1]  # e.g., "pw"
        batch = "_".join(parts[2:])  # e.g., "batch_1"
    else:
        await query.edit_message_text(
            "Invalid batch selection. Please restart with /start."
        )
        return ConversationHandler.END

    # Get user from database
    user = get_user(telegram_id)
    
    if not user:
        await query.edit_message_text(
            "User not found. Please restart with /start."
        )
        return ConversationHandler.END

    phone = user.get("phone")
    stored_coaching = user.get("selected_coaching")

    # Verify coaching matches
    if stored_coaching != coaching_key:
        await query.edit_message_text(
            f"Coaching mismatch. Please restart with /start.\n"
            f"Expected: {stored_coaching}, Got: {coaching_key}"
        )
        return ConversationHandler.END

    # Safety check
    if not phone:
        await query.edit_message_text(
            "Phone number not found. Please restart with /start."
        )
        return ConversationHandler.END

    # Get coaching config
    coaching = COACHINGS.get(coaching_key)
    if not coaching:
        await query.edit_message_text(
            "Invalid coaching. Please restart with /start."
        )
        return ConversationHandler.END
        
    group_id = coaching.get("group_id")

    # --- Eligibility Check ---
    eligible, reason = user_is_eligible(phone)

    if not eligible:
        await query.edit_message_text(
            f"❌ You cannot join right now.\nReason: {reason}"
        )
        return ConversationHandler.END

    # --- Create Invite Link ---
    # Check if group_id is a placeholder (negative numbers starting with -100123456789x)
    is_placeholder = str(group_id).startswith("-100123456789")
    
    if is_placeholder:
        # For testing: show success message without creating real invite link
        invite_url = "https://t.me/+PLACEHOLDER_INVITE_LINK"
        
        # Save to DB
        save_user_join(telegram_id, group_id)
        
        await query.edit_message_text(
            f"🎉 **You're eligible!**\n\n"
            f"📚 Coaching: *{coaching['name']}*\n"
            f"🏷 Batch: *{batch}*\n"
            f"📞 Phone: `{phone}`\n\n"
            f"✅ **Registration successful!**\n\n"
            f"⚠️ *Note: This is a test environment.*\n"
            f"Configure real group IDs in `constants.py` to generate actual invite links.",
            parse_mode="Markdown"
        )
    else:
        # Production: create real invite link
        try:
            invite_link = await context.bot.create_chat_invite_link(
                chat_id=group_id,
                member_limit=1
            )
            invite_url = invite_link.invite_link
            
            # Save to DB
            save_user_join(telegram_id, group_id)
            
            await query.edit_message_text(
                f"🎉 **You're eligible!**\n\n"
                f"📚 Coaching: *{coaching['name']}*\n"
                f"🏷 Batch: *{batch}*\n"
                f"📞 Phone: `{phone}`\n\n"
                f"Here is your **one-time invite link**:\n{invite_url}",
                parse_mode="Markdown"
            )
        except Exception as e:
            await query.edit_message_text(
                f"⚠️ Failed to generate invite link.\n"
                f"Error: {str(e)}\n\n"
                f"Please make sure the bot is admin in the group and group_id is configured correctly."
            )
            return ConversationHandler.END

    return ConversationHandler.END

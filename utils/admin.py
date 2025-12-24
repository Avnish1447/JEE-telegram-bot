"""
Admin utilities for telegram-access-bot
Handles admin authentication and permissions
"""

from config import ADMIN_USER_IDS


def is_admin(user_id: int) -> bool:
    """
    Check if a user is an admin.
    
    Args:
        user_id: Telegram user ID to check
        
    Returns:
        bool: True if user is admin, False otherwise
    """
    return user_id in ADMIN_USER_IDS


async def require_admin(update, context):
    """
    Check if the user executing a command is an admin.
    Send error message if not.
    
    Args:
        update: Telegram update object
        context: Telegram context object
        
    Returns:
        bool: True if user is admin, False otherwise
    """
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text(
            "🚫 Access Denied\n\n"
            "This command is only available to administrators."
        )
        return False
    
    return True

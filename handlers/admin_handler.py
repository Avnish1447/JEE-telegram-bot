"""
Admin Handler for Mentor Tracking Bot
Handles admin commands for managing mentors and viewing statistics

STRICT MODE: Only responds to admin in private chat
"""

from telegram import Update
from telegram.ext import ContextTypes
import database as db
import config


def check_admin_private_chat(update: Update) -> bool:
    """
    Check if the command is from admin in private chat.
    
    Returns True only if:
    1. User is admin
    2. Chat is private (not group)
    
    Args:
        update: Telegram update object
    
    Returns:
        bool: True if admin in private chat, False otherwise
    """
    user_id = update.effective_user.id
    chat_type = update.effective_chat.type
    
    # Must be admin
    if not config.is_admin(user_id):
        return False
    
    # Must be private chat
    if chat_type != 'private':
        return False
    
    return True


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the /start command.
    
    STRICT: Only responds to admin in private chat.
    
    Args:
        update: Telegram update object
        context: Bot context
    """
    # STRICT CHECK: Only admin in private chat
    if not check_admin_private_chat(update):
        return  # Silently ignore
    
    user_name = update.effective_user.first_name or "there"
    
    # Admin welcome message
    response = (
        f"👋 Welcome, {user_name}!\n\n"
        "🤖 Mentor Tracking Bot - Admin Panel\n\n"
        "You have admin access to this bot. Here's what you can do:\n\n"
        "📋 Quick Start:\n"
        "1. Add this bot to your group\n"
        "2. Make the bot an admin\n"
        "3. Use /add_mentor to register mentors\n"
        "4. Test with /send_poll\n\n"
        "🛠️ Admin Commands:\n"
        "/add_mentor - Register a new mentor\n"
        "/remove_mentor - Remove a mentor\n"
        "/mentor_stats - View mentor statistics\n"
        "/today_votes - Today's rankings\n"
        "/total_votes - Lifetime rankings\n"
        "/send_poll - Send a test poll\n"
        "/help - Show help message\n\n"
        "⏰ Automated Polls:\n"
        f"Polls are sent automatically at: {', '.join(config.POLL_TIMES)}\n\n"
        "Need help? Use /help anytime!"
    )
    
    await update.message.reply_text(response)


async def add_mentor_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Admin command to add a mentor to the system.
    
    STRICT: Only responds to admin in private chat.
    
    Usage: /add_mentor <user_id> <username> <full_name>
    Example: /add_mentor 123456789 john_doe "John Doe"
    
    Args:
        update: Telegram update object
        context: Bot context with args
    """
    # STRICT CHECK: Only admin in private chat
    if not check_admin_private_chat(update):
        return  # Silently ignore
    
    # Check if command has correct number of arguments
    if len(context.args) < 3:
        await update.message.reply_text(
            "❌ Invalid usage!\n\n"
            "Usage: /add_mentor <user_id> <username> <full_name>\n"
            "Example: /add_mentor 123456789 john_doe \"John Doe\""
        )
        return
    
    try:
        # Parse arguments
        mentor_id = int(context.args[0])
        username = context.args[1]
        full_name = ' '.join(context.args[2:])  # Join remaining args as full name
        group_id = 0  # Placeholder, will be updated when mentor joins group
        
        # Add mentor to database
        success = db.add_mentor(mentor_id, username, full_name, group_id)
        
        if success:
            await update.message.reply_text(
                f"✅ Mentor added successfully!\n\n"
                f"👤 Name: {full_name}\n"
                f"🆔 ID: {mentor_id}\n"
                f"📱 Username: @{username}\n\n"
                "The mentor will be tracked in all groups where they are active."
            )
        else:
            await update.message.reply_text("❌ Failed to add mentor. Please try again.")
            
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID. Must be a number.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def remove_mentor_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Admin command to remove a mentor from the system.
    
    STRICT: Only responds to admin in private chat.
    
    Usage: /remove_mentor <mentor_id>
    Example: /remove_mentor 123456789
    
    Args:
        update: Telegram update object
        context: Bot context with args
    """
    # STRICT CHECK: Only admin in private chat
    if not check_admin_private_chat(update):
        return  # Silently ignore
    
    # Check if command has correct number of arguments
    if len(context.args) < 1:
        await update.message.reply_text(
            "❌ Invalid usage!\n\n"
            "Usage: /remove_mentor <mentor_id>\n"
            "Example: /remove_mentor 123456789"
        )
        return
    
    try:
        # Parse arguments
        mentor_id = int(context.args[0])
        
        # Check if mentor exists
        if not db.is_mentor(mentor_id):
            await update.message.reply_text(f"❌ Mentor with ID {mentor_id} not found.")
            return
        
        # Remove mentor from database
        success = db.remove_mentor(mentor_id)
        
        if success:
            await update.message.reply_text(
                f"✅ Mentor removed successfully!\n\n"
                f"🆔 Mentor ID: {mentor_id}\n\n"
                "Note: Their message history and votes are still in the database."
            )
        else:
            await update.message.reply_text("❌ Failed to remove mentor. Please try again.")
            
    except ValueError:
        await update.message.reply_text("❌ Invalid mentor ID. Must be a number.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def mentor_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Admin command to view statistics for a specific mentor.
    
    STRICT: Only responds to admin in private chat.
    
    Usage: /mentor_stats <mentor_id>
    Example: /mentor_stats 123456789
    
    Shows:
    - Total messages today
    - Message type breakdown
    - Votes today
    - Lifetime votes
    
    Args:
        update: Telegram update object
        context: Bot context with args
    """
    # STRICT CHECK: Only admin in private chat
    if not check_admin_private_chat(update):
        return  # Silently ignore
    
    # Check if mentor_id is provided
    if len(context.args) < 1:
        await update.message.reply_text(
            "❌ Invalid usage!\n\n"
            "Usage: /mentor_stats <mentor_id>\n"
            "Example: /mentor_stats 123456789"
        )
        return
    
    try:
        mentor_id = int(context.args[0])
        
        # Check if mentor exists
        if not db.is_mentor(mentor_id):
            await update.message.reply_text(f"❌ Mentor with ID {mentor_id} not found.")
            return
        
        # Get mentor stats
        stats = db.get_mentor_stats_today(mentor_id)
        
        # Format message type breakdown
        msg_types = stats['message_types']
        type_breakdown = "\n".join([f"  • {msg_type}: {count}" for msg_type, count in msg_types.items()])
        if not type_breakdown:
            type_breakdown = "  No messages today"
        
        # Create response message
        response = (
            f"📊 **Mentor Statistics**\n"
            f"🆔 Mentor ID: {mentor_id}\n\n"
            f"📅 **Today's Activity:**\n"
            f"📨 Total Messages: {stats['total_messages']}\n"
            f"🗳️ Votes Received: {stats['votes_today']}\n\n"
            f"📝 **Message Breakdown:**\n{type_breakdown}\n\n"
            f"⭐ **Lifetime Stats:**\n"
            f"🏆 Total Votes: {stats['lifetime_votes']}"
        )
        
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except ValueError:
        await update.message.reply_text("❌ Invalid mentor ID. Must be a number.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def today_votes_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Admin command to view today's vote rankings.
    
    STRICT: Only responds to admin in private chat.
    
    Usage: /today_votes
    
    Shows ranking of all mentors by votes received today.
    
    Args:
        update: Telegram update object
        context: Bot context
    """
    # STRICT CHECK: Only admin in private chat
    if not check_admin_private_chat(update):
        return  # Silently ignore
    
    try:
        # Get today's vote rankings
        rankings = db.get_today_votes_ranking()
        
        if not rankings:
            await update.message.reply_text("📊 No votes recorded today yet.")
            return
        
        # Format rankings
        response = "📊 **Today's Vote Rankings**\n\n"
        
        for idx, (mentor_id, full_name, vote_count) in enumerate(rankings, 1):
            # Add medal emojis for top 3
            medal = ""
            if idx == 1:
                medal = "🥇 "
            elif idx == 2:
                medal = "🥈 "
            elif idx == 3:
                medal = "🥉 "
            
            response += f"{medal}{idx}. {full_name} - {vote_count} votes\n"
        
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def total_votes_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Admin command to view lifetime vote rankings.
    
    STRICT: Only responds to admin in private chat.
    
    Usage: /total_votes
    
    Shows ranking of all mentors by total votes received (all time).
    
    Args:
        update: Telegram update object
        context: Bot context
    """
    # STRICT CHECK: Only admin in private chat
    if not check_admin_private_chat(update):
        return  # Silently ignore
    
    try:
        # Get lifetime vote rankings
        rankings = db.get_total_votes_ranking()
        
        if not rankings:
            await update.message.reply_text("📊 No votes recorded yet.")
            return
        
        # Format rankings
        response = "🏆 **Lifetime Vote Rankings**\n\n"
        
        for idx, (mentor_id, full_name, vote_count) in enumerate(rankings, 1):
            # Add medal emojis for top 3
            medal = ""
            if idx == 1:
                medal = "🥇 "
            elif idx == 2:
                medal = "🥈 "
            elif idx == 3:
                medal = "🥉 "
            
            response += f"{medal}{idx}. {full_name} - {vote_count} votes\n"
        
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Shows available admin commands.
    
    STRICT: Only responds to admin in private chat.
    
    Usage: /help
    
    Args:
        update: Telegram update object
        context: Bot context
    """
    # STRICT CHECK: Only admin in private chat
    if not check_admin_private_chat(update):
        return  # Silently ignore
    
    response = (
        "🤖 **Mentor Tracking Bot - Admin Commands**\n\n"
        "**Mentor Management:**\n"
        "/add_mentor <id> <username> <name> - Add a mentor\n"
        "/remove_mentor <id> - Remove a mentor\n\n"
        "**Statistics:**\n"
        "/mentor_stats <mentor_id> - View mentor stats\n"
        "/today_votes - Today's vote rankings\n"
        "/total_votes - Lifetime vote rankings\n\n"
        "/help - Show this message"
    )
    
    await update.message.reply_text(response, parse_mode='Markdown')

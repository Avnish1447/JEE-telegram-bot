"""
Admin command handlers for telegram-access-bot
Provides statistics and tracking commands for administrators
"""

from telegram import Update
from telegram.ext import ContextTypes
from utils.admin import require_admin
from utils.database import (
    get_total_user_count,
    get_users_registered_today,
    get_users_registered_this_week,
    get_daily_registration_stats
)
from datetime import datetime


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Show quick user statistics overview.
    Command: /stats
    Admin only.
    """
    # Check if user is admin
    if not await require_admin(update, context):
        return
    
    # Get statistics
    total_users = get_total_user_count()
    today_users = get_users_registered_today()
    week_users = get_users_registered_this_week()
    
    # Format message
    message = (
        "📊 **User Statistics**\n\n"
        f"👥 Total Users: **{total_users}**\n"
        f"📅 Registered Today: **{today_users}**\n"
        f"🆕 New This Week: **{week_users}**\n\n"
        f"_Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_"
    )
    
    await update.message.reply_text(message, parse_mode="Markdown")


async def daily_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Show detailed daily registration statistics.
    Command: /daily_stats [days]
    Admin only.
    
    Args:
        days: Optional number of days to show (default 7, max 30)
    """
    # Check if user is admin
    if not await require_admin(update, context):
        return
    
    # Parse days argument
    days = 7  # default
    if context.args and len(context.args) > 0:
        try:
            days = int(context.args[0])
            if days < 1:
                days = 7
            elif days > 30:
                days = 30
        except ValueError:
            await update.message.reply_text(
                "❌ Invalid number of days. Using default (7 days)."
            )
            days = 7
    
    # Get daily stats
    stats = get_daily_registration_stats(days)
    
    if not stats:
        await update.message.reply_text("No registration data available.")
        return
    
    # Find max count for scaling the bar chart
    max_count = max(count for _, count in stats) if stats else 1
    if max_count == 0:
        max_count = 1
    
    # Build message with bar chart
    message = f"📈 **Daily Registration Stats** (Last {days} Days)\n\n"
    
    for date, count in stats:
        # Create bar chart (max 12 blocks)
        bar_length = int((count / max_count) * 12) if max_count > 0 else 0
        bar = "█" * bar_length
        
        # Format date (show as Dec 24, Dec 23, etc.)
        date_obj = datetime.fromisoformat(date)
        formatted_date = date_obj.strftime("%b %d")
        
        message += f"`{formatted_date}`: {bar} **{count}** user{'s' if count != 1 else ''}\n"
    
    total = sum(count for _, count in stats)
    avg = total / days if days > 0 else 0
    
    message += f"\n📊 **Summary**\n"
    message += f"Total: **{total}** registrations\n"
    message += f"Average: **{avg:.1f}** per day"
    
    await update.message.reply_text(message, parse_mode="Markdown")

from telegram.error import BadRequest, Forbidden
import asyncio

async def kick_user(chat_id, user_id, context):
    try:
        await context.bot.ban_chat_member(chat_id, user_id)
        await asyncio.sleep(0.5)
        await context.bot.unban_chat_member(chat_id, user_id)  # ensures they can join later again
    except Forbidden:
        pass
    except BadRequest:
        pass
    except Exception:
        pass
async def safe_notify(user_id: int, text: str, context):
    try:
        await context.bot.send_message(chat_id=user_id, text=text)
    except Forbidden:
        # User blocked bot
        pass
    except BadRequest:
        # Invalid user / cannot send message
        pass
    except Exception:
        # Never crash
        pass

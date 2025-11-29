# # # from telegram import Update
# # # from telegram.ext import ContextTypes
# # # from utils.storage import get_user
# # # from utils.security import kick_user
# # # from utils.constants import COACHINGS
# # # from utils.storage import get_user, log_join_attempt
# # # from utils.constants import INVITE_MAP as INVITE_MAPPINGS
# # # from utils.logging_utils import log_join_attempt


# # # async def handle_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
# # #     chat = update.effective_chat
# # #     message = update.message

# # #     if not message or not message.new_chat_members:
# # #         return
    
# # #     invite_link_used = message.invite_link
# # #     new_member = message.new_chat_members[0]
# # #     telegram_id = new_member.id


# # #     # 1. Verify invite link existence
# # #     if invite_link_used is None:
# # #         await kick_user(chat.id, telegram_id, context)
# # #         return
    
# # #     #the raw link string
# # #     invite_key = invite_link_used.invite_link


# # #     #2. Identify coaching + batch from the invite link
# # #     coaching_key, batch_key= extract_mapping(invite_key)
# # #     if coaching_key is None:
# # #         await kick_user(chat.id, telegram_id, context)
# # #         return
    
# # #      #3. Fetch user record
# # #     user = get_user(telegram_id)
    
# # #     #Log attempt
# # #     log_join_attempt(
# # #         telegram_id=telegram_id,
# # #         username=new_member.username,
# # #         coaching=coaching_key,
# # #         batch_key=batch_key,
# # #         status="attempt"
# # #     )

# # #     #4. Validate User
# # #     if not user:
# # #         await kick_user(chat.id, telegram_id, context)
# # #         await context.bot.send_message(chat_id=telegram_id, text=
# # #             "You are not registered in the system.\n"
# # #             "Please complete verification in the bot before joining."
# # #         )
# # #         return
# # #     if "phone" not in user:
# # #         await kick_user(chat.id, telegram_id, context)
# # #         await context.bot.send_message(chat_id=telegram_id, text=
# # #             "Phone number verification missing.\n"
# # #             "Use /start in bot to register again."
# # #         )
# # #         return

# # #     #Checking coaching match    
# # #     if user.get("selected_coaching") != coaching_key:
# # #         await kick_user(chat.id, telegram_id, context)
# # #         await context.bot.send_message(chat_id=telegram_id, text=
# # #             "You tried joining a coaching you're not approved for.\n"
# # #             "Your assigned coaching: "
# # #             f"{user.get('selected_coaching')}"
# # #         )
# # #         return
    
# # #     #Check Bans
# # #     if user.get("banned", False):
# # #         await kick_user(chat.id, telegram_id, context)
# # #         await context.bot.send_message(chat_id=telegram_id, text=
# # #             "You are banned from this coaching group."
# # #         )
# # #         return
    
# # #     #5. If passed all checks: welcome message
# # #     await message.reply_text(
# # #         f"✨ Welcome {new_member.first_name}!\n"
# # #         f"Coaching: {COACHINGS[coaching_key]['name']}\n"
# # #         f"Batch: {batch_key}\n"
# # #         "You're successfully verified. Enjoy!"
# # #     )

# # #     # Log success
# # #     log_join_attempt(
# # #         telegram_id=telegram_id,
# # #         username=new_member.username,
# # #         coaching=coaching_key,
# # #         batch=batch_key,
# # #         status="success"
# # #     )

# # # def extract_mapping(invite_link: str):
# # #     return INVITE_MAPPINGS.get(invite_link, (None, None))


# # from telegram import Update
# # from telegram.ext import ContextTypes

# # from utils.storage import get_user
# # from utils.security import kick_user
# # from utils.constants import COACHINGS, INVITE_MAPPINGS
# # from utils.logging_utils import log_join_attempt


# # async def handle_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     chat = update.effective_chat
# #     message = update.message

# #     if not message or not message.new_chat_members:
# #         return

# #     invite_link_used = message.invite_link
# #     new_member = message.new_chat_members[0]
# #     telegram_id = new_member.id

# #     # 1. Verify that the join happened through an invite link
# #     if invite_link_used is None:
# #         await kick_user(chat.id, telegram_id, context)
# #         return

# #     # The raw link string
# #     invite_key = invite_link_used.invite_link

# #     # 2. Map link → coaching + batch
# #     coaching_key, batch_key = extract_mapping(invite_key)
# #     if coaching_key is None:
# #         await kick_user(chat.id, telegram_id, context)
# #         return

# #     # 3. Load user
# #     user = get_user(telegram_id)

# #     # Log attempt
# #     log_join_attempt(
# #         telegram_id=telegram_id,
# #         username=new_member.username,
# #         coaching_key=coaching_key,
# #         batch_key=batch_key,
# #         status="attempt"
# #     )

# #     # 4. Validate user registration
# #     if not user:
# #         await kick_user(chat.id, telegram_id, context)
# #         await context.bot.send_message(
# #             chat_id=telegram_id,
# #             text="You are not registered.\nUse the bot to verify before joining."
# #         )
# #         return

# #     if not user.get("phone"):
# #         await kick_user(chat.id, telegram_id, context)
# #         await context.bot.send_message(
# #             chat_id=telegram_id,
# #             text="Phone number missing.\nUse /start in bot to register."
# #         )
# #         return

# #     # Coaching mismatch
# #     if user.get("selected_coaching") != coaching_key:
# #         await kick_user(chat.id, telegram_id, context)
# #         await context.bot.send_message(
# #             chat_id=telegram_id,
# #             text=f"You are not approved for this coaching.\n"
# #                  f"Assigned: {user.get('selected_coaching')}"
# #         )
# #         return

# #     # Banned users
# #     if user.get("banned", False):
# #         await kick_user(chat.id, telegram_id, context)
# #         await context.bot.send_message(
# #             chat_id=telegram_id,
# #             text="You are banned from this coaching."
# #         )
# #         return

# #     # 5. Success message
# #     await message.reply_text(
# #         f"✨ Welcome {new_member.first_name}!\n"
# #         f"Coaching: {COACHINGS[coaching_key]['name']}\n"
# #         f"Batch: {batch_key}\n"
# #         "You're successfully verified. Enjoy!"
# #     )

# #     # Log success
# #     log_join_attempt(
# #         telegram_id=telegram_id,
# #         username=new_member.username,
# #         coaching_key=coaching_key,
# #         batch_key=batch_key,
# #         status="success"
# #     )


# # def extract_mapping(invite_link: str):
# #     return INVITE_MAPPINGS.get(invite_link, (None, None))
# from telegram import Update
# from telegram.ext import ContextTypes

# from utils.storage import get_user
# from utils.security import kick_user, safe_notify
# from utils.constants import COACHINGS, INVITE_MAP
# from utils.logging_utils import log_join_attempt


# async def handle_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """
#     Triggered whenever someone joins a group.
#     Validates the user based on the invite link & stored bot data.
#     """

#     message = update.message
#     chat = update.effective_chat

#     # Safety: no member added?
#     if not message or not message.new_chat_members:
#         return

#     new_member = message.new_chat_members[0]
#     telegram_id = new_member.id
#     invite_link_used = message.invite_link

#     # 1. Ensure an invite link exists
#     if invite_link_used is None:
#         await kick_user(chat.id, telegram_id, context)
#         return

#     invite_key = invite_link_used.invite_link

#     # 2. Map invite → (coaching, batch)
#     coaching_key, batch_key = extract_mapping(invite_key)
#     if coaching_key is None:
#         await kick_user(chat.id, telegram_id, context)
#         return

#     # 3. Load user record
#     user = get_user(telegram_id)

#     # Log attempt
#     log_join_attempt(
#         telegram_id=telegram_id,
#         username=new_member.username,
#         coaching=coaching_key,
#         batch=batch_key,
#         status="attempt"
#     )

#     # 4. Validate user
#     if not user:
#         await kick_user(chat.id, telegram_id, context)
#         await safe_notify(
#             telegram_id,
#             "You are not registered in the system.\n"
#             "Please verify through the bot before joining a group.",
#             context
#         )
#         return

#     if not user.get("phone"):
#         await kick_user(chat.id, telegram_id, context)
#         await safe_notify(
#             telegram_id,
#             "Phone number verification missing.\n"
#             "Use /start in the bot to complete the setup.",
#             context
#         )
#         return

#     # Coaching mismatch
#     if user.get("selected_coaching") != coaching_key:
#         await kick_user(chat.id, telegram_id, context)
#         await safe_notify(
#             telegram_id,
#             "You tried joining a coaching you're not approved for.\n"
#             f"Your assigned coaching: {user.get('selected_coaching')}",
#             context
#         )
#         return

#     # User banned
#     if user.get("banned", False):
#         await kick_user(chat.id, telegram_id, context)
#         await safe_notify(
#             telegram_id,
#             "You are banned from this coaching group.",
#             context
#         )
#         return

#     # 5. Passed all checks → allow
#     await message.reply_text(
#         f"✨ Welcome {new_member.first_name}!\n"
#         f"Coaching: {COACHINGS[coaching_key]['name']}\n"
#         f"Batch: {batch_key}\n"
#         "You have been successfully verified."
#     )

#     # Log success
#     log_join_attempt(
#         telegram_id=telegram_id,
#         username=new_member.username,
#         coaching=coaching_key,
#         batch=batch_key,
#         status="success"
#     )


# def extract_mapping(invite_link: str):

#     return INVITE_MAP.get(invite_link, (None, None))
from telegram import Update
from telegram.ext import ContextTypes

from utils.storage import get_user
from utils.security import kick_user, safe_notify
from utils.constants import COACHINGS, INVITE_MAP
from utils.logging_utils import log_join_attempt


async def handle_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Triggered whenever someone joins a group.
    Validates the user based on the invite link & stored bot data.
    """

    message = update.message
    chat = update.effective_chat

    # Safety: no member added?
    if not message or not message.new_chat_members:
        return

    new_member = message.new_chat_members[0]
    telegram_id = new_member.id
    invite_link_used = message.invite_link

    # 1. Ensure an invite link exists
    if invite_link_used is None:
        await kick_user(chat.id, telegram_id, context)
        return

    invite_key = invite_link_used.invite_link

    # 2. Map invite → (coaching, batch)
    coaching_key, batch_key = extract_mapping(invite_key)
    if coaching_key is None:
        await kick_user(chat.id, telegram_id, context)
        return

    # 3. Load user record
    user = get_user(telegram_id)

    # Log attempt
    log_join_attempt(
        telegram_id=telegram_id,
        username=new_member.username,
        coaching=coaching_key,
        batch=batch_key,
        status="attempt"
    )

    # 4. Validate user
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
            "Phone number verification missing.\n"
            "Use /start in the bot to complete the setup.",
            context
        )
        return

    # Coaching mismatch
    if user.get("selected_coaching") != coaching_key:
        await kick_user(chat.id, telegram_id, context)
        await safe_notify(
            telegram_id,
            "You tried joining a coaching you're not approved for.\n"
            f"Your assigned coaching: {user.get('selected_coaching')}",
            context
        )
        return

    # User banned
    if user.get("banned", False):
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

    # Log success
    log_join_attempt(
        telegram_id=telegram_id,
        username=new_member.username,
        coaching=coaching_key,
        batch=batch_key,
        status="success"
    )


def extract_mapping(invite_link: str):

    return INVITE_MAP.get(invite_link, (None, None))

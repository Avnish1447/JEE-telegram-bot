# import json
# from pathlib import Path
# from copy import deepcopy

# EMPTY_USER_TEMPLATE = {
#     "phone": "",
#     "telegram_id": 0,
#     "groups_join": 0,
#     "last_join_time": None,
#     "joined_group_list": [],
#     "last_invite_link": {"link": "", "chat_id": 0}
# }

# USER_FLIES_PATH = Path("data/users.json")
# # Open users.json
# # Read it into a Python dictionary
# # Return the dictionary
# # If file is empty, return {}
# def load_users():
#     users_file = USER_FLIES_PATH
#     if not users_file.exists():   # optional: handle missing file
#         return {}
#     try:
#         with open(users_file, "r") as file:
#             data = json.load(file)
#         return data
#     except json.JSONDecodeError:
#         return {}


# def get_user(telegram_id):
#     users = load_users()
#     user_id = str(telegram_id)
#     return users.get(user_id)

# def save_users(users_dict):
#     user_file = USER_FLIES_PATH
#     user_file.parent.mkdir(parents=True, exists_ok=True) #This wil check if data folder exists
#     with open(user_file, "w", encoding="utf-8") as file:
#         json.dump(users_dict, file, indent=4)



<<<<<<< HEAD
# def update_user(telegram_id, new_data):
#     users = load_users()
#     user_id = str(telegram_id)
#     if user_id not in users:
#         users[user_id] = deepcopy(EMPTY_USER_TEMPLATE)
#     users[user_id].update(new_data)
#     save_users(users)
    
#-----------------------------------------------------------------------------
# utils/storage.py
from typing import Optional, Dict, Any
from utils import database

# compatibility layer: exposes the same functions your handlers expected,
# but uses the new SQLite implementation underneath.

def get_user(telegram_id: int) -> Optional[Dict[str, Any]]:
    """Return user dict or None."""
    return database.get_user(telegram_id)


def get_user_by_phone(phone: str) -> Optional[Dict[str, Any]]:
    """Return user dict found by phone or None."""
    return database.get_user_by_phone(phone)


def update_user(telegram_id: int, fields: Dict[str, Any]) -> None:
    """Update or create user row with provided fields."""
    return database.update_user(telegram_id, fields)


def save_user_join(telegram_id: int, chat_id: int) -> None:
    """Legacy name used by some handlers — update counters when user joins."""
    # implement via database functions: increment groups_join and log join event
    # database.update_user will insert or update; then we can call database.log_join_event
    user = database.get_user(telegram_id)
    # increment groups_join, set last_join_time, append joined_group (if you store lists elsewhere)
    if user is None:
        # create minimal user row first
        database.update_user(telegram_id, {"phone": None})

    # increase groups_join and set last_join_time
    database.update_user(telegram_id, {
        "groups_join": (user.get("groups_join", 0) + 1) if user else 1,
        "last_join_time": database._now_iso()
    })

    # log join event table
    database.log_join_event(telegram_id, coaching=None, batch=None, outcome="joined")


def log_join_attempt(telegram_id, username, coaching, batch, status):
    """Compatibility function used by handlers.logging_utils previously."""
    # Map to the database join_events table
    database.log_join_event(telegram_id=telegram_id, coaching=coaching, batch=batch, outcome=status)
=======
def update_user(telegram_id, new_data):
    users = load_users()
    user_id = str(telegram_id)
    if user_id not in users:
        users[user_id] = deepcopy(EMPTY_USER_TEMPLATE)
    users[user_id].update(new_data)
    save_users(users)
>>>>>>> 764c36f4e07b29252ec465778061be43957ea0d3

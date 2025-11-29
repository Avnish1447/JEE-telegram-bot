import json
from pathlib import Path
from datetime import datetime

DB_FILE = Path("data/users.json")


# ----------------------------
# Internal helpers
# ----------------------------
def _load_db():
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not DB_FILE.exists():
        return {}

    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def _save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ----------------------------
# Public functions
# ----------------------------
def get_user(telegram_id):
    data = _load_db()
    return data.get(str(telegram_id))


def get_user_by_phone(phone):
    """Get user by phone number."""
    data = _load_db()
    for user_id, user_data in data.items():
        if user_data.get("phone") == phone:
            return user_data
    return None


def update_user(telegram_id, fields: dict):
    """Create or update a user entry with the given fields."""
    data = _load_db()
    tid = str(telegram_id)

    if tid not in data:
        data[tid] = {
            "phone": "",
            "telegram_id": telegram_id,
            "groups_join": 0,
            "last_join_time": None,
            "joined_group_list": [],
            "last_invite_link": {"link": "", "chat_id": 0},
            "selected_coaching": None,
            "selected_batch": None,
        }

    data[tid].update(fields)
    _save_db(data)


def save_user_join(telegram_id, chat_id):
    """
    Called when a user successfully joins a Telegram group.
    Updates:
      - groups_join += 1
      - last_join_time = now
      - joined_group_list.append(chat_id)
    """
    data = _load_db()
    tid = str(telegram_id)

    if tid not in data:
        # should never happen normally
        data[tid] = {
            "phone": "",
            "telegram_id": telegram_id,
            "groups_join": 0,
            "last_join_time": None,
            "joined_group_list": [],
            "last_invite_link": {"link": "", "chat_id": 0},
            "selected_coaching": None,
            "selected_batch": None,
        }

    user = data[tid]

    # update fields
    user["groups_join"] = user.get("groups_join", 0) + 1
    user["last_join_time"] = datetime.utcnow().isoformat()

    jlist = user.get("joined_group_list", [])
    if chat_id not in jlist:
        jlist.append(chat_id)
    user["joined_group_list"] = jlist

    _save_db(data)

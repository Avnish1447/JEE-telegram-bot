import json
from pathlib import Path
from copy import deepcopy

EMPTY_USER_TEMPLATE = {
    "phone": "",
    "telegram_id": 0,
    "groups_join": 0,
    "last_join_time": None,
    "joined_group_list": [],
    "last_invite_link": {"link": "", "chat_id": 0}
}

USER_FLIES_PATH = Path("data/users.json")
# Open users.json
# Read it into a Python dictionary
# Return the dictionary
# If file is empty, return {}
def load_users():
    users_file = USER_FLIES_PATH
    if not users_file.exists():   # optional: handle missing file
        return {}
    try:
        with open(users_file, "r") as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError:
        return {}


def get_user(telegram_id):
    users = load_users()
    user_id = str(telegram_id)
    return users.get(user_id)

def save_users(users_dict):
    user_file = USER_FLIES_PATH
    user_file.parent.mkdir(parents=True, exists_ok=True) #This wil check if data folder exists
    with open(user_file, "w", encoding="utf-8") as file:
        json.dump(users_dict, file, indent=4)



def update_user(telegram_id, new_data):
    users = load_users()
    user_id = str(telegram_id)
    if user_id not in users:
        users[user_id] = deepcopy(EMPTY_USER_TEMPLATE)
    users[user_id].update(new_data)
    save_users(users)
    

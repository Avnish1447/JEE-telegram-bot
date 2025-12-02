# from datetime import datetime, timedelta

# def normalize_phone(phone: str) -> str | None:

#     s = phone.strip()

#     # remove leading +
#     if s.startswith("+"):
#         s = s[1:]

#     # remove leading 91 if length is >= 12
#     if s.startswith("91") and len(s) >= 12:
#         s = s[2:]

#     # final validation
#     if len(s) == 10 and s.isdigit() and s[0] in {"6", "7", "8", "9"}:
#         return s

#     return None


# def is_valid_phone_number(phone: str) -> bool:
#     """Simple wrapper."""
#     return normalize_phone(phone) is not None


# def user_is_eligible(phone: str) -> tuple[bool, str]:
#     """
#     Checks if a user can join a new group.
#     Rules:
#     - Max 2 groups total
#     - Must wait 24 hours between joining groups
    
#     Args:
#         phone: User's phone number
    
#     Returns:
#         (True, "ok") if eligible, (False, "reason") if not
#     """
#     from utils.database import get_user_by_phone
    
#     user = get_user_by_phone(phone)
#     if not user:
#         return False, "User not found in database."
    
#     if user.get("groups_join", 0) >= 2:
#         return False, "You have already joined 2 groups."

#     last = user.get("last_join_time")
#     if last:
#         try:
#             last_dt = datetime.fromisoformat(last)
#             if datetime.utcnow() - last_dt < timedelta(hours=24):
#                 return False, "You must wait 24 hours before joining another group."
#         except:
#             pass

#     return True, "ok"

#-----------------------------------------------------------------------------


# from datetime import datetime, timedelta
# from utils.database import get_user_by_phone_sql  # SQL version of get_user_by_phone
# from utils.database import get_user, get_user_by_phone, update_user, increment_groups_join

# def normalize_phone(phone: str) -> str | None:
#     """
#     Normalize Indian phone numbers to 10-digit string.
#     Accepts:
#         - "9876543210"
#         - "+919876543210"
#         - "919876543210"
#     Returns 10-digit string if valid, else None.
#     """
#     s = phone.strip()

#     if s.startswith("+"):
#         s = s[1:]

#     if s.startswith("91") and len(s) >= 12:
#         s = s[2:]

#     if len(s) == 10 and s.isdigit() and s[0] in {"6", "7", "8", "9"}:
#         return s

#     return None


# def is_valid_phone_number(phone: str) -> bool:
#     """Wrapper for normalize_phone."""
#     return normalize_phone(phone) is not None


# def user_is_eligible(phone: str) -> tuple[bool, str]:
#     """
#     Checks if a user can join a new group.
#     Rules:
#         1. Max 2 groups total
#         2. Must wait 24 hours between joins

#     Args:
#         phone: 10-digit string
    
#     Returns:
#         Tuple: (True, "ok") if eligible, (False, reason) otherwise
#     """
#     user = get_user_by_phone_sql(phone)
#     if not user:
#         return False, "User not found in database."

#     # Max groups check
#     if user.get("groups_join", 0) >= 2:
#         return False, "You have already joined 2 groups."

#     # Last join time check
#     last_join = user.get("last_join_time")
#     if last_join:
#         try:
#             last_dt = datetime.fromisoformat(last_join)
#             if datetime.utcnow() - last_dt < timedelta(hours=24):
#                 return False, "You must wait 24 hours before joining another group."
#         except Exception:
#             # ignore parsing errors, allow join
#             pass

#     return True, "ok"

#-----------------------------------------------------------------------------
from utils.database import get_user_by_phone
from datetime import datetime, timedelta

def normalize_phone(phone: str) -> str | None:
    s = phone.strip()
    if s.startswith("+"):
        s = s[1:]
    if s.startswith("91") and len(s) >= 12:
        s = s[2:]
    if len(s) == 10 and s.isdigit() and s[0] in {"6", "7", "8", "9"}:
        return s
    return None

def is_valid_phone_number(phone: str) -> bool:
    return normalize_phone(phone) is not None

def user_is_eligible(phone: str) -> tuple[bool, str]:
    """
    Checks if a user can join a new group.
    Rules:
    - Max 2 groups total
    - Must wait 24 hours between joining groups
    """
    user = get_user_by_phone(phone)
    
    # If user doesn't exist yet, they're eligible (first time user)
    if not user:
        return True, "ok"
    
    # Check if user has already joined 2 groups (handle None values and convert to int)
    groups_join_raw = user.get("groups_join")
    try:
        groups_join = int(groups_join_raw) if groups_join_raw is not None else 0
    except (ValueError, TypeError):
        groups_join = 0
    
    if groups_join >= 2:
        return False, "You have already joined 2 groups."

    # Check 24-hour cooldown
    last = user.get("last_join_time")
    if last:
        try:
            last_dt = datetime.fromisoformat(last)
            if datetime.utcnow() - last_dt < timedelta(hours=24):
                return False, "You must wait 24 hours before joining another group."
        except:
            pass

    return True, "ok"


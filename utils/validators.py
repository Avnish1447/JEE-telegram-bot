from datetime import datetime, timedelta

def normalize_phone(phone: str) -> str | None:

    s = phone.strip()

    # remove leading +
    if s.startswith("+"):
        s = s[1:]

    # remove leading 91 if length is >= 12
    if s.startswith("91") and len(s) >= 12:
        s = s[2:]

    # final validation
    if len(s) == 10 and s.isdigit() and s[0] in {"6", "7", "8", "9"}:
        return s

    return None


def is_valid_phone_number(phone: str) -> bool:
    """Simple wrapper."""
    return normalize_phone(phone) is not None


def user_is_eligible(phone: str) -> tuple[bool, str]:
    """
    Checks if a user can join a new group.
    Rules:
    - Max 2 groups total
    - Must wait 24 hours between joining groups
    
    Args:
        phone: User's phone number
    
    Returns:
        (True, "ok") if eligible, (False, "reason") if not
    """
    from utils.database import get_user_by_phone
    
    user = get_user_by_phone(phone)
    if not user:
        return False, "User not found in database."
    
    if user.get("groups_join", 0) >= 2:
        return False, "You have already joined 2 groups."

    last = user.get("last_join_time")
    if last:
        try:
            last_dt = datetime.fromisoformat(last)
            if datetime.utcnow() - last_dt < timedelta(hours=24):
                return False, "You must wait 24 hours before joining another group."
        except:
            pass

    return True, "ok"

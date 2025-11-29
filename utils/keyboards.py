# from telegram import InlineKeyboardButton
# from utils.constants import COACHINGS


# def build_batch_keyboard(coaching_key: str):
#     """
#     Returns an InlineKeyboard layout for available batches
#     of the selected coaching.
#     """
#     coaching = COACHINGS.get(coaching_key)

#     if not coaching:
#         return [[InlineKeyboardButton("No batches found", callback_data="none")]]

#     batches = coaching.get("batches", [])

#     keyboard = [
#         [InlineKeyboardButton(batch, callback_data=f"batch_{batch}")]
#         for batch in batches
#     ]

#     return keyboard

from telegram import InlineKeyboardButton
from utils.constants import COACHINGS


def build_batch_keyboard(coaching_key: str):
    """
    Returns an InlineKeyboard layout for batch selection.
    Encodes coaching + batch inside callback_data.
    """
    coaching = COACHINGS.get(coaching_key)

    if not coaching:
        return [[InlineKeyboardButton("No batches found", callback_data="none")]]

    batches = coaching.get("batches", [])

    # callback_data example: batch_pw_batch_1
    keyboard = [
        [
            InlineKeyboardButton(
                batch,
                callback_data=f"batch_{coaching_key}_{batch}"
            )
        ]
        for batch in batches
    ]

    return keyboard

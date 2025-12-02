from telegram import InlineKeyboardButton
from utils.constants import COACHINGS


def build_class_keyboard():
    """
    Returns an InlineKeyboard layout for student class selection.
    Options: Class 11, Class 12, Dropper
    """
    keyboard = [
        [InlineKeyboardButton("Class 11", callback_data="class_11")],
        [InlineKeyboardButton("Class 12", callback_data="class_12")],
        [InlineKeyboardButton("Dropper", callback_data="class_dropper")]
    ]
    return keyboard


def build_batch_keyboard(coaching_key: str, student_class: str):
    """
    Returns an InlineKeyboard layout for batch selection.
    Batches are specific to the student's class.
    
    Args:
        coaching_key: Selected coaching (e.g., 'allen', 'pw')
        student_class: Student's class ('11', '12', or 'dropper')
    """
    coaching = COACHINGS.get(coaching_key)

    if not coaching:
        return [[InlineKeyboardButton("No batches found", callback_data="none")]]

    # Map class codes to display names
    class_display = {
        "11": "Class 11",
        "12": "Class 12",
        "dropper": "Dropper"
    }
    
    class_name = class_display.get(student_class, student_class)
    
    # Generate class-specific batches
    # Each class has Batch A and Batch B
    batches = ["A", "B"]
    
    keyboard = [
        [
            InlineKeyboardButton(
                f"{class_name} - Batch {batch}",
                callback_data=f"batch_{coaching_key}_{student_class}_{batch}"
            )
        ]
        for batch in batches
    ]

    return keyboard

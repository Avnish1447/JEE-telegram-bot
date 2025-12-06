COACHINGS = {
    "pw": {
        "name": "PW",
        "classes": {
            "11": {"group_id": -1001234567890},      # Replace with actual Class 11 group ID
            "12": {"group_id": -1001234567891},      # Replace with actual Class 12 group ID
            "dropper": {"group_id": -1001234567892}  # Replace with actual Dropper group ID
        }
    },
    "allen": {
        "name": "Allen",
        "classes": {
            "11": {"group_id": -1001234567893},
            "12": {"group_id": -1001234567894},
            "dropper": {"group_id": -1001234567895}
        }
    },
    "aakash": {
        "name": "Aakash",
        "classes": {
            "11": {"group_id": -1001234567896},
            "12": {"group_id": -1001234567897},
            "dropper": {"group_id": -1001234567898}
        }
    },
    "resonance": {
        "name": "Resonance",
        "classes": {
            "11": {"group_id": -1001234567899},
            "12": {"group_id": -1001234567900},
            "dropper": {"group_id": -1001234567901}
        }
    },
    "fiitjee": {
        "name": "FIITJEE",
        "classes": {
            "11": {"group_id": -1001234567902},
            "12": {"group_id": -1001234567903},
            "dropper": {"group_id": -1001234567904}
        }
    },
}

# Helper function to get coaching key from group_id
def get_coaching_by_group_id(group_id: int) -> tuple[str | None, str | None]:
    """
    Returns (coaching_key, class_key) for a given group_id.
    Returns (None, None) if not found.
    """
    for coaching_key, coaching_data in COACHINGS.items():
        for class_key, class_data in coaching_data["classes"].items():
            if class_data["group_id"] == group_id:
                return coaching_key, class_key
    return None, None

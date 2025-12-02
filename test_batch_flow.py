"""
Test batch selection flow
"""
from utils.database import get_user, update_user
from utils.validators import user_is_eligible
from utils.constants import COACHINGS

def test_batch_flow():
    telegram_id = 1163516550
    callback_data = "batch_allen_11_A"
    
    print("=" * 60)
    print("TESTING BATCH SELECTION FLOW")
    print("=" * 60)
    
    # Parse callback
    print(f"\n1. Parsing callback: {callback_data}")
    parts = callback_data.split("_")
    print(f"   Parts: {parts}")
    
    if len(parts) < 4:
        print("   ❌ Invalid format")
        return
    
    coaching_key = parts[1]
    student_class = parts[2]
    batch_letter = parts[3]
    batch_full = f"{student_class}_{batch_letter}"
    
    print(f"   ✅ Coaching: {coaching_key}, Class: {student_class}, Batch: {batch_letter}")
    
    # Get user
    print(f"\n2. Getting user {telegram_id}")
    user = get_user(telegram_id)
    if not user:
        print("   ❌ User not found")
        return
    
    phone = user.get("phone")
    user_coaching = user.get("selected_coaching")
    user_class = user.get("student_class")
    
    print(f"   Phone: {phone}")
    print(f"   Coaching: {user_coaching}")
    print(f"   Class: {user_class}")
    
    if not user_coaching or not phone or not user_class:
        print("   ❌ Incomplete registration")
        return
    
    print("   ✅ User data complete")
    
    # Check eligibility
    print(f"\n3. Checking eligibility for phone: {phone}")
    eligible, reason = user_is_eligible(phone)
    if not eligible:
        print(f"   ❌ Not eligible: {reason}")
        return
    print(f"   ✅ Eligible: {reason}")
    
    # Save batch
    print(f"\n4. Saving batch: {batch_full}")
    update_user(telegram_id, {"selected_batch": batch_full})
    print("   ✅ Batch saved")
    
    # Get coaching config
    print(f"\n5. Getting coaching config for: {coaching_key}")
    coaching = COACHINGS.get(coaching_key)
    if not coaching:
        print("   ❌ Coaching not found")
        return
    
    group_id = coaching.get("group_id")
    print(f"   Group ID: {group_id}")
    print(f"   Starts with -100123456789? {str(group_id).startswith('-100123456789')}")
    
    # Determine invite URL
    print(f"\n6. Determining invite URL")
    if group_id is None or str(group_id).startswith("-100123456789"):
        invite_url = "https://t.me/+PLACEHOLDER_INVITE_LINK"
        print(f"   ✅ Using placeholder: {invite_url}")
    else:
        print(f"   Would create real invite link for group: {group_id}")
        invite_url = "REAL_LINK"
    
    # Format message
    print(f"\n7. Formatting final message")
    class_display = {
        "11": "Class 11",
        "12": "Class 12",
        "dropper": "Dropper"
    }.get(student_class, student_class)
    
    batch_display = f"{class_display} - Batch {batch_letter}"
    
    message = (
        f"🎉 **You're eligible!**\\n\\n"
        f"📚 Coaching: *{coaching['name']}*\\n"
        f"🎒 Class: *{class_display}*\\n"
        f"🏷 Batch: *{batch_display}*\\n"
        f"📞 Phone: `{phone}`\\n\\n"
        f"Here is your **one-time invite link**:\\n{invite_url}"
    )
    
    print("\n" + "=" * 60)
    print("FINAL MESSAGE:")
    print("=" * 60)
    print(message)
    print("=" * 60)
    print("\n✅ ALL STEPS PASSED!")

if __name__ == "__main__":
    test_batch_flow()

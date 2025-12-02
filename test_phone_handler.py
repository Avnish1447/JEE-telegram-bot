"""
Test script to debug phone handler
"""
import asyncio
from utils.database import get_user, update_user
from utils.validators import normalize_phone, user_is_eligible
from utils.keyboards import build_class_keyboard

async def test_phone_flow():
    telegram_id = 1163516550
    phone_input = "7869001255"
    
    print("=" * 60)
    print("TESTING PHONE HANDLER FLOW")
    print("=" * 60)
    
    # Step 1: Validate phone
    print(f"\n1. Validating phone: {phone_input}")
    phone = normalize_phone(phone_input)
    if not phone:
        print("   ❌ Phone validation FAILED")
        return
    print(f"   ✅ Phone normalized to: {phone}")
    
    # Step 2: Get user
    print(f"\n2. Getting user {telegram_id} from database")
    user = get_user(telegram_id)
    if not user:
        print("   ❌ User NOT found")
        return
    print(f"   ✅ User found: {user}")
    
    # Step 3: Check coaching
    print(f"\n3. Checking coaching selection")
    selected_coaching = user.get("selected_coaching")
    if not selected_coaching:
        print("   ❌ No coaching selected")
        return
    print(f"   ✅ Coaching: {selected_coaching}")
    
    # Step 4: Update phone
    print(f"\n4. Updating phone in database")
    update_user(telegram_id, {"phone": phone})
    print(f"   ✅ Phone updated")
    
    # Step 5: Check eligibility
    print(f"\n5. Checking eligibility")
    eligible, reason = user_is_eligible(phone)
    if not eligible:
        print(f"   ❌ NOT eligible: {reason}")
        return
    print(f"   ✅ Eligible: {reason}")
    
    # Step 6: Build keyboard
    print(f"\n6. Building class keyboard")
    keyboard = build_class_keyboard()
    print(f"   ✅ Keyboard built: {len(keyboard)} buttons")
    for row in keyboard:
        for button in row:
            print(f"      - {button.text}: {button.callback_data}")
    
    print("\n" + "=" * 60)
    print("✅ ALL STEPS PASSED - Phone handler should work!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_phone_flow())

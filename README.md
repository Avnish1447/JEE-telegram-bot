# JEE Simplified - Telegram Access Bot

A Telegram bot that manages controlled access to JEE coaching-related Telegram groups. The bot handles user registration, phone verification, eligibility checks, and generates one-time invite links for approved users.

## Features

- 🎓 **Multi-Coaching Support**: Supports PW, Allen, Aakash, Resonance, and FIITJEE
- 📱 **Phone Verification**: Validates and normalizes Indian mobile numbers
- 🔐 **Access Control**: Limits users to 2 group joins with 24-hour cooldown
- 🎫 **One-Time Invite Links**: Generates single-use invite links for verified users
- 📊 **Join Logging**: Tracks all join attempts (success/failure) in JSON and text formats
- ✅ **Group Verification**: Validates users when they join via invite links
- 🎒 **Class Selection**: Support for Class 11, Class 12, and Dropper students
- 👨‍💼 **Admin Commands**: Track user statistics and daily registrations (admin-only)

---

## Installation

### Prerequisites

- Python 3.10 or higher
- A Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Admin access to Telegram groups you want to manage

### Steps

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot** (see Configuration section below)

4. **Run the bot**:
   ```bash
   python bot.py
   ```

---

## Configuration

### 1. Set Your Bot Token

Open `bot.py` and update line 73 with your bot token:

```python
TOKEN = "YOUR_BOT_TOKEN_HERE"
```

**Security Note**: For production, use environment variables instead:
```python
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
```

### 2. Configure Group IDs

Open `utils/constants.py` and replace the placeholder `group_id` values with your actual Telegram group IDs:

```python
COACHINGS = {
    "pw": {
        "name": "PW", 
        "batches": ["batch_1", "batch_2"],
        "group_id": -1001234567890  # Replace with actual group ID
    },
    # ... update all coaching entries
}
```

**How to get Telegram Group IDs:**

1. Add your bot to the target group as an admin
2. Send any message in the group
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Find the `chat` object and copy the `id` value (it's a negative number)

### 3. Configure Batches (Optional)

You can customize batch names in `utils/constants.py`:

```python
"batches": ["batch_1", "batch_2"]  # Change to your batch names
```

---

## How It Works

### User Flow

1. **Start**: User sends `/start` to the bot
2. **Select Coaching**: User chooses their coaching institute (PW, Allen, etc.)
3. **Phone Verification**: User enters their 10-digit mobile number (returning users skip this)
4. **Class Selection**: User selects their class (11, 12, or Dropper)
5. **Batch Selection**: User selects their batch
6. **Eligibility Check**: Bot verifies user can join (max 2 groups, 24hr cooldown)
7. **Invite Link**: Bot generates a one-time invite link
8. **Join Group**: User clicks link and joins the group
9. **Verification**: Bot verifies user when they join via the invite link

### Access Restrictions

The bot enforces the following rules:

#### 1. **Maximum 2 Groups Per User**
- Each user can join a maximum of 2 groups total
- Tracked via `groups_join` counter in user database
- Prevents abuse and ensures fair access

#### 2. **24-Hour Cooldown Between Joins**
- Users must wait 24 hours between joining different groups
- Tracked via `last_join_time` timestamp
- Prevents rapid group hopping

#### 3. **Phone Number Validation**
- Must be a valid 10-digit Indian mobile number
- Must start with 6, 7, 8, or 9
- Accepts formats: `9876543210`, `+919876543210`, `919876543210`
- Automatically normalized to 10-digit format

#### 4. **Coaching Verification**
- Users can only join groups for their selected coaching
- Verified when user joins via invite link
- Prevents cross-coaching access

#### 5. **One-Time Invite Links**
- Each invite link has `member_limit=1`
- Link becomes invalid after one use
- Prevents link sharing

---

## Project Structure

```
telegram-access-bot/
├── bot.py                      # Main bot entry point
├── config.py                   # Admin configuration
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── migrate_add_created_at.py   # Database migration script
├── data/                       # Data storage (auto-created)
│   └── users.db               # SQLite user database
├── handlers/                   # Command and callback handlers
│   ├── start_handler.py       # /start command
│   ├── coaching_handler.py    # Coaching selection
│   ├── phone_handler.py       # Phone number validation
│   ├── class_handler.py       # Class selection (11/12/Dropper)
│   ├── batch_handler.py       # Batch selection & invite links
│   ├── invite_handler.py      # New member verification
│   └── admin_handler.py       # Admin commands
└── utils/                      # Utility modules
    ├── constants.py           # Coaching configs & invite mappings
    ├── database.py            # SQLite database operations
    ├── validators.py          # Phone & eligibility validation
    ├── keyboards.py           # Inline keyboard builders
    ├── security.py            # Kick/ban functions
    ├── logging_utils.py       # Join attempt logging
    ├── admin.py               # Admin authentication
    └── storage.py             # Alternative storage functions
```

---

## Database Schema

User data is stored in SQLite database `data/users.db`:

**Users Table:**
- `telegram_id` (INTEGER PRIMARY KEY) - User's Telegram ID
- `phone` (TEXT UNIQUE) - Verified phone number
- `selected_coaching` (TEXT) - Chosen coaching institute
- `selected_batch` (TEXT) - Selected batch
- `student_class` (TEXT) - Class (11, 12, or dropper)
- `groups_join` (INTEGER) - Number of groups joined
- `last_join_time` (TEXT) - Last group join timestamp
- `banned` (INTEGER) - Ban status (0 or 1)
- `created_at` (TIMESTAMP) - Registration timestamp

---

## Admin Commands

**Admin-only commands** for tracking user statistics (configured in `config.py`):

### `/stats`
Quick overview of user statistics:
- Total registered users
- Users registered today
- New users this week

### `/daily_stats [days]`
Detailed daily registration breakdown with visual charts:
- Shows last N days (default: 7, max: 30)
- Bar chart visualization
- Total and average calculations

**Example:**
```
/stats
/daily_stats
/daily_stats 14
```

**Admin Configuration:**
Add your Telegram user ID to `config.py`:
```python
ADMIN_USER_IDS = [
    1163516550  # Your admin user ID
]
```

---

## Logs

Join attempts are logged in `logs/` directory with timestamps and status.

---


## License

This project is provided as-is for educational purposes.


---

## Support

For issues or questions, please contact the project maintainer.

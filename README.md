# JEE Simplified - Telegram Access Bot

A Telegram bot that manages controlled access to JEE coaching-related Telegram groups. The bot handles user registration, phone verification, eligibility checks, and generates one-time invite links for approved users.

## Features

- 🎓 **Multi-Coaching Support**: Supports PW, Allen, Aakash, Resonance, and FIITJEE
- 📱 **Phone Verification**: Validates and normalizes Indian mobile numbers
- 🔐 **Access Control**: Limits users to 2 group joins with 24-hour cooldown
- 🎫 **One-Time Invite Links**: Generates single-use invite links for verified users
- 📊 **Join Logging**: Tracks all join attempts (success/failure) in JSON and text formats
- ✅ **Group Verification**: Validates users when they join via invite links

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

## How to Run

### Development Mode

```bash
python bot.py
```

The bot will run with placeholder group IDs and show test messages instead of creating real invite links.

### Production Mode

1. Configure real group IDs in `utils/constants.py`
2. Make sure the bot is an admin in all groups
3. Run the bot:
   ```bash
   python bot.py
   ```

### Running in Background (Linux/Mac)

```bash
nohup python bot.py > bot.log 2>&1 &
```

### Running as a Service (Recommended for Production)

Create a systemd service file `/etc/systemd/system/telegram-bot.service`:

```ini
[Unit]
Description=JEE Simplified Telegram Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/telegram-access-bot
Environment="TELEGRAM_BOT_TOKEN=your_token_here"
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

---

## How It Works

### User Flow

1. **Start**: User sends `/start` to the bot
2. **Select Coaching**: User chooses their coaching institute (PW, Allen, etc.)
3. **Phone Verification**: User enters their 10-digit mobile number
4. **Batch Selection**: User selects their batch
5. **Eligibility Check**: Bot verifies user can join (max 2 groups, 24hr cooldown)
6. **Invite Link**: Bot generates a one-time invite link
7. **Join Group**: User clicks link and joins the group
8. **Verification**: Bot verifies user when they join via the invite link

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
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── data/                       # Data storage (auto-created)
│   ├── users.json             # User database
│   ├── join_logs.json         # Structured join logs
│   └── join_logs.txt          # Human-readable logs
├── handlers/                   # Command and callback handlers
│   ├── start_handler.py       # /start command
│   ├── coaching_handler.py    # Coaching selection
│   ├── phone_handler.py       # Phone number validation
│   ├── batch_handler.py       # Batch selection & invite links
│   └── invite_handler.py      # New member verification
└── utils/                      # Utility modules
    ├── constants.py           # Coaching configs & invite mappings
    ├── database.py            # User data management
    ├── validators.py          # Phone & eligibility validation
    ├── keyboards.py           # Inline keyboard builders
    ├── security.py            # Kick/ban functions
    ├── logging_utils.py       # Join attempt logging
    └── storage.py             # Alternative storage functions
```

---

## Database Schema

User data is stored in `data/users.json`:

```json
{
  "123456789": {
    "phone": "9876543210",
    "telegram_id": 123456789,
    "groups_join": 1,
    "last_join_time": "2025-11-29T12:30:00",
    "joined_group_list": [-1001234567890],
    "last_invite_link": {"link": "", "chat_id": 0},
    "selected_coaching": "pw",
    "selected_batch": "batch_1"
  }
}
```

---

## Logs

### Join Logs (JSON)
`data/join_logs.json` - Structured logs for programmatic access

### Join Logs (Text)
`data/join_logs.txt` - Human-readable logs

Example:
```
2025-11-29 18:30:00 | user_id=123456789 | username=john | coaching=pw | batch=batch_1 | status=attempt
2025-11-29 18:30:01 | user_id=123456789 | username=john | coaching=pw | batch=batch_1 | status=success
```

---

## Troubleshooting

### Bot doesn't respond
- Check if bot is running: `ps aux | grep bot.py`
- Check bot token is correct
- Verify bot is not blocked by user

### "Chat not found" error
- Ensure bot is added to the group as admin
- Verify `group_id` is correct (negative number)
- Check bot has permission to create invite links

### Phone validation fails
- Ensure number is 10 digits
- Must start with 6, 7, 8, or 9
- Try with country code: +91XXXXXXXXXX

### User can't join group
- Check if user has already joined 2 groups
- Verify 24-hour cooldown has passed
- Ensure coaching selection matches

---

## Security Considerations

1. **Never commit bot token to Git**
   - Use environment variables
   - Add `.env` to `.gitignore`

2. **Protect user data**
   - `data/users.json` contains phone numbers
   - Add `data/` to `.gitignore`
   - Implement proper access controls

3. **Bot permissions**
   - Only grant necessary admin permissions
   - Regularly audit group members

---

## License

This project is provided as-is for educational purposes.

---

## Support

For issues or questions, please contact the project maintainer.

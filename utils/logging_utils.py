import json
from pathlib import Path
from datetime import datetime
LOG_FILE = Path("data/join_logs.json")
TEXT_LOG_FILE = Path("data/join_logs.txt")

def log_join_attempt(telegram_id, username,coaching,batch,status):
    LOG_FILE.parent.mkdir(parents=True, exists_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = {
        "telegram_id": telegram_id,
        "username": username,
        "coaching": coaching,
        "batch": batch,
        "status": status,
        "time": datetime.utcnow().isoformat()
    }

    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
            if not isinstance(logs, list):
                logs = []
        except:
            logs = []
    else:
        logs = []

    logs.append(log_entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
         json.dump(logs, f, indent=4)


    text_line = (
         f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        f"user_id={telegram_id} | username={username} | "
        f"coaching={coaching} | batch={batch} | status={status}\n"
    )

    with open(TEXT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text_line)


#EXAMPLE OUTPUT
# 2025-02-10 16:42:22 | user_id=12345 | username=john | coaching=pw | batch=batch_1 | status=attempt
# 2025-02-10 16:42:23 | user_id=12345 | username=john | coaching=pw | batch=batch_1 | status=success

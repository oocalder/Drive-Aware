import os
import time
from datetime import datetime
import shutil
import requests  

# 🔁 Update this with your actual SD card path
EVENT_FOLDER = "/media/pi/WOLFBOX/DCIM/EVENT"
DEST_FOLDER = "/home/pi/wolfbox_events"
LOG_FILE = "/home/pi/wolfbox_event_log.txt"

seen_files = set()

def get_event_files():
    return set(f for f in os.listdir(EVENT_FOLDER) if f.endswith(".mp4") or f.endswith(".ts"))

def log_event(filename):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp}: Collision clip saved — {filename}\n")
    print(f"[{timestamp}] New collision file detected: {filename}")

def copy_file(filename):
    src = os.path.join(EVENT_FOLDER, filename)
    dst = os.path.join(DEST_FOLDER, filename)
    shutil.copy2(src, dst)

def trigger_alexa():
    try:
        requests.post("https://maker.ifttt.com/trigger/collision_event/with/key/YOUR_IFTTT_KEY")
        print("✅ Alexa trigger sent!")
    except Exception as e:
        print("❌ Alexa trigger failed:", e)

# Ensure destination folder exists
os.makedirs(DEST_FOLDER, exist_ok=True)

print("📹 Monitoring Wolfbox dashcam for emergency events...")

while True:
    try:
        current_files = get_event_files()
        new_files = current_files - seen_files

        for file in new_files:
            log_event(file)
            copy_file(file)
            trigger_alexa()  

        seen_files = current_files
        time.sleep(5)
    except Exception as e:
        print("❌ Error:", e)
        time.sleep(5)

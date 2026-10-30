from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

# --- VIDEO DIRECTORY SETUP WITH FALLBACK ---
PRIMARY_VIDEO_FOLDER = '/mnt/dashcam/event/CH1'
BACKUP_VIDEO_FOLDER = '/home/pi/backup_event/CH1'

# Check for folder availability
if os.path.exists(PRIMARY_VIDEO_FOLDER):
    VIDEO_FOLDER = PRIMARY_VIDEO_FOLDER
    print("[INFO] Using primary video folder.")
elif os.path.exists(BACKUP_VIDEO_FOLDER):
    VIDEO_FOLDER = BACKUP_VIDEO_FOLDER
    print("[INFO] SD card not found. Using backup folder.")
else:
    VIDEO_FOLDER = None
    print("[ERROR] No valid video folder found.")

LOG_FILE = 'motion_log.json'

# --- HOME PAGE ROUTE: LIST VIDEOS ---
@app.route('/')
def home():
    if not VIDEO_FOLDER:
        return "No video folder found", 500
    videos = [f for f in os.listdir(VIDEO_FOLDER) if f.endswith('.mp4')]
    return render_template('videos.html', videos=videos)

# --- STREAM OR DOWNLOAD A SPECIFIC VIDEO ---
@app.route('/video/<filename>')
def serve_video(filename):
    if not VIDEO_FOLDER:
        return "Video folder not found", 500
    return send_from_directory(VIDEO_FOLDER, filename)

# --- RECEIVE MOTION SENSOR DATA VIA POST ---
@app.route('/motion', methods=['POST'])
def receive_motion():
    data = request.get_json()
    data['timestamp_received'] = datetime.utcnow().isoformat()

    # Load existing motion log or create new one
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
    else:
        logs = []

    # Append new motion entry
    logs.append(data)

    # Save updated log
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

    print("[INFO] Motion data received:", data)
    return jsonify({"message": "Motion data received"}), 200

# --- VIEW MOTION LOG AS JSON ---
@app.route('/motion-log')
def motion_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
    return jsonify(logs)

# --- TEST CONNECTION ENDPOINT ---
@app.route('/test', methods=['GET'])
def test_connection():
    return "Hello from Raspberry Pi!", 200

# --- START FLASK SERVER ---
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)

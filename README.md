# Drive Aware
### Smart Incident Logger & Dashcam Video Browser — Raspberry Pi / Flask / IoT prototype

**Project type:** Personal technical prototype and integration case study  
**Primary focus:** Raspberry Pi, Python, Flask, dashcam file access, JSON logging, and integration troubleshooting  
**Status:** Historical prototype, archived for demonstration; **not a deployed or end-to-end collision-detection product**

> **What works and what doesn't:** The Pi-side Flask server was previously demonstrated receiving test motion data, retaining JSON logs, and listing/serving dashcam files. The phone-to-Pi accelerometer workflow did not reach verified end-to-end operation. Wolfbox event polling and Alexa notifications exist as prototype code, **not verified production integrations**. The supplied source has not been freshly tested on the original hardware.

## 1. The idea

Drive Aware began as a question: could I connect a consumer dashcam, a Raspberry Pi, a phone's motion sensors, and an at-home voice assistant to help organize and surface driving incidents?

I was interested in connected-vehicle workflows and in fleet-technology approaches to event monitoring. The goal was to make recordings and metadata easier to retrieve, without having to manually hunt through footage on an SD card. This project was independently built as a learning exercise; it is not affiliated with Samsara, Rivian, Wolfbox, or Amazon.

The **original proposed workflow** was:

1. Detect an unusual event using motion measurements or the dashcam's built-in emergency recording feature.
2. Retrieve or copy the related recorded video to a Raspberry Pi.
3. Record event metadata or motion observations through a Python/Flask backend.
4. Browse footage and logs from a local web page.
5. Optionally notify a household device through an Alexa-related integration.

This is the proposed architecture, **not a claim that all five steps were connected and functioning**.

## 2. Equipment and tools

| Layer | Technology / role |
| --- | --- |
| Camera | Wolfbox G840S mirror dashcam and its SD-card recordings |
| Edge device | Raspberry Pi 4, used as the locally hosted server |
| Backend | Python + Flask |
| Data transport | HTTP POST and JSON for motion samples |
| UI | HTML template for local dashcam video links |
| Experiment | Cordova/VoltBuilder Android accelerometer client, JavaScript, Smoothie Charts |
| Optional notification concept | Python event watcher + an IFTTT webhook intended for Alexa notification automation |

The earlier PDF documents an Echo Show and testing with Android; the source files in this archive do not establish a completed Alexa delivery.

## 3. System design

```text
                          [Dashcam / SD card]
                                  |
                       recorded .mp4 files
                                  |
                         [Raspberry Pi]
                                  |
                     Python / Flask server
                     /         |          \
                GET /     GET /video/     POST /motion
                  |        <filename>        |
           video listing   video file    JSON motion log
                  |                        GET /motion-log
                  +-------------+------------+
                                |
                          local browser

    EXPERIMENTAL / NOT VERIFIED END-TO-END
    [Android Cordova accelerometer] --HTTP POST--> [Flask /motion]

    SEPARATE PROTOTYPE / NOT CONNECTED TO FLASK
    [Local event-file watcher] --> [copy file to separate folder]
                               --> [IFTTT placeholder webhook]
```

**Important architectural distinction:** `wolfbox/watch_wolfbox_events.py` watches an example SD-card directory and copies recordings to its own destination. `server/app.py` lists videos from a **different** directory. As written, those programs do not form a complete automated dashcam-to-dashboard pipeline.

## 4. What I built and validated historically

### A. Raspberry Pi Flask server

`server/app.py` exposes a small local HTTP service that:

- Finds a video directory using a primary path with a backup-path fallback.
- Displays available `.mp4` files through `server/templates/videos.html`.
- Serves selected recordings from that directory.
- Accepts JSON via `POST /motion`, adds a server-receipt timestamp, and appends entries to `motion_log.json`.
- Displays saved motion observations through `GET /motion-log`.
- Responds to `GET /test` with a simple connection message.

In the original documentation, local `curl` requests successfully returned `Motion data received`, and a browser displayed a dashcam recording. The included `examples/motion_log.sample.json` contains two historical test-style measurements; **these are not evidence that a real collision was detected**.

### B. Local video browser

An HTML/Jinja template rendered the available video filenames and links. This was deliberately a minimal proof of file access, rather than a polished dashboard. The archived `dashcam_server.zip` placed `videos.html` outside Flask's default `templates/` directory. For repository packaging, it has been moved into the conventional folder, without rewriting its content.

### C. Mobile accelerometer experiment

I built a Cordova-based Android app interface that displays X/Y/Z acceleration values and graphs them. Its JavaScript also attempts to POST each reading to the Pi's Flask endpoint. However, the source and my original testing notes show the mobile app did **not** achieve reliable end-to-end delivery.

Debugging exposed a mismatch between a local HTTPS-hosted Cordova webview and a plain HTTP endpoint on the Raspberry Pi, with cleartext network/security configuration involved. This prompted edits to the app Content Security Policy and Android manifest configuration. The code still points to a particular private-network IP and remains **experimental**. It also sends **raw samples**, not classified collision events.

### D. Wolfbox event watcher — recovered prototype

`wolfbox/watch_wolfbox_events.py` polls a configured directory for `.mp4` and `.ts` files, copies newly encountered filenames to a separate folder, logs their names, and attempts an IFTTT webhook request. That script was recovered separately from the archives; the uploaded `Samsara Wolfbox.zip` contained **no files**.

This proves the intended *integration approach is represented in source code*, not that the watcher executed successfully on the camera or delivered Alexa alerts. It relies on recordings being present in an accessible directory; it does not communicate with the camera over its proprietary Wi-Fi connection.

## 5. Troubleshooting and engineering decisions

| Challenge | What happened / lesson |
| --- | --- |
| Dashcam power | A blown 15A 12V car fuse prevented power; replacing it resolved the physical installation issue, as documented at the time. |
| Consumer-camera connectivity | Wolfbox Wi-Fi Direct / proprietary behavior did not expose a convenient network file system. SD-card file access became the more realistic approach. |
| Hardware vs. motion prediction | The camera already provided emergency recordings; relying on its own event capture was more plausible than inventing reliable collision detection from a phone accelerometer. |
| Flask endpoint testing | `curl` was useful to isolate server functionality from client or networking problems. |
| Android mobile transport | Cordova security/network configuration caused difficulty posting to the Pi. Browser connectivity and a successful test POST did not prove automated mobile-to-Pi telemetry worked. |
| Alexa notifications | An originally considered webhook/voice route was not demonstrated end to end; the recovered watcher retains an unconfigured IFTTT request. |
| Portability | Hard-coded Pi paths, LAN IPs, and untested build assumptions limit reuse on a different device. |

The most valuable lesson was **separating a proven backend endpoint from unverified hardware and mobile integrations**, and adapting the design when a consumer product's interface was closed.

## 6. Current status and limitations

| Capability | Evidence | Status |
| --- | --- | --- |
| Flask motion-receipt endpoint | Python source, original test notes, historical sample log | **Previously verified** using test requests |
| Local JSON read/write | Python source and sample records | **Previously verified** for test data |
| Local dashcam video listing and playback | Flask/Jinja source and PDF screenshot | **Previously demonstrated** |
| `/test` connection endpoint | Standalone Raspberry Pi source | **Implemented**, not retested here |
| Phone X/Y/Z visualization | Cordova app source and PDF screenshots | **Built / demonstrated locally** |
| Phone → Pi automatic motion POST | Client code and unsuccessful debugging notes | **Not verified end-to-end** |
| Automatic event-video ingestion | File-watcher code with different storage paths | **Prototype only** |
| Alexa household announcement | Webhook placeholder in watcher, no delivery evidence | **Concept / unverified** |
| Collision detection or classification | No robust classification logic or sensor calibration | **Not implemented** |
| Publicly accessible or production-ready service | No authentication, deployment protections, or validation | **Not implemented** |

**Engineering limitations to acknowledge:**

- The Pi server uses hard-coded example paths. For this public archive its Flask entry point now binds to `127.0.0.1` with `debug=False`; the **original** code bound to all interfaces in debug mode. This prototype has no authentication and is **not an internet-facing deployment**.
- The server does not authenticate clients or robustly validate incoming motion JSON. The log is a flat JSON file, not a concurrent database.
- The phone script posts each accelerometer sample at a configured 1-second interval and displays a success/error alert for each attempt; it does not calculate crash thresholds or distinguish routine bumps from collisions.
- The recovered watcher starts with an empty in-memory seen-file set, so pre-existing recordings may be treated as newly discovered after a restart; it also lacks settled-file checks, retry policy, request timeouts, and response-status verification.
- The mobile `index.html` and JavaScript originally contained a private home-network IP address. It has been replaced with the `PI_HOST` placeholder; set a trusted local hostname or address before attempting tests.
- There is **no evidence of a verified continuous workflow** from event detection through matching video retrieval and announcement.
- The original Android build/signing configuration contained plaintext credentials. The packaged example replaces those credentials with placeholders. If the originals were real or reused, their passwords should be rotated.

## 7. Next integrations — deliberately out of scope for this archive

1. **Event ingestion (first priority):** Harmonize watcher destination and Flask video folder; process only completed video writes and store each video event once.
2. **Unified event model:** Give each event an ID, file location, recording timestamp, event source, and optional accelerometer/GPS measurements.
3. **Local dashboard:** Display a searchable timeline where a motion record can be associated with a known video file.
4. **Mobile telemetry (optional):** Revisit the Cordova client, make endpoint URL configurable, use an appropriate secure network transport, buffer failed uploads, and replace per-sample alerts with useful app status.
5. **Alexa/home integration (optional):** Design a tested, permissioned notification service only after reliable event classification and ingestion exist.
6. **Hardening and testability:** Add safe configuration, request validation, local-only default, logging/retention controls, and repeatable simulated-event tests.

These are design goals, **not delivered features**. Collision notifications in particular should never be used as a safety-critical or emergency response system without substantial validation.

## 8. Repository guide

```text
Drive_Aware_GitHub_Sanitized/
├── README.md                     Main project story and technical case study
├── requirements.txt              Python dependencies (not locked/tested)
├── .gitignore                    Keeps generated files and credentials out
├── server/
│   ├── app.py                    Latest supplied Raspberry Pi Flask app, with paths redacted and local-only safe defaults
│   └── templates/videos.html     Historical video listing HTML, correctly placed for Flask
├── wolfbox/
│   └── watch_wolfbox_events.py   Recovered event-monitoring prototype
├── mobile/
│   ├── config.xml                Cordova config with namespace correction and author/package redactions
│   ├── voltbuilder.example.json  Sanitized, nonfunctional signing config example
│   ├── www/                      Original app HTML, CSS, JS, and bundled chart library
│   └── resources/                Neutral placeholder icons (not original branded graphics)
├── examples/
│   ├── curl_motion.json          Sample test POST body
│   └── motion_log.sample.json    Two historical sample motion records
└── docs/
    ├── SOURCE_AUDIT.md           Which files came from which uploads, plus changes
    ├── PORTFOLIO_PROJECT_01.md   Website copy, presentation outline and evidence checklist
    ├── THIRD_PARTY.md           Source attributions and publication considerations
    └── SECURITY_AND_PRIVACY.md   Publication safety notes and redactions
```

### Inspecting the prototype locally (optional)

The following demonstrates only **server endpoints**, not a working dashcam or collision detector. Test on a trusted local computer; do not expose this prototype to the internet.

```bash
python -m venv .venv
# Activate the environment, then:
pip install -r requirements.txt
cd server
python app.py
```

In a separate terminal, test with:

```bash
curl http://127.0.0.1:5000/test
curl -X POST http://127.0.0.1:5000/motion \
  -H 'Content-Type: application/json' \
  -d '{"x":1.2,"y":0.5,"z":9.8,"timestamp":"2025-05-28T00:00:00Z"}'
curl http://127.0.0.1:5000/motion-log
```

The video homepage requires the original dashcam folder, or the app's configured backup folder, to exist with recordings. Without those paths, `/` currently returns a missing-directory response. Running these commands does not make the full project work automatically. The historic `app.py` enabled debug mode and bound to all interfaces; this public copy now uses localhost and disables debug. Do not expose this unauthenticated service to the internet.

For Android, the `mobile/` directory is **archived source, not a verified build recipe**. `voltbuilder.example.json` cannot sign a package until you supply your *own* signing assets; never commit them. The phone network configuration also requires revision before any retest.

## 9. How I would present this project

**One-line portfolio description:** Designed a Raspberry Pi/Flask prototype for browsing dashcam footage and logging motion events, with documented experiments in mobile sensor integration and home alerts.

**Emphasize:** API tests, integration boundaries, investigation of closed hardware interfaces, file-system fallbacks, JSON persistence, and candid scoping of the unfinished pieces.

**Avoid claiming:** an operational collision detection engine, automatically triggered emergency recordings, a reliable mobile data feed, or working Alexa announcements.

For suggested copy that fits the `Project 01` data fields in my current portfolio, see [`docs/PORTFOLIO_PROJECT_01.md`](docs/PORTFOLIO_PROJECT_01.md).

---

### Project note

Personal network addresses, usernames, app metadata, and unsafe Flask startup defaults have been redacted or changed. This is a **curated archival release**, not a claim that the historic Raspberry Pi environment has been reproduced. See [`docs/SOURCE_AUDIT.md`](docs/SOURCE_AUDIT.md) for the origin of each file and the few publication-safe changes made for this repository. No incident footage or proprietary software firmware is included.

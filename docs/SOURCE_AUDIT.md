# Source audit and release notes

This repository packages selected user-provided project sources as a historical technical case study. It is **not** a functioning end-to-end release.

## Upload inventory

| Uploaded item | What was found | Repository treatment |
| --- | --- | --- |
| `Drive Aware.docx.pdf` | Six-page original project plan, issues, photos and test screenshots | Used as narrative reference; not redistributed in repo |
| `dashcam_server.zip` | Old Flask app, `motion_log.json` empty, HTML template misplaced at root | Compared with standalone latest Pi files; not included separately |
| `app.py` | Pi Flask server with additional `/test` endpoint | Copied into `server/app.py`; username redacted and safe localhost-only startup set |
| `videos.html` | Jinja HTML list of video links | Copied into `server/templates/videos.html` to satisfy Flask's template lookup |
| `motion_log.json` | Two entries with test-style acceleration readings | Copied into `examples/motion_log.sample.json`, explicitly labeled as sample data |
| `watch_wolfbox_events.py` | Standalone polling/copying script with IFTTT webhook placeholder | Copied into `wolfbox/`, unchanged (contains generic `/home/pi` paths) |
| `Samsara Wolfbox.zip` | Valid ZIP with **zero entries** | No content to include; standalone watcher preserved |
| `Samsara Accelerometer.zip` | Cordova HTML/JS/CSS/config; chart library; signing passwords; branded icons | Archived in `mobile/` with the safety/portability changes below |
| `portfolio.zip` | Existing static portfolio with three placeholder projects | Not bundled with this separate GitHub project repository; `Project 01` copy provided in docs |

## Specific changes from supplied files

1. **Moved HTML template:** `videos.html` now lives in `server/templates/videos.html` so Flask can find it.
2. **XML parser fix only:** Added `xmlns:android="http://schemas.android.com/apk/res/android"` to `mobile/config.xml`. The original contained `android:`-prefixed manifest attributes but no namespace binding. This is not a claim that a Cordova build now works.
3. **Removed credentials:** Replaced the original `voltbuilder.json` with `voltbuilder.example.json`, where signing passwords are placeholders. The original unredacted file is **not included**.
4. **Replaced third-party app branding:** Removed original Samsara-branded icon/splash resources. Neutral `DA` placeholders keep those file references present without implying endorsement or ownership of the trademark.
5. **Privacy redactions:** Replaced the original local-network address in the mobile HTML and JavaScript with `PI_HOST`, changed the user-specific Pi backup path to `/home/pi/backup_event/CH1`, removed author email/name and identifying mobile package ID from `mobile/config.xml`, and replaced a legacy branded provision-file example. This alters configuration examples, not the implemented integration logic.
6. **Safer Flask defaults:** Changed Flask binding from all interfaces in debug mode to `127.0.0.1` and `debug=False`. Other devices on the LAN cannot reach this server unless explicitly reconfigured.
7. **Added documentation:** README, technical source audit, portfolio copy, third-party notes, .gitignore, basic Python dependency list, and non-executable example JSON payloads.
8. **No integration functionality rewritten:** Flask route handlers, JavaScript accelerometer logic, and watcher behavior have not been redesigned or extended.

## Important mismatches in historical artifacts

- Flask reads video clips from `/mnt/dashcam/event/CH1` or the sanitized example path `/home/pi/backup_event/CH1`; the Wolfbox watcher reads `/media/pi/WOLFBOX/DCIM/EVENT` and copies to `/home/pi/wolfbox_events`. There is no code linking the watcher output into Flask's video directory.
- The uploaded older `dashcam_server.zip` Flask app lacks the `/test` endpoint present in the later standalone Pi `app.py`. The later version was selected.
- The original PDF mentions a `/tester` route during experimentation; the current file implements `/test`.
- The PDF describes potential voice notifications, but the supplied watcher only contains an IFTTT request with a placeholder key; no Alexa implementation is proven.
- The accelerometer front end tries to send **every reading**, not only suspected incidents, and its network issues are unresolved in the available evidence.

## Verification performed during packaging

- Reviewed ZIP entries and compared both Flask app copies.
- Parsed supplied Python for syntax and reviewed the motion sender, configuration, video routes, and event-watcher implementation.
- Observed that original mobile `config.xml` was invalid XML due to the missing `android` namespace; the packaged XML is parseable.
- No hardware, Android device, dashcam recording, IFTTT account, or running Flask environment was available for an end-to-end test. The packaging process does **not** establish current operational behavior.

## Before pushing publicly

Check the git diff; ensure there are no original password files, camera footage, personally sensitive GPS data, license-key files, or signing certificates. **Rotate any old signing passwords if you have ever reused them elsewhere.**

# Publication & privacy check

This public archive was prepared as a historical demonstration, **not a security-reviewed deployed application**.

- Replaced the former private LAN host in the mobile HTML and JavaScript with the placeholder `PI_HOST`.
- Removed the original author name, email address, and personally attributable Android application ID from the Cordova config.
- Replaced the Pi user's personal home directory with a generic example path.
- Original signing credentials and signing files are **not** included. All passwords in the build configuration are dummy placeholders. Do not upload the original raw mobile ZIP or real signing keys.
- Changed the Flask entry-point defaults to `127.0.0.1` (localhost) and `debug=False`. No remote LAN client can access it without configuration changes.
- No GPS records, dashcam videos, license plates, photographs, account tokens, or public IP addresses were found in this archive at packaging time.

## Important limitations

The Flask endpoints do not authenticate users, validate data rigorously, or secure the footage. **Do not expose this server to the public internet.** The archived mobile app still contains permissive networking configuration; it is experimental source, not a hardened production mobile client.

The Pi paths and `PI_HOST` placeholder must be configured if testing on new hardware. Do not put secrets directly in Python/JS source; use an ignored environment file for future work. `.gitignore` does not remove anything that has already been committed.

Before publishing, double-check the uploaded directory contents and run GitHub's secret scanning where available. Rotate any real signing passwords that were reused outside this archive.

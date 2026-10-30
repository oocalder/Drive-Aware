# Portfolio — Project 01: Drive Aware

The supplied `portfolio.zip` has a Projects scene with three placeholder cards, implemented as `portfolioProjects` in `portfolio/js/portfolio.js`. Project 01 currently says `Client work`, even though this was a **personal prototype**. Replace just its first entry after you have published the repository; keep the portfolio repository separate from Drive Aware.

## Recommended compact card

**Title:** Drive Aware / IoT & Backend  
**Summary:** A Raspberry Pi and Flask prototype for browsing dashcam footage and logging motion data, with explored integrations for phone sensors and automated alerts.  
**Role:** Personal project — system design, Python backend, integration troubleshooting  
**Tools:** Raspberry Pi, Python, Flask, HTTP/JSON, HTML, Cordova (experimental)  
**Outcome:** Demonstrated local video access and test motion logging; documented hardware and Android integration limitations.

### Ready-to-edit data entry

Paste the following in the **first object** of the `portfolioProjects` array in `portfolio/js/portfolio.js`. Keep `sourceUrl` empty until the public repository exists.

```js
{
  title: "Project 01 / Drive Aware",
  summary: "Raspberry Pi + Flask prototype for dashcam video access and JSON motion logging, with experimental phone-sensor and notification integrations.",
  role: "Personal project / system design, Python backend, and troubleshooting",
  tools: "Raspberry Pi · Python · Flask · HTTP/JSON · HTML · Cordova (prototype)",
  outcome: "Demonstrated local video playback and test motion logging; documented integration gaps and next steps.",
  image: "", // Add your OWN clean screenshot later; no placeholder demo claimed.
  liveUrl: "", // No public live deployment exists.
  sourceUrl: "", // Set to GitHub repository URL after publishing.
},
```

**One additional website edit:** the Projects animation in your current `portfolio/js/portfolio.js` has a separate hard-coded info label (`STATUS Live`, near the Projects drawing code). Change that label to `STATUS Prototype` for this project; updating the first `portfolioProjects` object alone will not correct it.

## What the project detail page should emphasize

Present **one engineering case study**, not a sales pitch for a finished vehicle safety product:

1. **Problem / goal:** dashcam recordings live on an SD card and are difficult to correlate with event metadata.
2. **Architecture:** consumer camera → accessible recordings → Pi Flask service → local browser and JSON logs.
3. **Evidence:** one cropped screenshot of the Flask video page, one short code excerpt explaining `/motion`, and an example JSON record. The historical PDF has evidence screenshots, but confirm they are appropriate for public redistribution.
4. **Decision:** pivoted from a phone-based collision detector toward the camera's existing event recording capability after discovering hardware access limitations.
5. **Troubleshooting:** separate HTTP endpoint validation with `curl` from broken Cordova networking.
6. **Next phase:** unify watcher and video paths; then add dashboard timeline; mobile telemetry and Alexa are lower-priority integrations.

## Suggested one-minute interview explanation

> I built Drive Aware to see whether I could put consumer dashcam footage and motion records behind one local interface. I used a Raspberry Pi as the server and Flask to list videos, serve recordings, and accept motion samples as JSON. I validated the backend with curl and confirmed local video browsing, then explored an Android accelerometer app and file-watching automation. Those integrations exposed real limitations, including Cordova network restrictions and the dashcam's closed wireless interface. Rather than claim a finished collision detector, I documented the working services and the boundaries between them. The next improvement would be consistent event IDs linking camera files to backend records.

## Evidence to collect if revisiting the Pi later

- Screenshot of the server listing your actual sample/test footage without revealing personal locations or other people's faces.
- Screenshot or brief screen recording showing a local `curl` call returning success, then the log endpoint containing the record.
- A simple diagram or short flow animation showing implemented vs proposed components (clearly labeled).
- Optional mobile UI capture with an explicit **experimental** caption.

## Career positioning

**For implementation or application support:** emphasize requirements, integration discovery, root-cause investigation, test inputs/outputs, file-system dependencies, and documentation.

**For development:** emphasize route behavior, JSON handling, Jinja template rendering, edge-device integration, and clearly explain planned corrections to hard-coded configuration, authentication and persistence. Do not represent this as production-quality or a comprehensively tested application.

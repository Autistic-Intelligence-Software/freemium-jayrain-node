# FreeMium JayRain — audio node bundle

Everything you need to run your own FreeMium JayRain audio node, in one download.

## Quick start

1. **Download** the latest `freemium-node.zip` from
   [Releases](../../releases/latest) (or the
   [direct link](../../releases/latest/download/freemium-node.zip)).
2. **Install Java 17+** if you don't have it: https://adoptium.net
3. **Unzip** anywhere, then run the launcher:
   - Windows: double-click `start-node.bat`
   - Mac/Linux: run `start-node.sh`
4. On first run it asks you to **choose a node password**. Keep the window open.
5. **Make it reachable** (the bot runs in the cloud):
   - Easy: free tunnel at https://playit.gg (TCP tunnel for port 2333), or
   - Advanced: forward port 2333 (TCP) on your router to this PC.
6. **Link it**: dashboard → https://freemiumjayrain.rivaleclipse.dev/setup-wizard
   (or `/mynode` in Discord) with your public address + password.

While this PC is online, every server you're in gets music. 🎵

## What's in the bundle

| File | What it is |
|---|---|
| `Lavalink.jar` | The audio server (v4) |
| `plugins/` | YouTube + LavaSrc plugins (Spotify, Apple Music, Tidal, yt-dlp) |
| `application.yml` | Pre-tuned config — opus quality 7, low resampling, lean sources |
| `start-node.bat` / `start-node.sh` | Launchers — first run sets your password automatically |
| `README.txt` | The 5-step version of this guide |

## Keeping it fresh

A scheduled GitHub Action rebuilds this bundle every Monday from the latest
upstream Lavalink + plugin releases and publishes a new Release automatically.
The `releases/latest/download` link always serves the newest bundle — no link
changes needed anywhere.

## For developers

- `bundle/` — the static files packed into the zip
- `scripts/build_bundle.py` — assembles the zip (`--out dist/`)
- `.github/workflows/build-release.yml` — weekly rebuild + release automation
- `versions.json` — last-built upstream versions (updated by the workflow)

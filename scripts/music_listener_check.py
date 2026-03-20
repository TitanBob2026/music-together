#!/usr/bin/env python3
"""
music_listener_check.py — Unraid Bob's music listener state checker.
Called every 15s by a dedicated cron job (agentTurn).
Outputs one of:
  NO_CHANGE         — track hasn't changed
  SESSION_ENDED     — server returned 404 (stale) or session is over
  NEW_TRACK:<json>  — track changed, JSON contains track info for analysis

Pulls now_playing.json directly from TITAN's HTTP server (port 18791).
No node invoke, no SMB — pure HTTP.
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

WORKSPACE = "/mnt/plex/bob/workspace"
NOW_PLAYING = os.path.join(WORKSPACE, "music_together", "now_playing.json")
STATE_FILE  = os.path.join(WORKSPACE, "music_together", "music_listener_state.json")
STALE_SECONDS = 600  # 10 minutes
NOW_PLAYING_SERVER = "http://192.168.178.32:18791/"

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def main():
    # Pull fresh now_playing.json from TITAN's HTTP server
    try:
        with urllib.request.urlopen(NOW_PLAYING_SERVER, timeout=5) as resp:
            if resp.status == 404:
                # Server returned 404 = session ended (stale data)
                print("SESSION_ENDED")
                return
            raw = resp.read().decode("utf-8")
            now_playing = json.loads(raw)
            # Write to local file for reference
            with open(NOW_PLAYING, "w", encoding="utf-8") as f:
                f.write(raw)
    except urllib.error.URLError:
        # Server unreachable — fall back to local file if it exists
        now_playing = load_json(NOW_PLAYING)
        if not now_playing:
            print("NO_CHANGE")
            return
    except Exception:
        print("NO_CHANGE")
        return

    # Compare to last known state
    state = load_json(STATE_FILE) or {}
    last_index = state.get("last_playlist_index", -1)
    current_index = now_playing.get("playlist_index", -1)

    if current_index == last_index:
        print("NO_CHANGE")
        return

    # Track changed — update state and report
    state["last_playlist_index"] = current_index
    save_json(STATE_FILE, state)

    track_info = {
        "track_name": now_playing.get("track_name"),
        "album": now_playing.get("album"),
        "current_file": now_playing.get("current_file"),
        "playlist_index": current_index,
        "playlist_count": now_playing.get("playlist_count"),
    }
    print(f"NEW_TRACK:{json.dumps(track_info)}")

if __name__ == "__main__":
    main()

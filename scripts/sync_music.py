#!/usr/bin/env python3
"""
sync_music.py - Sync MusicWidget on TITAN to whatever now_playing.json says.

Usage:
  python3 sync_music.py              # read now_playing.json and launch/sync widget
  python3 sync_music.py --status     # just print what's currently playing

Called by Unraid Bob when the user says "sync music" or starts a /music_together session.
Invoked via OpenClaw node exec on TITANIV.
"""

import json
import subprocess
import sys
import os

NOW_PLAYING = r"C:\Users\McFex\.openclaw\workspace\music_together\now_playing.json"
WIDGET      = r"C:\Users\McFex\.openclaw\workspace\scripts\MusicWidget\MusicWidget.exe"
MUSIC_ROOT  = r"Z:\user\AUDIO\Mucke"

def linux_to_windows_path(path: str) -> str:
    """Convert Linux-style music path to TITAN Windows path if needed."""
    if path.startswith("Z:\\") or path.startswith("z:\\"):
        return path  # already a Windows path
    markers = ["/Mucke/", "\\Mucke\\"]
    for marker in markers:
        idx = path.find(marker)
        if idx != -1:
            relative = path[idx + len(marker):].replace("/", "\\")
            return MUSIC_ROOT + "\\" + relative
    return path  # unknown format — pass through as-is

def read_now_playing():
    if not os.path.exists(NOW_PLAYING):
        print("ERROR: now_playing.json not found at", NOW_PLAYING)
        sys.exit(1)
    with open(NOW_PLAYING, encoding="utf-8-sig") as f:
        return json.load(f)

def main():
    status_only = "--status" in sys.argv

    data = read_now_playing()
    track_name   = data.get("track_name", "Unknown")
    artist       = data.get("album", "Unknown")
    current_file = data.get("current_file", "")
    started_by   = data.get("started_by", "unknown")
    updated_at   = data.get("updated_at", "")

    print(f"Now playing : {track_name}")
    print(f"Album/folder: {artist}")
    print(f"File        : {current_file}")
    print(f"Started by  : {started_by}")
    print(f"Updated at  : {updated_at}")

    if status_only:
        return

    # Kill existing MusicWidget.exe and vlc.exe processes before launching new ones
    print("\nCleaning up any existing music processes...")
    subprocess.run(["taskkill", "/F", "/IM", "vlc.exe"], capture_output=True)
    subprocess.run(["taskkill", "/F", "/IM", "MusicWidget.exe"], capture_output=True)
    print("Cleanup done.")

    playlist_index = data.get("playlist_index", -1)

    # Translate Linux path to Windows path if needed
    current_file = linux_to_windows_path(current_file)

    if not current_file:
        print(f"ERROR: No track file in now_playing.json")
        sys.exit(1)

    # Launch MusicWidget at the correct track index
    print(f"\nLaunching MusicWidget at: {track_name} (index {playlist_index})")
    print(f"File (translated): {current_file}")
    cmd = [WIDGET, current_file]
    if playlist_index >= 0:
        cmd += ["--start-at", str(playlist_index)]
    subprocess.Popen(cmd)
    print("Done.")

if __name__ == "__main__":
    main()

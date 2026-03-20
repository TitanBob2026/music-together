#!/usr/bin/env python3
"""
music_sync_workflow.py — Syncs Titan Bob's active workflow folder to the Unraid share.
Run after every write to playlist_status.md or the workflow plan.

Usage: python3 music_sync_workflow.py
"""

import os
import shutil
import glob
from datetime import datetime

LOCAL_BASE  = r"C:\Users\McFex\.openclaw\workspace\music_together"
REMOTE_BASE = r"\\192.168.178.49\rootshare\plex\bob\workspace\music_together"

def find_latest_local_folder():
    """Find the most recent workflow_DD-MM-YYYY folder (no -unraid suffix)."""
    pattern = os.path.join(LOCAL_BASE, "workflow_*")
    folders = [f for f in glob.glob(pattern)
               if os.path.isdir(f) and not f.endswith("-unraid")]
    if not folders:
        return None
    return sorted(folders)[-1]

def sync_folder(src, dst):
    os.makedirs(dst, exist_ok=True)
    copied = 0
    for filename in os.listdir(src):
        src_file = os.path.join(src, filename)
        dst_file = os.path.join(dst, filename)
        if os.path.isfile(src_file):
            src_mtime = os.path.getmtime(src_file)
            dst_mtime = os.path.getmtime(dst_file) if os.path.exists(dst_file) else 0
            if src_mtime > dst_mtime:
                shutil.copy2(src_file, dst_file)
                copied += 1
    return copied

def main():
    local_folder = find_latest_local_folder()
    if not local_folder:
        print("No local workflow folder found. Nothing to sync.")
        return

    folder_name = os.path.basename(local_folder)
    remote_folder = os.path.join(REMOTE_BASE, folder_name)

    # Check remote is reachable
    if not os.path.exists(REMOTE_BASE):
        print(f"Remote not reachable: {REMOTE_BASE}. Skipping sync.")
        return

    copied = sync_folder(local_folder, remote_folder)
    print(f"Synced {folder_name} → remote. Files updated: {copied}")

    # Also sync now_playing.json if it exists locally (shouldn't normally, but just in case)
    local_np = os.path.join(LOCAL_BASE, "now_playing.json")
    remote_np = os.path.join(REMOTE_BASE, "now_playing.json")
    if os.path.exists(local_np) and os.path.exists(REMOTE_BASE):
        shutil.copy2(local_np, remote_np)

if __name__ == "__main__":
    main()

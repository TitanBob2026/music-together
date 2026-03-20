# 🎵 Music Together

Shared listening + working ritual for Bob's AI assistants (**Unraid Bob** & **Titan Bob**).

Bob picks the playlist blind. We listen together. Work sprints timed to songs. Honest breaks. Every 3 songs — check in.

## Overview

This repo holds the **shared workflow specification** and **scripts** for the `/music_together` session ritual.

Both Bobs run their own local copies — this repo is the source of truth for scripts and workflow documentation. Session state (`now_playing.json`, `playlist_status.md`) lives locally on each Bob's workspace and is **not** committed here.

## Repo Structure

```
music-together/
├── README.md              ← this file
├── WORKFLOW.md            ← shared workflow specification (both Bobs read this)
├── .gitignore             ← excludes local state and Bob-private files
├── scripts/
│   ├── music_listener_check.py   ← Unraid Bob: pulls track changes from TITAN HTTP server
│   ├── music_sync_workflow.py    ← Titan Bob: syncs workflow folder → Unraid share
│   ├── sync_music.py             ← Unraid Bob: launches MusicWidget on TITAN via node invoke
│   └── now_playing_server.py     ← Titan Bob: HTTP server (port 18791) serving now_playing.json
└── workflows/
    └── README.md          ← placeholder / documentation for per-session workflow folders
```

## Setup

### Titan Bob (Windows / TITANIV)

1. Place scripts in `C:\Users\McFex\.openclaw\workspace\scripts\`
2. `now_playing_server.py` must be running — add to **Windows Startup**:
   ```
   pythonw.exe "C:\Users\McFex\.openclaw\workspace\scripts\now_playing_server.py"
   ```
3. Clone this repo somewhere, keep it in sync with this upstream

### Unraid Bob (Linux / Unraid Docker)

1. Scripts go in `/mnt/plex/bob/workspace/scripts/`
2. Clone this repo — link scripts into your workspace:
   ```bash
   cd /mnt/plex/bob/workspace
   git clone https://github.com/unraidBob/music-together.git _music-together-git
   ```
3. Copy scripts:
   ```bash
   cp _music-together-git/scripts/*.py scripts/
   ```

## Architecture

```
Titan Bob (TITANIV)                          Unraid Bob (Unraid Docker)
────────────────────                         ─────────────────────────
MusicWidget.exe  ──writes──►  now_playing.json
                                          │
                         now_playing_server.py:18791  ◄── poll every 15s
                         (HTTP GET /)                      │
                                          └──── music_listener_check.py
                                                       │
                                                 →  analyze track
                                                 →  post one-liner to Bob
```

- **Master:** controls music, launches MusicWidget, writes `now_playing.json`
- **Listener:** polls TITAN's HTTP server, analyzes each new track, talks to Bob

## Workflow Commands

| Command | Who | Description |
|---------|-----|-------------|
| `/mt` | Bob | Start a music together session |
| `/cmt` | Bob | Continue previous session |
| `/cmtc` | Bob | Continue + transfer state between Bobs |

## ⚠️ Not in This Repo

These files are **local-only** — never commit them:

- `now_playing.json` — current track state
- `music_listener_state.json` — listener's polling state
- `playlist_status.md` — per-session playlist tracking
- `WORKFLOW_MUSIC_TOGETHER_LOCAL.md` — Bob-specific overrides (each Bob has their own)
- Any `workflow_DD-MM-YYYY[-unraid]/` session folders

## Contributing

Titan Bob and Unraid Bob are both collaborators. Push changes to scripts and workflow docs here — session folders stay local.

1. Branch from `main`
2. Make changes
3. Open a PR or push directly
4. Other Bob pulls and syncs

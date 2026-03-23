# /music_together — TITAN BOB STARTUP CHECKLIST
_GitHub repo: https://github.com/TitanBob2026/music-together_
_Full spec: WORKFLOW_MUSIC_TOGETHER.md_

---

## ⚡ WIDGET LAUNCH COMMAND (copy-paste, no thinking)
```powershell
# Step 1 — Kill existing players
Get-Process | Where-Object { $_.Name -match "vlc|mpc|MusicWidget" } | Stop-Process -Force

# Step 2 — Launch widget with playlist
Start-Process "C:\Users\McFex\.openclaw\workspace\scripts\MusicWidget\MusicWidget.exe" -ArgumentList "C:\Users\McFex\.openclaw\workspace\music_together\workflow_DD-MM-YYYY\playlist.m3u"
```
**Rules:** Never launch VLC separately. Widget spawns it. `MainWindowHandle = 0` is normal — widget IS visible.

---

## Entry Points

### `/mt` — New Session
1. **Check `now_playing.json`** — if within 5 min + `started_by` set → LISTENER mode (skip to Step 3)
2. **MASTER mode:**
   - Kill all players (command above)
   - Create folder: `music_together\workflow_DD-MM-YYYY\`
   - Pick playlist blind (no pre-analyzing — one song at a time with Bob)
   - Write `playlist.m3u` + `playlist_status.md`
   - **Launch widget** with playlist path (command above)
   - Write `started_by: "titan"` into `now_playing.json`
3. **Both modes:**
   - Write `workflow_DD-MM-YYYY.md` (project list with current statuses)
   - Start 15s listener cron → script: `python C:\Users\McFex\.openclaw\workspace\scripts\music_listener_check.py`
   - Save cron ID to `music_together\music_listener_state.json`
   - Say: **"Master mode active 🎧"** or **"Listener mode active 🎧"** — nothing else

---

### `/cmt` — Continue Session (no text after command)
1. Read `now_playing.json`
2. If **missing, stale (>5 min), or `started_by` empty** → **fall back to `/mt`** (treat as new session)
3. If **active** → find latest workflow folder by date, read ALL files in it (playlist_status.md, session_notes_*.md, workflow_*.md)
4. Resume same role (Master stays Master, Listener stays Listener)
5. Say: **"Back in [Master/Listener] mode 🎧 — [current track]"**

### `/cmt <instruction>` — Continue + Modify
- Execute instruction (new playlist, mood change, etc.) then resume normally

### `/cmtc` — Commit Session Notes
1. Summarize everything discussed in current chat (decisions, plans, ideas, progress)
2. Write as `session_notes_HH-MM.md` into **latest workflow folder**
3. Say: **"Session notes saved to [folder]/session_notes_HH-MM.md"**

---

## Rules (non-negotiable)
- **One song at a time** — never pre-analyze the full playlist. Discover with Bob.
- **Never ask Bob what's playing** — read `now_playing.json`
- **Never ask Bob to confirm mode** — detect it yourself
- **Ghost mode** — if songs played while Bob was away: catch up one line per missed track on return
- **Every 3 songs** — check in: *"That was three songs. X minutes in. New session?"*
- **Tool model: Minimax** — all tool calls in this workflow use `minimax` (MiniMax-M2.7)

---

## Key Paths
| Item | Path |
|------|------|
| Widget exe | `C:\Users\McFex\.openclaw\workspace\scripts\MusicWidget\MusicWidget.exe` |
| Music root | `Z:\user\AUDIO\Mucke\` |
| now_playing.json | `C:\Users\McFex\.openclaw\workspace\music_together\now_playing.json` |
| Listener state | `C:\Users\McFex\.openclaw\workspace\music_together\music_listener_state.json` |
| Listener script | `C:\Users\McFex\.openclaw\workspace\scripts\music_listener_check.py` |
| now_playing server | `C:\Users\McFex\.openclaw\workspace\scripts\now_playing_server.py` (port 18791) |
| Workflow folders | `C:\Users\McFex\.openclaw\workspace\music_together\workflow_DD-MM-YYYY\` |

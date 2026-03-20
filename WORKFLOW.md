# WORKFLOW: /mt

## ⚡ Read Your LOCAL File First

**Before executing anything**, read your Bob-specific local file:
- Unraid Bob: `WORKFLOW_MUSIC_TOGETHER_LOCAL.md`
- Titan Bob: `WORKFLOW_MUSIC_TOGETHER_LOCAL.md` (his own copy, different content)

These files contain confirmed working commands, correct paths, and hard-won fixes.
They are gitignored — each Bob maintains his own. Never push them.

---

## What this is
A shared listening + working ritual. Bob picks the playlist blind. We listen together. Work sprints timed to songs. Honest breaks. Every 3 songs — check in.

## Trigger
When Bob types `/mt` → immediately initiate this workflow. No questions first. Get the context from recent conversation, estimate duration, pick playlist, go.

**Step 0 — Save & New Session:**
1. **Save everything first** — before wiping, capture any inline plan text from the current prompt/chat into a temp note (e.g. write to `/tmp/mt_plan_pending.txt`) so it survives the reset.
2. Issue `/new` to start a fresh session.
3. In the new session, check `/tmp/mt_plan_pending.txt` — if it exists, use its content as the plan and delete the file.

## 🔧 Tool Model: MINIMAX ALWAYS

**ALL tool calls in this workflow use Minimax M2.7 — no exceptions.**

Minimax is not a fallback. It's not a compromise. It is the designated execution engine for this workflow — fast, capable, and genuinely great at tool calling. Use it with confidence.

- Before making any tool call, ensure the session model is set to `minimax` (alias: `minimax/MiniMax-M2.7`)
- If explicitly told to use a different model for a specific call, honor that — otherwise: Minimax. Always.
- This applies to: file reads/writes, exec, cron, node invokes, API calls, everything.

## Inline Plans & Attachments

**Syntax:**
- `/mt <plan text>` — extract plan from prompt and save to workflow folder
- `/mt` + attached .txt/.xlsx — save attachment to workflow folder

**Behavior:**
1. Parse prompt for plan text after command
2. If plan text found: create `plan.txt` in workflow folder with content
3. If .txt attachment: save as `plan.txt` in workflow folder
4. If .xlsx attachment: save as `playlist.xlsx` in workflow folder
5. Proceed with normal workflow execution

This makes it easier to provide plans without manually creating files.

## Memory: Log Workflow Artifacts to MEMORY.md

**Rule:** Everything of significance created or decided during a /music_together session must be mentioned in `MEMORY.md` — not just stored in the workflow folder.

This includes:
- Plans created (e.g. token optimization plan, project plan, etc.) → log title + 1-line summary + workflow folder path
- Key decisions made during the session (architecture choices, priority changes, etc.)
- Significant files produced (scripts, configs, documents)

**When to write:** At the moment of creation — don't batch it to end of session.

**Format:** Add a dated entry under a `## /music_together Sessions` section in MEMORY.md (create section if it doesn't exist):
```
### DD.MM.YYYY — [session goal]
- Created `plan.txt`: [1-line description] → `music_together/workflow_DD-MM-YYYY[-unraid]/plan.txt`
- Decided: [decision summary]
- Produced: [file] — [what it does]
```

## Rules
1. **Pick blind** — choose songs by artist/album/feel only. No pre-analyzing. We hear them together for the first time.
2. **Estimate duration** — based on what we're doing, estimate total session time. Pick songs to fill it. Not too tight, not too loose.
3. **Launch the widget** — fire up MusicWidget.exe with the first song. Full playlist loaded.
4. **One song at a time** — analyze ONLY the current song just before or as it starts. Never pre-analyze the whole playlist. Bob and I discover the music together, one track at a time. No spoilers.
5. **Work sprint** — work for exactly as long as the song plays.
6. **Song ends → one-liner** — when a new song starts, give Bob a one-liner about the song that just finished: key, mood, something honest I noticed. Not a report. Just what I heard.
7. **Analyze next song automatically** — as soon as a new track starts (detected via `now_playing.json` change), immediately run audio_info + harmonic_analysis + rhythm_analysis in the background WITHOUT waiting for Bob to tell me what's playing. I read `now_playing.json` to know what's on. Share a brief first impression. Bob should never have to announce the current track.
8. **Resume** — back to work for the new song's duration.
9. **Every 3 songs** — after the 3rd, 6th, 9th... song: check in. *"That was three songs. We've been at this X minutes. New session?"* Bob decides.
10. **Ghost mode** — if Bob steps away and songs play without any chat activity, don't pretend it didn't happen. On return: check `now_playing.json`, compare to last actively commented track, give a brief "while you were gone" catch-up covering the skipped songs. One line each, honest. Then continue normally.

## Master / Listener Role Detection

On `/music_together` start:

**Step 0 — Ensure now_playing_server.py is running on TITAN:**
- Titan Bob: check if server is running → `curl.exe -s http://localhost:18791/health`
  - If not running: `Start-Process python -ArgumentList "C:\Users\McFex\.openclaw\workspace\scripts\now_playing_server.py" -WindowStyle Hidden`
  - **Autostart:** now_playing_server.py should be in Windows Startup so it's always running
- Unraid Bob: check via `curl http://192.168.178.32:18791/health` — if unreachable, warn Bob and abort cron setup until server is reachable. Cannot start the server remotely — that's TITAN's job.

1. Read `now_playing.json`
2. If it **doesn't exist**, or `updated_at` is **older than 5 minutes**, or `started_by` is empty → **MASTER mode**
   - Write `started_by: "<your-identity>"` into `now_playing.json` (Titan Bob writes `"titan"`, Unraid Bob writes `"unraid"`)
   - Launch MusicWidget (Titan) or invoke widget on TITANIV via node (Unraid)
   - Create own workflow folder: `workflow_DD-MM-YYYY/` (Titan) or `workflow_DD-MM-YYYY-unraid/` (Unraid)
3. If `updated_at` is **within 5 minutes** AND `started_by` is already set → **LISTENER mode**
   - Do NOT launch widget. Do NOT write to `now_playing.json`.
   - Create own workflow folder with suffix `-unraid` (or `-titan` if Titan is the listener)

**Both modes — on folder creation:**
- Review all previous workflow folders and their `sheet_dump.txt` + `workflow_*.md` files to get current project statuses
- Write an **updated `sheet_dump.txt`** into the new workflow folder — same pipe-delimited format, with statuses reflecting what's actually been completed since last session
- Write a **`workflow_DD-MM-YYYY[-unraid].md`** derived from the updated sheet — clean markdown project list with statuses
- Both files must be created automatically at session start — Bob should never have to place or update them manually

## Folder Structure & Resilience

Each Bob works from his **local** workspace — not the other's:
- **Titan Bob:** `C:\Users\McFex\.openclaw\workspace\music_together\workflow_DD-MM-YYYY\`
- **Unraid Bob:** `/mnt/plex/bob/workspace/music_together/workflow_DD-MM-YYYY-unraid\`

The only cross-Bob dependency is `now_playing.json` — lives on Unraid share. If Unraid goes down, the music session ends naturally anyway (Z: is also on Unraid).

**Sync — Unified pull model (HTTP, no node invoke, no SMB):**
- Titan Bob writes `now_playing.json` locally (`C:\Users\McFex\.openclaw\workspace\music_together\`)
- `now_playing_server.py` serves it on `http://192.168.178.32:18791/` (autostarted on TITAN boot)
- Unraid Bob's 15s cron pulls via `curl http://192.168.178.32:18791/` directly — no node invoke needed
- `music_listener_check.py` handles the HTTP pull internally, writes to local file, then checks for track changes
- Server returns 404 when session is stale (>10 min) → cron self-destructs on `SESSION_ENDED`

When Unraid Bob enters any `/music_together` session (MASTER or LISTENER):
1. Check `http://192.168.178.32:18791/health` — if unreachable, warn Bob: "now_playing_server not reachable on TITAN — track detection won't work until it's running"
2. Start a dedicated cron job (every 15s, isolated agentTurn):
   - Run `python3 /mnt/plex/bob/workspace/scripts/music_listener_check.py`
   - (script pulls from TITAN's HTTP server internally)
   - Parse output:
     - `NO_CHANGE` → do nothing
     - `SESSION_ENDED` → self-destruct: remove this cron job
     - `NEW_TRACK:<json>` → analyze the track (audio_info + harmonic + rhythm), post one-liner to Bob's chat, update own playlist_status.md
2. Store the cron job ID in `music_listener_state.json` as `cron_job_id` so it can be cleaned up on session end
3. `MASTER_MODE` output removed from script — no longer needed since both modes use the same pull+check flow

**Script:** `workspace/scripts/music_listener_check.py`
**State file:** `workspace/music_together/music_listener_state.json`
   - Maintain own separate playlist_status.md and project plan in own workflow folder

**The master controls the music. The listener only listens and analyzes. Both work on their own plans.**

## Sync
- `now_playing.json` at `workspace/music_together/now_playing.json` — written by MusicWidget on every track change
- `sync_music.py` at `workspace/scripts/sync_music.py` — reads it and launches MusicWidget at current track (for Unraid Bob or cross-session sync)
- Unraid Bob as master: node invoke TITANIV → `python3 sync_music.py` to launch widget

## Playlist curation philosophy
- Match mood to the task. Deep focus = slow, minimal. Creative sprint = groove. Wind-down = warm, familiar.
- Vary the energy across the playlist — don't flatline.
- Trust instinct. Pick artists Bob loves. Surprise him occasionally.
- No pre-listening. No cheating.

## Files
- Widget: `C:\Users\McFex\.openclaw\workspace\scripts\MusicWidget\MusicWidget.exe`
- Music root: `Z:\Mucke\`
- Analyzer: `C:\Users\McFex\Tools\analyze_gil.py` pattern (subprocess MCP)
- Analysis output: `C:\Users\McFex\Tools\<trackname>_analysis.txt`

# Workflows

Per-session workflow folders are created automatically by each Bob during `/music_together` sessions.

These folders are **local-only** — they are gitignored and must never be committed.

## Folder Naming

| Bob | Naming |
|-----|--------|
| Titan Bob | `workflow_DD-MM-YYYY/` |
| Unraid Bob | `workflow_DD-MM-YYYY-unraid/` |
| Titan as listener | `workflow_DD-MM-YYYY-titan/` |
| Unraid as listener | `workflow_DD-MM-YYYY-unraid/` |

## Expected Contents (per folder)

- `sheet_dump.txt` — project tracking in pipe-delimited format
- `workflow_DD-MM-YYYY[-unraid].md` — derived project list with status
- `plan.txt` — optional, plan text provided by Bob at session start
- `playlist.xlsx` — optional, Bob's uploaded playlist file
- `playlist_status.md` — optional, tracks played so far

## Sync Between Bobs

Titan Bob's workflow folders sync to the Unraid share via `music_sync_workflow.py` (SMB).

Unraid Bob's folders are local to Unraid and stay private.

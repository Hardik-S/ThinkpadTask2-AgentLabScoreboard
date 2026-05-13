# Local Agent Lab Scoreboard - Codex Fix

This folder is the repaired, portfolio-visible copy of the raw Qwen worker
artifact. The raw worker output is preserved unchanged in
`state/raw-agent-lab-scoreboard/`.

## Why this repair exists

The 24-turn Qwen phase completed all turns, but the final raw artifact was not a
working static dashboard:

- `data/scoreboard.json` did not parse as JSON.
- `app.js` was wrapped in Markdown fences and failed `node --check`.
- `scripts/validate-static-site.js` was also fenced and failed `node --check`.
- The raw HTML and CSS were useful directionally but not publication-ready.

Codex repaired only this copied folder. The repaired version keeps the failure
history visible and does not overwrite raw evidence.

## Verification

Run from this folder:

```powershell
node --check app.js
node scripts\validate-static-site.js
python -m json.tool data\scoreboard.json
```

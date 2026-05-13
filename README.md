# Local Agent Lab Scoreboard

This repository contains a supervised local-worker experiment and the repaired
static dashboard that came out of it.

The goal was to use local `qwen2.5-coder:3b` through direct Ollama HTTP to build
a portfolio-visible dashboard comparing local and agent workflows. The dashboard
starts with evidence from `Thinkpad24TurnsTest` and is structured so future
models and runs can be added later.

## Folder map

- `state/` preserves raw worker evidence: prompts, responses, progress JSON,
  block snapshots, and the final raw Qwen project.
- `state/raw-agent-lab-scoreboard/` is the frozen raw artifact. It is broken and
  intentionally left untouched.
- `codex-fix/` is the repaired, portfolio-visible static dashboard.
- `docs/` contains staged findings and the final report.
- `scripts/scoreboard_worker_controller.py` is the tiny direct-Ollama controller
  used for the 24-turn worker phase.

## What happened

Qwen completed all 24 turns without a timeout after the requested model was
pulled into the local Ollama registry. Completion did not mean publication
quality: the raw JSON failed parsing, and the generated JavaScript files were
wrapped in Markdown fences. Codex therefore created `codex-fix/` after the raw
phase and repaired only that copy.

## Run the repaired dashboard

Open `codex-fix/index.html` directly, or serve the folder:

```powershell
cd codex-fix
python -m http.server 49312 --bind 127.0.0.1
```

## Verify

```powershell
node --check codex-fix\app.js
node codex-fix\scripts\validate-static-site.js
python -m json.tool codex-fix\data\scoreboard.json
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\scripts\codex-public-redaction-scan.ps1" -Path codex-fix
```

Raw validation failures are documented in `docs/FINAL_REPORT.md`; they are part
of the evidence, not something to hide.

"""Run the raw 24-turn Qwen worker phase for Local Agent Lab Scoreboard.

This controller is intentionally small and conservative. It calls Ollama's
direct HTTP API, stores every prompt and raw response under state/, and writes
the response text directly to the requested raw project file. It does not strip
Markdown fences, repair invalid JSON, or otherwise improve Qwen output. Codex
repair, if needed, belongs only in codex-fix/ after all 24 turns are complete.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import time
import urllib.error
import urllib.request
import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
RUNS = STATE / "runs"
RAW_PROJECT = STATE / "raw-agent-lab-scoreboard"
SNAPSHOTS = STATE / "block-snapshots"
DOCS = ROOT / "docs"

MODEL = "qwen2.5-coder:3b"
API_URL = "http://127.0.0.1:11434/api/generate"
TIMEOUT_SECONDS = 300

TASK1_FACTS = """Task 1 evidence to seed scoreboard:
- Prior project: Thinkpad24TurnsTest / ThinkPad Build Observatory.
- Worker/model: ThinkPad e530 running local qwen2.5-coder:3b through direct Ollama HTTP.
- Turn budget: 24 turns, max 5 minutes each.
- Outcome: 24 attempted, 16 completed, 8 failed or timed out.
- Strong prompt shape: direct-file and micro-markdown prompts.
- Weak prompt shape: broad JSON envelopes, larger source/context dumps, and multi-file turns.
- Raw artifact quality: useful docs and partial static assets, but not publication-ready.
- Codex repair burden: high; repaired JavaScript, data truthfulness, validator script, and presentation layer in codex-fix/.
- Validation issue: raw validator script was Markdown-fenced and failed node --check.
- Recommendation: use local Qwen for docs, schemas, run logs, narrow static assets, and cheap exploratory implementation; keep Codex responsible for final verification and publication.
"""


TURNS = [
    (1, "README", "README.md", "Write the raw project README for Local Agent Lab Scoreboard. Explain the raw Qwen boundary, offline static dashboard purpose, Task 1 seed evidence, and future extensibility. Markdown only."),
    (2, "Data schema", "docs/data-schema.md", "Define the scoreboard data schema. Include fields for worker/model name, task attempted, turns attempted, completed turns, timeout/failure rate, raw artifact quality, Codex repair burden, validation status, token/cost estimate, lessons learned, and recommended use cases. Markdown only."),
    (3, "Seed scoreboard data", "data/scoreboard.json", "Write valid JSON only. Create an array with one run record for Task 1 using the provided facts. Include room for future runs. No prose, no fences."),
    (4, "Dashboard content plan", "docs/dashboard-content-plan.md", "Write a concise content plan for the static dashboard sections and reviewer story. Markdown only."),
    (5, "File manifest", "docs/file-manifest.md", "Write a file manifest with purpose and ownership for every expected raw project file. Markdown only."),
    (6, "Validation plan", "docs/validation-plan.md", "Write a validation plan for syntax, JSON parsing, redaction, accessibility, and browser smoke checks. Markdown only."),
    (7, "HTML shell", "index.html", "Write complete index.html for an offline static dashboard. Link styles.css and app.js. Use semantic regions and accessible headings. No external assets, no CDN, no network calls."),
    (8, "CSS base", "styles.css", "Write complete styles.css for a polished responsive static dashboard. Use restrained professional dashboard styling, stable table layout, readable cards, and no external assets."),
    (9, "JavaScript skeleton", "app.js", "Write complete app.js skeleton that loads local scoreboard data from an embedded fallback constant first. Include functions for rendering table, metrics, cards, lessons, estimates, and states. No network calls."),
    (10, "Render table", "app.js", "Rewrite complete app.js to render a scoreboard table from embedded Task 1 data. Keep functions small. No external dependencies."),
    (11, "Render summary metrics", "app.js", "Rewrite complete app.js to add summary metrics for attempts, completed turns, failure rate, repair burden, and validation status. Preserve table rendering."),
    (12, "Accessibility notes", "docs/accessibility-notes.md", "Write accessibility notes for the dashboard: landmarks, heading order, table captions, focus states, contrast, and empty states. Markdown only."),
    (13, "Comparison cards", "app.js", "Rewrite complete app.js to add comparison cards for workflow strengths, weaknesses, best prompt shape, and future-use fit. Preserve existing rendering behavior."),
    (14, "Lessons section", "app.js", "Rewrite complete app.js to add a lessons learned section from the Task 1 evidence. Preserve existing rendering behavior."),
    (15, "Token cost estimate", "app.js", "Rewrite complete app.js to add token and cost estimate rendering. Use honest approximate fields and mark unknown values clearly. Preserve existing rendering behavior."),
    (16, "Empty and error states", "app.js", "Rewrite complete app.js with empty and malformed-data handling. Make missing future runs clear without hiding Task 1 evidence."),
    (17, "Static validator", "scripts/validate-static-site.js", "Write complete CommonJS validator. Check required files, parse data/scoreboard.json, run node --check app.js, and scan project files for http://, https://, cdn, api_key, secret, password, token. No markdown fences."),
    (18, "Validation report", "docs/raw-validation-report.md", "Write a raw validation report template that says Codex must run it after turn 24. Do not claim checks passed yet. Markdown only."),
    (19, "Polish copy", "docs/turn-19-polish-copy.md", "Write concise copy polish recommendations for the current dashboard. Suggest exact wording, but do not edit runtime files in this turn. Markdown only under 500 words."),
    (20, "Responsive layout", "styles.css", "Rewrite complete styles.css with improved responsive layout for desktop and mobile. Preserve offline static constraints."),
    (21, "Final raw README update", "README.md", "Rewrite the README with final raw-worker status language. Keep raw boundary, future additions, validation expectations, and Codex repair boundary clear. Markdown only."),
    (22, "Handoff notes", "docs/handoff-to-codex.md", "Write final handoff notes for Codex. Include what exists, what might be broken, what to validate, and why raw output must remain frozen. Markdown only under 450 words."),
    (23, "Retrospective", "docs/qwen-retrospective.md", "Write a retrospective from the local Qwen worker perspective: what worked, what timed out risked, and how future controllers should prompt. Markdown only under 450 words."),
    (24, "Final raw validation attempt", "docs/final-raw-validation-attempt.md", "Write final raw validation attempt notes. Be honest that actual commands must be run by Codex after this worker phase. Markdown only under 450 words."),
]


def ensure_dirs() -> None:
    for path in (RUNS, RAW_PROJECT, SNAPSHOTS, DOCS):
        path.mkdir(parents=True, exist_ok=True)


def read_file_list() -> str:
    files = []
    for path in sorted(RAW_PROJECT.rglob("*")):
        if path.is_file():
            files.append(path.relative_to(RAW_PROJECT).as_posix())
    if not files:
        return "(no raw project files yet)"
    return "\n".join(f"- {item}" for item in files[-30:])


def known_raw_issues() -> str:
    progress_path = STATE / "progress.json"
    if not progress_path.exists():
        return "(none recorded yet)"
    try:
        progress = json.loads(progress_path.read_text(encoding="utf-8"))
    except Exception:
        return "progress.json could not be parsed by the controller"
    issues = []
    for item in progress.get("turns", []):
        for message in item.get("validation", []):
            if message.startswith("FAIL"):
                issues.append(f"- Turn {item['turn']} {item['target']}: {message}")
        if item.get("status") != "completed":
            issues.append(f"- Turn {item['turn']} {item['target']}: {item.get('error', 'worker failed')}")
    for path in sorted(RAW_PROJECT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".html", ".css", ".js", ".json"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lstrip()
        if text.startswith("```"):
            issues.append(f"- {path.relative_to(RAW_PROJECT).as_posix()}: starts with a Markdown fence; future turns should rewrite target files as direct file content")
    return "\n".join(issues[-10:]) if issues else "(none recorded yet)"


def format_issue_count() -> int:
    issues = 0
    progress_path = STATE / "progress.json"
    if progress_path.exists():
        try:
            progress = json.loads(progress_path.read_text(encoding="utf-8"))
            for item in progress.get("turns", []):
                issues += sum(1 for message in item.get("validation", []) if message.startswith("FAIL"))
        except Exception:
            issues += 1
    for path in sorted(RAW_PROJECT.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".html", ".css", ".js", ".json"}:
            if path.read_text(encoding="utf-8", errors="ignore").lstrip().startswith("```"):
                issues += 1
    return issues


def prompt_style(completed: int, failures: int) -> str:
    if format_issue_count() >= 2:
        return "micro-direct"
    if failures >= 2:
        return "micro-direct"
    if completed >= 12:
        return "direct-file"
    return "direct-file"


def build_prompt(turn: int, title: str, target: str, instruction: str, failures: int) -> str:
    style = prompt_style(turn - 1, failures)
    context = TASK1_FACTS
    if style == "micro-direct":
        context = "\n".join(TASK1_FACTS.splitlines()[:8])
    return f"""You are Qwen running locally as a small worker for a Codex-supervised experiment.
Project: Local Agent Lab Scoreboard.
Turn: {turn}/24.
Target file: {target}
Prompt shape: {style}

Hard rules:
- Produce only the full content for the target file.
- Do not wrap the answer in Markdown fences unless the target is a Markdown file and fences are part of that document.
- Do not modify more than this one target file.
- Do not include external URLs, CDN references, package installs, credentials, API keys, or private network details.
- Keep the result useful but compact.

{context}

Current raw project files:
{read_file_list()}

Known raw issues to account for without repairing previous files:
{known_raw_issues()}

Task:
{instruction}
"""


def call_model(prompt: str) -> tuple[str, float]:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 1800,
        },
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    start = time.monotonic()
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        body = response.read().decode("utf-8", errors="replace")
    elapsed = time.monotonic() - start
    parsed = json.loads(body)
    return parsed.get("response", ""), elapsed


def write_raw_target(target: str, content: str) -> None:
    output = RAW_PROJECT / target
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")


def validate_after_turn(target: str) -> list[str]:
    messages = []
    path = RAW_PROJECT / target
    if not path.exists():
        return [f"FAIL missing target {target}"]
    messages.append(f"PASS target exists {target}")
    if target.endswith(".json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
            messages.append(f"PASS json parses {target}")
        except Exception as exc:  # noqa: BLE001 - evidence capture, not repair
            messages.append(f"FAIL json parse {target}: {exc}")
    if target.endswith(".js"):
        try:
            subprocess.run(
                ["node", "--check", str(path)],
                cwd=str(ROOT),
                check=True,
                text=True,
                capture_output=True,
                timeout=30,
            )
            messages.append(f"PASS node --check {target}")
        except Exception as exc:  # noqa: BLE001 - evidence capture, not repair
            messages.append(f"FAIL node --check {target}: {exc}")
    return messages


def load_progress() -> dict:
    progress_path = STATE / "progress.json"
    if progress_path.exists():
        return json.loads(progress_path.read_text(encoding="utf-8"))
    return {
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": MODEL,
        "api_url": API_URL,
        "turn_timeout_seconds": TIMEOUT_SECONDS,
        "turns": [],
        "block_findings": [],
    }


def save_progress(progress: dict) -> None:
    (STATE / "progress.json").write_text(json.dumps(progress, indent=2), encoding="utf-8")


def snapshot_block(block_end: int) -> None:
    destination = SNAPSHOTS / f"after-turn-{block_end:02d}"
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(RAW_PROJECT, destination)


def write_block_findings(progress: dict, block_start: int, block_end: int) -> None:
    block_turns = [t for t in progress["turns"] if block_start <= t["turn"] <= block_end]
    completed = sum(1 for t in block_turns if t["status"] == "completed")
    failed = len(block_turns) - completed
    elapsed = sum(t.get("elapsed_seconds", 0) for t in block_turns)
    finding = {
        "block": f"{block_start}-{block_end}",
        "completed": completed,
        "failed": failed,
        "elapsed_seconds": round(elapsed, 2),
        "prompt_adjustment": "continue direct-file prompts" if failed < 2 else "switch or stay on micro-direct prompts",
    }
    progress["block_findings"].append(finding)
    lines = [
        f"# Turns {block_start}-{block_end} Findings",
        "",
        f"- Completed: {completed}",
        f"- Failed/timeouts: {failed}",
        f"- Total elapsed seconds: {elapsed:.2f}",
        f"- Prompt adjustment: {finding['prompt_adjustment']}",
        "",
        "## Turn Evidence",
        "",
        "| Turn | Target | Status | Elapsed | Notes |",
        "| ---: | --- | --- | ---: | --- |",
    ]
    for item in block_turns:
        notes = "; ".join(item.get("validation", [])) or item.get("error", "")
        lines.append(f"| {item['turn']} | `{item['target']}` | {item['status']} | {item.get('elapsed_seconds', 0):.2f}s | {notes} |")
    lines.extend([
        "",
        "## Boundary",
        "",
        "These findings describe raw Qwen output only. Codex has not repaired runtime files in this phase.",
        "",
    ])
    (DOCS / f"turns-{block_start:02d}-{block_end:02d}-findings.md").write_text("\n".join(lines), encoding="utf-8")
    snapshot_block(block_end)


def run(start_turn: int, end_turn: int) -> int:
    ensure_dirs()
    progress = load_progress()
    completed_turns = {item["turn"] for item in progress["turns"]}
    equivalent_failures = 0

    for turn, title, target, instruction in TURNS:
        if turn < start_turn or turn > end_turn:
            continue
        if turn in completed_turns:
            continue
        run_dir = RUNS / f"turn-{turn:02d}"
        run_dir.mkdir(parents=True, exist_ok=True)
        prompt = build_prompt(turn, title, target, instruction, equivalent_failures)
        (run_dir / "prompt.md").write_text(prompt, encoding="utf-8")
        record = {
            "turn": turn,
            "title": title,
            "target": target,
            "status": "failed",
            "elapsed_seconds": 0.0,
            "validation": [],
        }
        try:
            response, elapsed = call_model(prompt)
            (run_dir / "response.txt").write_text(response, encoding="utf-8")
            write_raw_target(target, response)
            validation = validate_after_turn(target)
            (run_dir / "validation.txt").write_text("\n".join(validation), encoding="utf-8")
            record.update(
                {
                    "status": "completed",
                    "elapsed_seconds": round(elapsed, 2),
                    "validation": validation,
                }
            )
            equivalent_failures = 0
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
            (run_dir / "error.txt").write_text(repr(exc), encoding="utf-8")
            (run_dir / "validation.txt").write_text(f"FAIL controller/model call: {exc}", encoding="utf-8")
            record["error"] = repr(exc)
            equivalent_failures += 1
        progress["turns"].append(record)
        save_progress(progress)
        if turn in (6, 12, 18, 24):
            write_block_findings(progress, turn - 5, turn)
            save_progress(progress)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a staged Qwen worker block.")
    parser.add_argument("--start", type=int, default=1, help="first turn to run")
    parser.add_argument("--end", type=int, default=24, help="last turn to run")
    args = parser.parse_args()
    raise SystemExit(run(args.start, args.end))

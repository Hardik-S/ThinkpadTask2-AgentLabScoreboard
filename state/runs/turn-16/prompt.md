You are Qwen running locally as a small worker for a Codex-supervised experiment.
Project: Local Agent Lab Scoreboard.
Turn: 16/24.
Target file: app.js
Prompt shape: micro-direct

Hard rules:
- Produce only the full content for the target file.
- Do not wrap the answer in Markdown fences unless the target is a Markdown file and fences are part of that document.
- Do not modify more than this one target file.
- Do not include external URLs, CDN references, package installs, credentials, API keys, or private network details.
- Keep the result useful but compact.

Task 1 evidence to seed scoreboard:
- Prior project: Thinkpad24TurnsTest / ThinkPad Build Observatory.
- Worker/model: ThinkPad e530 running local qwen2.5-coder:3b through direct Ollama HTTP.
- Turn budget: 24 turns, max 5 minutes each.
- Outcome: 24 attempted, 16 completed, 8 failed or timed out.
- Strong prompt shape: direct-file and micro-markdown prompts.
- Weak prompt shape: broad JSON envelopes, larger source/context dumps, and multi-file turns.
- Raw artifact quality: useful docs and partial static assets, but not publication-ready.

Current raw project files:
- app.js
- data/scoreboard.json
- docs/accessibility-notes.md
- docs/dashboard-content-plan.md
- docs/data-schema.md
- docs/file-manifest.md
- docs/validation-plan.md
- index.html
- README.md
- styles.css

Known raw issues to account for without repairing previous files:
- Turn 3 data/scoreboard.json: FAIL json parse data/scoreboard.json: Expecting value: line 1 column 1 (char 0)
- Turn 13 app.js: FAIL node --check app.js: Command '['node', '--check', 'C:\\Users\\hshre\\OneDrive\\Documents\\42 - Agents\\Codex\\April\\ProjectX\\ThinkpadTask2-AgentLabScoreboard\\state\\raw-agent-lab-scoreboard\\app.js']' returned non-zero exit status 1.
- Turn 14 app.js: FAIL node --check app.js: Command '['node', '--check', 'C:\\Users\\hshre\\OneDrive\\Documents\\42 - Agents\\Codex\\April\\ProjectX\\ThinkpadTask2-AgentLabScoreboard\\state\\raw-agent-lab-scoreboard\\app.js']' returned non-zero exit status 1.
- Turn 15 app.js: FAIL node --check app.js: Command '['node', '--check', 'C:\\Users\\hshre\\OneDrive\\Documents\\42 - Agents\\Codex\\April\\ProjectX\\ThinkpadTask2-AgentLabScoreboard\\state\\raw-agent-lab-scoreboard\\app.js']' returned non-zero exit status 1.
- app.js: starts with a Markdown fence; future turns should rewrite target files as direct file content
- data/scoreboard.json: starts with a Markdown fence; future turns should rewrite target files as direct file content
- index.html: starts with a Markdown fence; future turns should rewrite target files as direct file content
- styles.css: starts with a Markdown fence; future turns should rewrite target files as direct file content

Task:
Rewrite complete app.js with empty and malformed-data handling. Make missing future runs clear without hiding Task 1 evidence.

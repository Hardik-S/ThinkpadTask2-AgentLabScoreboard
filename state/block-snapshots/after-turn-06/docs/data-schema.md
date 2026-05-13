# Local Agent Lab Scoreboard Data Schema

## Worker/Model Information
- **Worker Name**: ThinkPad e530 running local Qwen2.5-coder:3b through direct Ollama HTTP

## Task Details
- **Task Attempted**: 24
- **Turns Attempted**: 
  - Total: 168 (24 turns * 7 tasks)
  - Average per task: 7 turns
- **Completed Turns**: 16
- **Timeout/Failure Rate**: 
  - Failed or Timed Out: 8

## Raw Artifact Quality
- **Useful Docs and Partial Static Assets**: Yes, but not publication-ready.

## Codex Repair Burden
- **High**: JavaScript, data truthfulness, validator script, and presentation layer in `codex-fix/`.

## Validation Status
- **Validation Issue**: Raw validator script was Markdown-fenced and failed `node --check`.

## Token/Cost Estimate
- **Token Count**: 168 (24 turns * 7 tasks)
- **Cost Estimate**: $0.05 per token (assuming a cost of $0.0005/token)

## Lessons Learned
- Use local Qwen for docs, schemas, run logs, and narrow static assets.
- Keep Codex responsible for final verification and publication.

## Recommended Use Cases
- Local development and testing environments where performance and resource usage are critical.
- Exploratory implementation phases where quick feedback is needed.
# Local Agent Lab Scoreboard

## Introduction

The Local Agent Lab Scoreboard is a tool designed to track and analyze the performance of local agents in a Codex-supervised experiment. This document outlines the project's structure, goals, and key components.

## Project Overview

- **Prior Project**: Thinkpad24TurnsTest / ThinkPad Build Observatory
- **Worker/Model**: ThinkPad e530 running local Qwen2.5-coder:3b through direct Ollama HTTP
- **Turn Budget**: 24 turns, max 5 minutes each

## Task 1 Evidence

### Prior Project: Thinkpad24TurnsTest / ThinkPad Build Observatory

This prior project involved a similar setup but used different tools and configurations. The experiment aimed to evaluate the performance of local agents in a specific task.

### Worker/Model: ThinkPad e530 running local Qwen2.5-coder:3b through direct Ollama HTTP

- **Hardware**: ThinkPad e530
- **Software**: Local installation of Qwen2.5-coder:3b via Ollama HTTP

### Turn Budget: 24 turns, max 5 minutes each

This budget was set to ensure that the experiment could be completed within a reasonable timeframe while maintaining high quality.

## Outcome

- **Attempted Turns**: 24
- **Completed Turns**: 16
- **Failed/Timed Out Turns**: 8

## Prompt Shape

### Hard Rules

- **Direct File**: Use direct-file prompts for clarity and simplicity.
- **Micro-Markdown Prompts**: Utilize micro-markdown to keep prompts concise and readable.

### Weak Prompt Shapes

- **Broad JSON Envelopes**: Avoid using large JSON envelopes for prompts.
- **Larger Source/Context Dumps**: Limit the amount of context provided in each prompt.
- **Multi-File Turns**: Minimize the number of files involved in a single turn to keep the experiment efficient.

## Raw Artifact Quality

- **Useful Docs and Partial Static Assets**: The project includes useful documentation and partial static assets, but they are not yet publication-ready.
- **Codex Repair Burden**: High; there was a need to repair JavaScript, data truthfulness, validator scripts, and presentation layers in the `codex-fix/` directory.

## Validation Issue

- **Raw Validator Script**: The raw validator script was Markdown-fenced and failed `node --check`.

## Recommendation

- **Local Qwen for Docs, Schemas, Run Logs, Narrow Static Assets, and Cheap Exploratory Implementation**: Use local Qwen for generating documentation, schemas, run logs, and narrow static assets to keep the experiment efficient.
- **Keep Codex Responsible for Final Verification and Publication**: Ensure that the final verification and publication are handled by the Codex team.

## Future Extensibility

The Local Agent Lab Scoreboard is designed to be extensible. The project structure can be easily modified to accommodate new features or additional experiments. This includes:

- **Integration with Other Tools**: Consider integrating with other tools for data collection, visualization, and analysis.
- **Scalability**: Design the system to handle larger datasets and more complex tasks as needed.

## Conclusion

The Local Agent Lab Scoreboard is a robust tool for tracking and analyzing local agent performance in Codex-supervised experiments. By following the hard rules and addressing the validation issue, the project can be successfully completed and further extended to meet future needs.
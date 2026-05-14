const runs = [
  {
    workerModel: "ThinkPad e530 / qwen2.5-coder:3b",
    taskAttempted: "Build ThinkPad Build Observatory over 24 supervised local-model turns.",
    turnsAttempted: 24,
    completedTurns: 16,
    failedOrTimedOutTurns: 8,
    timeoutFailureRate: 0.3333,
    rawArtifactQuality: "Useful docs and partial static assets; raw app not publication-ready.",
    codexRepairBurden: "High",
    validationStatus: "Raw failed; repaired artifact passed final checks.",
    tokenCostEstimate: "Local Ollama, no API billing. Token count not captured.",
    lessonsLearned: [
      "Direct-file Markdown and micro-prompts worked best.",
      "Large context and broad JSON envelopes increased failure risk.",
      "Publication needs a Codex-owned repair and verification boundary."
    ],
    recommendedFutureUseCases: ["Run logs", "Schema drafts", "First-pass docs", "Small static UI slices"]
  },
  {
    workerModel: "ThinkPad-local Ollama / qwen2.5-coder:3b",
    taskAttempted: "Build this Local Agent Lab Scoreboard seeded from the first run evidence.",
    turnsAttempted: 24,
    completedTurns: 24,
    failedOrTimedOutTurns: 0,
    timeoutFailureRate: 0,
    rawArtifactQuality: "All turns responded, but raw JSON and JavaScript were malformed or fenced.",
    codexRepairBurden: "High",
    validationStatus: "Raw failed JSON/JS checks; this codex-fix copy is repaired.",
    tokenCostEstimate: "Local Ollama, no API billing. About 59.9 minutes of worker wall time.",
    lessonsLearned: [
      "Completed turn count is not the same as usable artifact quality.",
      "Micro-direct prompts reduced context but did not eliminate code fencing.",
      "The scoreboard needs a separate format-failure field in future runs."
    ],
    recommendedFutureUseCases: ["Evidence dashboards", "Offline portfolio prototypes", "Workflow comparison tables"]
  }
];

const metricGrid = document.querySelector("#metric-grid");
const scoreboardBody = document.querySelector("#scoreboard-body");
const comparisonGrid = document.querySelector("#comparison-grid");
const lessonGrid = document.querySelector("#lesson-grid");
const validationList = document.querySelector("#validation-list");

function pct(value) {
  return `${Math.round(value * 100)}%`;
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function statusClass(text) {
  const lower = text.toLowerCase();
  if (lower.includes("passed")) return "status";
  if (lower.includes("failed")) return "status bad";
  return "status warn";
}

function renderMetrics() {
  const attempted = runs.reduce((sum, run) => sum + run.turnsAttempted, 0);
  const completed = runs.reduce((sum, run) => sum + run.completedTurns, 0);
  const failed = runs.reduce((sum, run) => sum + run.failedOrTimedOutTurns, 0);
  const repairHeavy = runs.filter((run) => run.codexRepairBurden.toLowerCase() === "high").length;
  const metrics = [
    ["Turns attempted", attempted],
    ["Completed turns", completed],
    ["Timeout/failure turns", failed],
    ["High-repair runs", repairHeavy]
  ];
  metricGrid.innerHTML = metrics.map(([label, value]) => `
    <article class="metric">
      <strong>${value}</strong>
      <span>${label}</span>
    </article>
  `).join("");
}

function renderTable() {
  scoreboardBody.innerHTML = runs.map((run) => `
    <tr>
      <td><strong>${escapeHtml(run.workerModel)}</strong></td>
      <td>${escapeHtml(run.taskAttempted)}</td>
      <td>${run.completedTurns}/${run.turnsAttempted}</td>
      <td>${pct(run.timeoutFailureRate)}</td>
      <td>${escapeHtml(run.rawArtifactQuality)}</td>
      <td>${escapeHtml(run.codexRepairBurden)}</td>
      <td><span class="${statusClass(run.validationStatus)}">${escapeHtml(run.validationStatus)}</span></td>
    </tr>
  `).join("");
}

function renderComparisons() {
  const cards = [
    ["Best worker fit", "Documentation, schemas, manifest drafting, and evidence-heavy static surfaces."],
    ["Weakest worker fit", "Executable JavaScript and strict JSON when the model tends to add Markdown fences."],
    ["Repair boundary", "Raw output stays under state/. Codex repairs only a copied artifact in codex-fix/."],
    ["Cost view", "No API billing, but local wall-clock time and final verification remain real costs."]
  ];
  comparisonGrid.innerHTML = cards.map(([title, body]) => `
    <article class="card">
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(body)}</p>
    </article>
  `).join("");
}

function renderLessons() {
  lessonGrid.innerHTML = runs.map((run) => `
    <article class="lesson">
      <h3>${escapeHtml(run.workerModel)}</h3>
      <ul>
        ${run.lessonsLearned.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
      </ul>
      <p><strong>Future use:</strong> ${escapeHtml(run.recommendedFutureUseCases.join(", "))}.</p>
      <p><strong>Cost estimate:</strong> ${escapeHtml(run.tokenCostEstimate)}</p>
    </article>
  `).join("");
}

function renderValidation() {
  const checks = [
    "Raw Qwen files preserved under state/raw-agent-lab-scoreboard/.",
    "Raw data/scoreboard.json failed JSON parsing.",
    "Raw app.js and raw validator failed node --check.",
    "codex-fix/data/scoreboard.json is valid JSON.",
    "codex-fix/app.js is browser-native and does not use network calls."
  ];
  validationList.innerHTML = checks.map((check) => `<li>${escapeHtml(check)}</li>`).join("");
}

function render() {
  if (!runs.length) {
    metricGrid.innerHTML = "<p>No runs are available yet.</p>";
    return;
  }
  renderMetrics();
  renderTable();
  renderComparisons();
  renderLessons();
  renderValidation();
}

render();

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const appPath = path.resolve(__dirname, "..", "app.js");
const appSource = fs.readFileSync(appPath, "utf8");

function createElement() {
  return {
    innerHTML: "",
    textContent: ""
  };
}

const elements = new Map([
  ["#metric-grid", createElement()],
  ["#scoreboard-body", createElement()],
  ["#comparison-grid", createElement()],
  ["#lesson-grid", createElement()],
  ["#validation-list", createElement()]
]);

const context = {
  document: {
    querySelector(selector) {
      const element = elements.get(selector);
      if (!element) {
        throw new Error(`Unexpected selector: ${selector}`);
      }
      return element;
    }
  }
};

vm.runInNewContext(`${appSource}
runs[0].workerModel = "<img src=x onerror=alert(1)>";
runs[0].taskAttempted = "Compare <worker> & Codex";
runs[0].lessonsLearned = ["Keep <raw> output observable"];
runs[0].recommendedFutureUseCases = ["Docs & schemas"];
renderTable();
renderLessons();
`, context, { filename: appPath });

const tableHtml = elements.get("#scoreboard-body").innerHTML;
const lessonHtml = elements.get("#lesson-grid").innerHTML;

function assert(condition, message) {
  if (!condition) {
    console.error(`FAIL ${message}`);
    process.exit(1);
  }
}

assert(!tableHtml.includes("<img src=x"), "table output must not contain raw injected tags");
assert(tableHtml.includes("&lt;img src=x onerror=alert(1)&gt;"), "table output should escape worker model text");
assert(tableHtml.includes("Compare &lt;worker&gt; &amp; Codex"), "table output should escape task text");
assert(lessonHtml.includes("Keep &lt;raw&gt; output observable"), "lesson list should escape lesson text");
assert(lessonHtml.includes("Docs &amp; schemas"), "future-use text should escape ampersands");

console.log("PASS app renderer escapes dynamic run text");

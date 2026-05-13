const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const root = path.resolve(__dirname, "..");
const required = [
  "index.html",
  "styles.css",
  "app.js",
  "data/scoreboard.json"
];

function fail(message) {
  console.error(`FAIL ${message}`);
  process.exitCode = 1;
}

function pass(message) {
  console.log(`PASS ${message}`);
}

for (const relative of required) {
  const file = path.join(root, relative);
  if (!fs.existsSync(file)) {
    fail(`missing ${relative}`);
  } else {
    pass(`found ${relative}`);
  }
}

try {
  const dataPath = path.join(root, "data", "scoreboard.json");
  const parsed = JSON.parse(fs.readFileSync(dataPath, "utf8"));
  if (!Array.isArray(parsed) || parsed.length < 1) {
    fail("scoreboard data must be a non-empty array");
  } else {
    pass("scoreboard data parses");
  }
} catch (error) {
  fail(`scoreboard JSON parse failed: ${error.message}`);
}

const syntax = spawnSync(process.execPath, ["--check", path.join(root, "app.js")], {
  encoding: "utf8"
});
if (syntax.status === 0) {
  pass("app.js syntax");
} else {
  fail(`app.js syntax: ${(syntax.stderr || syntax.stdout).trim()}`);
}

const disallowedExternal = /\b(?:https?:\/\/|cdn\.)/i;
const credentialPattern = new RegExp(
  "\\b(?:" + ["api[_-]?key", "password", "secret", "sk-[A-Za-z0-9]{20,}", "BEGIN (?:RSA|OPENSSH|PRIVATE)"].join("|") + ")",
  "i"
);
const offlineRuntimeFiles = new Set(["index.html", "styles.css", "app.js", path.join("data", "scoreboard.json")]);

function walk(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(full);
    } else if (/\.(html|css|js|json|md)$/i.test(entry.name)) {
      const text = fs.readFileSync(full, "utf8");
      const relative = path.relative(root, full);
      if (offlineRuntimeFiles.has(relative) && disallowedExternal.test(text)) fail(`external reference in ${relative}`);
      if (relative !== path.join("scripts", "validate-static-site.js") && credentialPattern.test(text)) {
        fail(`credential-shaped text in ${relative}`);
      }
    }
  }
}

walk(root);

if (!process.exitCode) {
  pass("static site validation complete");
}

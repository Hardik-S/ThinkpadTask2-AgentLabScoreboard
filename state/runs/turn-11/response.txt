```javascript
const { createServer } = require('http');
const fs = require('fs');

// Load scoreboard data from file
let scoreboardData = JSON.parse(fs.readFileSync('data/scoreboard.json', 'utf8'));

// Function to calculate summary metrics
function calculateSummaryMetrics() {
  const totalTurns = scoreboardData.totalTurns;
  const completedTurns = scoreboardData.completedTurns;
  const failedOrTimedOut = scoreboardData.failedOrTimedOut;

  const attemptRate = (completedTurns / totalTurns) * 100;
  const failureRate = ((totalTurns - completedTurns - failedOrTimedOut) / totalTurns) * 100;
  const repairBurden = scoreboardData.repairBurden;
  const validationStatus = scoreboardData.validationStatus;

  return {
    attemptRate,
    failureRate,
    repairBurden,
    validationStatus
  };
}

// Function to render summary metrics as a table
function renderSummaryTable(summaryMetrics) {
  return `
    <table>
      <thead>
        <tr>
          <th>Attempt Rate</th>
          <th>Failure Rate</th>
          <th>Repair Burden</th>
          <th>Validation Status</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>${summaryMetrics.attemptRate.toFixed(2)}%</td>
          <td>${summaryMetrics.failureRate.toFixed(2)}%</td>
          <td>${repairBurden}</td>
          <td>${validationStatus ? 'Passed' : 'Failed'}</td>
        </tr>
      </tbody>
    </table>
  `;
}

// Create an HTTP server to serve the summary table
const server = createServer((req, res) => {
  if (req.url === '/') {
    const summaryMetrics = calculateSummaryMetrics();
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(renderSummaryTable(summaryMetrics));
  } else {
    res.writeHead(404);
    res.end('Not Found');
  }
});

// Start the server
server.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```
```javascript
const fs = require('fs');
const path = require('path');

// Function to check if a file contains any sensitive information
function containsSensitiveInfo(fileContent) {
  const sensitiveKeywords = ['http://', 'https://', 'cdn', 'api_key', 'secret', 'password', 'token'];
  return sensitiveKeywords.some(keyword => fileContent.includes(keyword));
}

// Function to validate the static site
async function validateStaticSite() {
  try {
    // Check if all required files exist
    const requiredFiles = ['app.js', 'data/scoreboard.json', 'index.html', 'styles.css'];
    for (const file of requiredFiles) {
      const filePath = path.join(__dirname, file);
      if (!fs.existsSync(filePath)) {
        console.error(`File ${file} does not exist.`);
        return false;
      }
    }

    // Read and validate data/scoreboard.json
    const scoreboardPath = path.join(__dirname, 'data', 'scoreboard.json');
    let scoreboardContent = fs.readFileSync(scoreboardPath, 'utf8');
    if (containsSensitiveInfo(scoreboardContent)) {
      console.error('Data/scoreboard.json contains sensitive information.');
      return false;
    }

    // Run node --check app.js
    const checkCommand = `node --check ${path.join(__dirname, 'app.js')}`;
    const { stdout, stderr } = await new Promise((resolve, reject) => {
      child_process.exec(checkCommand, (error, stdout, stderr) => {
        if (error) {
          return reject(error);
        }
        resolve({ stdout, stderr });
      });
    });

    if (stderr.trim() !== '') {
      console.error(`node --check app.js failed with error: ${stderr}`);
      return false;
    }

    // Scan project files for http://, https://, cdn, api_key, secret, password, token
    const allFiles = [appPath, scoreboardPath, indexHtmlPath, stylesCssPath];
    for (const file of allFiles) {
      if (containsSensitiveInfo(fs.readFileSync(file, 'utf8'))) {
        console.error(`File ${file} contains sensitive information.`);
        return false;
      }
    }

    console.log('Static site validation passed.');
    return true;
  } catch (error) {
    console.error('Error during static site validation:', error);
    return false;
  }
}

// Run the validation
validateStaticSite();
```
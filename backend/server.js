/**
 * S.E.A.D.S. Legacy Bridge
 * This file allows you to run the Python backend using 'node server.js'
 */
const { spawn } = require('child_process');

console.log("\n" + "═".repeat(55));
console.log("   🤖 S.E.A.D.S.  Python Backend Bridge");
console.log("   (Running via Node.js for compatibility)");
console.log("═".repeat(55) + "\n");

const pythonProcess = spawn('python', ['-m', 'uvicorn', 'main:app', '--reload', '--port', '8000'], {
    stdio: 'inherit',
    shell: false
});

pythonProcess.on('error', (err) => {
    console.error('❌ Failed to start Python backend:', err);
    console.log('📝 Make sure Python and uvicorn are installed.');
});

pythonProcess.on('close', (code) => {
    if (code !== 0) {
        console.log(`\n⚠️  Python process exited with code ${code}`);
    }
});

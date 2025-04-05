import { createWebSocket, sendMessage } from './customWebSocket.js'

let currentInput = '';
let commandHistory = [];
let historyIndex = -1;
let cursorIndex = 0;

// Initialize WebSocket
createWebSocket()

// Initialize the terminal
const term = new Terminal({
    cols: 40,
    cursorBlink: true,
    rows: 20,
    lineWrap: true,
});

term.open(document.getElementById('terminal'));
term.focus();


term.write('Welcome to \x1b[94mBookify\x1B[0m \r\n// Enter Bookify commands here...\r\n// Examples: \r\nlistEvents()\r\nreserveTicket(\'Event Name\', \'Seat\', Date);')


const prompt = (label = 'Bookify', newline = true) => {
    if (newline) term.write('\r\n');
    term.write(`Enter your command \x1b[94m${label}\x1b[0m >> `);
};

prompt()

function redrawInput() {
    term.write('\x1b[?25l');
    // Clear current line and move cursor to beginning
    term.write('\x1b[2K\r');

    // Redraw prompt and input without newline
    prompt('Bookify', false); 
    term.write(currentInput);

    // Move cursor back to correct position
    const moveBack = currentInput.length - cursorIndex;
    if (moveBack > 0) {
        term.write(`\x1b[${moveBack}D`);
    }
    term.write('\x1b[?25h');
}

function loadHistory() {
    currentInput = commandHistory[historyIndex];
    cursorIndex = currentInput.length;
    redrawInput();
}

term.onData((data) => {

    switch (data) {
        case '\r':
            // Enter pressed
            const input = currentInput.trim();

            if (input !== '') {
                commandHistory.push(input);
                historyIndex = commandHistory.length;
            }

            if (input.toLowerCase() === "cls") {
                term.clear();
                term.focus();
            } else {
                console.log(input)
                sendMessage(input)
            }

            currentInput = '';
            cursorIndex = 0;
            prompt();
            break;
        case '\u007F': // backspace
            if (cursorIndex > 0) {
                currentInput =
                    currentInput.slice(0, cursorIndex - 1) +
                    currentInput.slice(cursorIndex);
                cursorIndex--;
                redrawInput();
            }
            break;
        case '\x1b[A': // Arrow Up
            if (historyIndex > 0) {
                historyIndex--;
                loadHistory();
            }
            break;
        case '\x1b[B': //Arrow down
            if (historyIndex < commandHistory.length - 1) {
                historyIndex++;
                loadHistory();
            } else {
                historyIndex = commandHistory.length;
                currentInput = '';
                cursorIndex = 0;
                redrawInput();
            }
            break;
        case '\x1b[D': // Left arrow
            if (cursorIndex > 0) {
                cursorIndex--;
                term.write('\x1b[D');
            }
            break;

        case '\x1b[C': // Right arrow
            if (cursorIndex < currentInput.length) {
                cursorIndex++;
                term.write('\x1b[C');
            }
            break;
        default:
            if (data >= ' ') { // printable characters
                currentInput =
                    currentInput.slice(0, cursorIndex) +
                    data +
                    currentInput.slice(cursorIndex);
                cursorIndex++;
                redrawInput();
            }
            break;
    }
});






import { createWebSocket, sendMessage } from './customWebSocket.js';

class TerminalManager {
    constructor() {
        this.currentInput = '';
        this.commandHistory = [];
        this.historyIndex = -1;
        this.cursorIndex = 0;
        this.initialized = false;

        this.initTerminal();
    }

    initTerminal() {
        try {
            // Initialize WebSocket
            createWebSocket();

            // Initialize the terminal
            this.term = new Terminal({
                cols: 80,  // Increased for better readability
                cursorBlink: true,
                rows: 24,  // Standard terminal size
                lineWrap: true,
                fontFamily: '"Courier New", monospace',
                theme: {
                    background: '#1e1e1e',
                    foreground: '#f0f0f0'
                }
            });

            this.term.open(document.getElementById('terminal'));
            this.term.focus();

            this.displayWelcomeMessage();
            this.prompt();

            this.setupEventListeners();
            this.initialized = true;
        } catch (error) {
            console.error('Terminal initialization failed:', error);
            // Fallback or error display logic could go here
        }
    }

    displayWelcomeMessage() {
        const welcomeMessage = [
            'Welcome to \x1b[94mBookify\x1B[0m',
            'Enter Bookify commands below:',
            'Examples:',
            '  listEvents()',
            '  reserveTicket(\'Event Name\', \'Seat\', Date);',
            '  help() for command list',
            ''
        ].join('\r\n');

        this.term.write(welcomeMessage);
    }

    prompt(label = 'Bookify', newline = true) {
        if (newline) this.term.write('\r\n');
        this.term.write(`\x1b[32m${label}\x1b[0m $ `);  // Changed to Unix-style prompt
    }

    redrawInput() {
        // Hide cursor during redraw to prevent flickering
        this.term.write('\x1b[?25l');

        // Move to start of line and clear it
        this.term.write('\r\x1b[K');

        // Redraw the prompt
        this.term.write(`\x1b[32mBookify\x1b[0m $ `);

        // Write the current input
        this.term.write(this.currentInput);

        // Position cursor correctly
        if (this.cursorIndex < this.currentInput.length) {
            // Move left N positions where N is remaining characters after cursor
            const moveLeft = this.currentInput.length - this.cursorIndex;
            this.term.write(`\x1b[${moveLeft}D`);
        } else if (this.cursorIndex > this.currentInput.length) {
            // Sanity check - shouldn't happen but protects against edge cases
            this.cursorIndex = this.currentInput.length;
        }

        // Show cursor again
        this.term.write('\x1b[?25h');
    }

    loadHistory() {
        this.currentInput = this.commandHistory[this.historyIndex] || '';
        this.cursorIndex = this.currentInput.length;
        this.redrawInput();
    }

    handleCommand(input) {
        input = input.trim();

        if (input === '') {
            this.prompt();
            return;
        }

        // Add to history if not duplicate of last command
        if (this.commandHistory[this.commandHistory.length - 1] !== input) {
            this.commandHistory.push(input);
        }
        this.historyIndex = this.commandHistory.length;

        // Handle special commands
        if (input.toLowerCase() === "clear" || input.toLowerCase() === "cls") {
            this.term.clear();
        } else if (input.toLowerCase() === "help") {
            this.displayHelp();
        } else {
            try {
                sendMessage(input);
            } catch (error) {
                this.term.write(`\r\n\x1b[31mError sending command: ${error.message}\x1b[0m\r\n`);
            }
        }

        this.currentInput = '';
        this.cursorIndex = 0;
        this.prompt();
    }

    displayHelp() {
        const helpText = [
            '\r\n\x1b[36mAvailable commands:\x1b[0m',
            '  listEvents() - Show available events',
            '  reserveTicket(name, seat, date) - Reserve a ticket',
            '  clear/cls - Clear the terminal',
            '  help - Show this help message',
            '\x1b[90mUse arrow keys for history navigation\x1b[0m\r\n'
        ].join('\r\n');

        this.term.write(helpText);
    }

    setupEventListeners() {
        this.term.onData((data) => {
            try {
                this.handleInput(data);
            } catch (error) {
                this.term.write(`\r\n\x1b[31mInput error: ${error.message}\x1b[0m\r\n`);
                this.prompt();
            }
        });

        // Optional: Handle resize events
        // window.addEventListener('resize', () => {
        //     this.term.fit();
        // });
    }

    handleInput(data) {
        switch (data) {
            case '\r': // Enter
            case '\n':
                this.handleCommand(this.currentInput);
                break;

            case '\u007F': // Backspace
                if (this.cursorIndex > 0) {
                    this.currentInput =
                        this.currentInput.slice(0, this.cursorIndex - 1) +
                        this.currentInput.slice(this.cursorIndex);
                    this.cursorIndex--;
                    this.redrawInput();
                }
                break;

            case '\x1b[A': // Up arrow
                if (this.historyIndex > 0) {
                    this.historyIndex--;
                    this.loadHistory();
                }
                break;

            case '\x1b[B': // Down arrow
                if (this.historyIndex < this.commandHistory.length - 1) {
                    this.historyIndex++;
                    this.loadHistory();
                } else {
                    this.historyIndex = this.commandHistory.length;
                    this.currentInput = '';
                    this.cursorIndex = 0;
                    this.redrawInput();
                }
                break;

            case '\x1b[D': // Left arrow
                if (this.cursorIndex > 0) {
                    this.cursorIndex--;
                    this.term.write('\x1b[D');
                }
                break;

            case '\x1b[C': // Right arrow
                if (this.cursorIndex < this.currentInput.length) {
                    this.cursorIndex++;
                    this.term.write('\x1b[C');
                }
                break;

            case '\x1b[3~': // Delete key
                if (this.cursorIndex < this.currentInput.length) {
                    this.currentInput =
                        this.currentInput.slice(0, this.cursorIndex) +
                        this.currentInput.slice(this.cursorIndex + 1);
                    this.redrawInput();
                }
                break;

            case '\x1b[H': // Home key
                this.cursorIndex = 0;
                this.term.write(`\x1b[${this.currentInput.length}D`);
                break;

            case '\x1b[F': // End key
                this.cursorIndex = this.currentInput.length;
                this.term.write(`\x1b[${this.currentInput.length - this.cursorIndex}C`);
                break;

            default:
                if (data >= ' ' && data <= '~') { // Printable ASCII characters
                    this.currentInput =
                        this.currentInput.slice(0, this.cursorIndex) +
                        data +
                        this.currentInput.slice(this.cursorIndex);
                    this.cursorIndex++;
                    this.redrawInput();
                }
                break;
        }
    }
}

// Initialize the terminal when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const terminalManager = new TerminalManager();
});
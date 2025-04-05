class ColorErrorPrinter {
    static COLORS = {
        RED: '\x1b[91m',
        GREEN: '\x1b[92m',
        YELLOW: '\x1b[93m',
        BLUE: '\x1b[94m',
        MAGENTA: '\x1b[95m',
        CYAN: '\x1b[96m',
        WHITE: '\x1b[97m',
        RESET: '\x1b[0m'
    };

    /**
     * Initialize the error printer with xterm.js Terminal instance
     * @param {Terminal} terminal - xterm.js Terminal instance
     * @param {boolean} [useColors=true] - Whether to use colored output
     */
    constructor(terminal, useColors = true) {
        this.terminal = terminal;
        this.useColors = useColors;
    }

    /**
     * Print an error message with optional coloring
     * @param {string} message - The error message to print
     * @param {string} [color] - Color name from COLORS dict
     * @param {string} [prefix='[ERROR]'] - Prefix for the message
     */
    printError(message, color = null, prefix = '[ERROR]') {
        let output = `${prefix} ${message}\r\n`;

        if (this.useColors && color && ColorErrorPrinter.COLORS[color]) {
            const colorCode = ColorErrorPrinter.COLORS[color];
            const resetCode = ColorErrorPrinter.COLORS.RESET;
            output = `\r\n${colorCode}${prefix} ${message}${resetCode}\r\n`;
        }

        this.terminal.write(output);
    }

    // Convenience methods
    critical(message) {
        this.printError(message, 'RED', '[CRITICAL]');
    }

    warning(message) {
        this.printError(message, 'YELLOW', '[WARNING]');
    }

    info(message) {
        this.printError(message, 'BLUE', '[INFO]');
    }

    success(message) {
        this.printError(message, 'GREEN', '[SUCCESS]');
    }
}

export default ColorErrorPrinter;
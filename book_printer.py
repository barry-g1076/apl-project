class ColorErrorPrinter:
    """
    A custom class for printing error messages with colored output in the console.

    Colors:
    - RED: For critical errors
    - YELLOW: For warnings
    - BLUE: For information
    - GREEN: For success messages
    - Default: For normal error messages
    """

    # ANSI color codes
    COLORS = {
        "RED": "\033[91m",
        "GREEN": "\033[92m",
        "YELLOW": "\033[93m",
        "BLUE": "\033[94m",
        "MAGENTA": "\033[95m",
        "CYAN": "\033[96m",
        "WHITE": "\033[97m",
        "RESET": "\033[0m",
    }

    def __init__(self, use_colors=True):
        """
        Initialize the error printer.

        Args:
            use_colors (bool): Whether to use colored output. Defaults to True.
        """
        self.use_colors = use_colors

    def print_error(self, message, color=None, prefix="[ERROR]"):
        """
        Print an error message with optional coloring.

        Args:
            message (str): The error message to print
            color (str, optional): Color name from COLORS dict. Defaults to None.
            prefix (str, optional): Prefix for the message. Defaults to "[ERROR]".
        """
        if self.use_colors and color and color in self.COLORS:
            color_code = self.COLORS[color]
            reset_code = self.COLORS["RESET"]
            print(f"{color_code}{prefix} {message}{reset_code}")
        else:
            print(f"{prefix} {message}")

    # Convenience methods for common error types
    def critical(self, message):
        """Print a critical error message in red."""
        self.print_error(message, color="RED", prefix="[CRITICAL]")

    def warning(self, message):
        """Print a warning message in yellow."""
        self.print_error(message, color="YELLOW", prefix="[WARNING]")

    def info(self, message):
        """Print an informational message in blue."""
        self.print_error(message, color="BLUE", prefix="[INFO]")

    def success(self, message):
        """Print a success message in green."""
        self.print_error(message, color="GREEN", prefix="[SUCCESS]")

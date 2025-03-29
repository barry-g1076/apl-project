import tkinter as tk
from tkinter import scrolledtext, messagebox
import book_lexer
import book_parser

class BookingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Booking Language Interpreter")
        self.root.geometry("500x450")
        self.root.configure(bg="#2C3E50")  # Dark background color

        # Styling
        self.font_style = ("Arial", 12)
        self.button_style = {"font": ("Arial", 10, "bold"), "bg": "#2980B9", "fg": "white", "bd": 3, "relief": "raised"}

        # Input Label
        self.input_label = tk.Label(root, text="Enter Booking Command:", font=self.font_style, bg="#2C3E50", fg="white")
        self.input_label.pack(pady=5)

        # Input Textbox
        self.input_text = scrolledtext.ScrolledText(root, height=4, width=50, font=self.font_style, bg="#ECF0F1")
        self.input_text.pack(pady=5)

        # Buttons
        button_frame = tk.Frame(root, bg="#2C3E50")
        button_frame.pack(pady=10)

        self.tokenize_button = tk.Button(button_frame, text="Tokenize", command=self.tokenize_text, **self.button_style)
        self.tokenize_button.grid(row=0, column=0, padx=5)

        self.parse_button = tk.Button(button_frame, text="Parse", command=self.parse_text, **self.button_style)
        self.parse_button.grid(row=0, column=1, padx=5)

        self.clear_button = tk.Button(button_frame, text="Clear", command=self.clear_text, **self.button_style)
        self.clear_button.grid(row=0, column=2, padx=5)

        # Output Label
        self.output_label = tk.Label(root, text="Output:", font=self.font_style, bg="#2C3E50", fg="white")
        self.output_label.pack(pady=5)

        # Output Textbox
        self.output_text = scrolledtext.ScrolledText(root, height=10, width=50, font=self.font_style, bg="#ECF0F1")
        self.output_text.pack(pady=5)

    def tokenize_text(self):
        """Runs the lexer and displays tokens."""
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Input Error", "Please enter a booking command.")
            return

        lexer = book_lexer.lexer
        lexer.input(text)
        tokens = [f"{tok.type}: {tok.value}" for tok in lexer]
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "\n".join(tokens))

    def parse_text(self):
        """Runs the parser and displays results."""
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Input Error", "Please enter a booking command.")
            return

        try:
            result = book_parser.parser.parse(text)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, str(result))
        except Exception as e:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"Parsing Error: {e}")

    def clear_text(self):
        """Clears the input and output fields."""
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookingGUI(root)
    root.mainloop()

class ErrorCollector:
    def __init__(self):
        self.reset()

    def reset(self):
        self.lex_errors = []
        self.parse_errors = []


error_collector = ErrorCollector()

import ply.lex as lex

# Reserved keywords
reserved = {
    "book": "BOOK",
    "status": "STATUS",
    "show": "SHOW",
    "fetch": "FETCH",
    "reserve": "RESERVE",
    "reservations": "RESERVATIONS",
    "list": "LIST",
    "pay": "PAY",
    "cancel": "CANCEL",
    "canceled": "CANCELED",
    "confirmed": "CONFIRMED",
    "for": "FOR",
    "on": "ON",
    "using": "USING",
    "of": "OF",
    "api": "API",
    "from": "FROM",
    "in": "IN",
    "tickets": "TICKETS",
    "available": "AVAILABLE",
    "events": "EVENTS",
    "paid": "PAID",
    "booking": "BOOKING",
    "bookings": "BOOKINGS",
    "all": "ALL",
}

    # "my": "MY",
    # "ticket": "TICKET",
    # "region": "REGION",
    # "select": "SELECT",
    # "read": "READ",
    # "by": "BY",
    # "out": "OUT",
    # "sort": "SORT",
    # "details": "DETAILS",
#    "event": "EVENT",
# Token list
tokens = [
    "NUMBER",
    "STRING",
    "BOOKING_ID",
    "PAYMENT_METHOD",
    "API_URL",
    "DATE",
    "ID",
    "EMAIL"
] + list(reserved.values())

    # "TICKET_ID",
# Lexer rules


# Ignore whitespace and newlines
t_ignore = " \t\n"

def t_EMAIL(t):
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return t

def t_API_URL(t):
    r"https?://[^\s]+"
    return t

def t_BOOKING_ID(t):
    r"booking_[a-zA-Z0-9_]+"
    return t


# def t_TICKET_ID(t):
#     r"ticket_[a-zA-Z0-9_]+"
#     return t


def t_PAYMENT_METHOD(t):
    r"CreditCard|PayPal|Crypto"
    return t


# Token rules for strings, numbers, and IDs
def t_DATE(t):
    r"\d{4}-\d{2}-\d{2}"
    return t


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.value = t.value.lower()
    t.type = reserved.get(t.value, "ID")  # Check for reserved words
    return t


def t_NUMBER(t):
    r"\d+\.\d+|\.\d+|\d+"  # Matches integers and floating-point numbers
    t.value = float(t.value) if "." in t.value else int(t.value)
    return t


def t_STRING(t):
    r'"[^"]+"|\'[^\']+\' '
    t.value = t.value.strip("\"'")  # Remove quotes if present
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    return None


# Error handling for lexer
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

if __name__ == "__main__":
    data = """
    BOOK 2 FOR "Coldplay Concert" ON "2025-07-15" FOR jack@gmail.com
    STATUS OF booking_12345
    SHOW available tickets FOR "Coldplay Concert"
    SHOW my reservations
    SELECT ticket_67890
    SORT tickets BY price
    FETCH tickets FROM API https://api.example.com
    RESERVE 3 FOR "Coldplay Concert" ON "2025-07-15"
    LIST all events
    PAY FOR booking_12345 USING CreditCard
    CANCEL booking_12345
    """
    lexer.input(data)
    for tok in lexer:
        print(tok)

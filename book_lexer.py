import ply.lex as lex


# List of token names
tokens = (
    "BOOK",
    "STATUS",
    "SHOW",
    "SELECT",
    "SORT",
    "FETCH",
    "READ",
    "RESERVE",
    "LIST",
    "PAY",
    "CANCEL",
    "API",
    "NUMBER",
    "DATE",
    "EVENT",
    "BOOKING_ID",
    "TICKET_ID",
    "REGION",
    "API_URL",
    "PAYMENT_METHOD",
    "FOR",
    "ON",
    "USING",
    "FROM",
    "IN",
    "TICKETS",
    "AVAILABLE",
    "BY",
    "PRICE",
    "EVENTS",
    "OUT",
    "MY",
    "BOOKING",
    "DETAILS",
)

# Regular expression rules for simple tokens
t_BOOK = r"BOOK"
t_STATUS = r"STATUS"
t_SHOW = r"SHOW"
t_SELECT = r"SELECT"
t_SORT = r"SORT"
t_FETCH = r"FETCH"
t_READ = r"READ"
t_RESERVE = r"RESERVE"
t_LIST = r"LIST"
t_PAY = r"PAY"
t_CANCEL = r"CANCEL"
t_API = r"API"
t_FOR = r"for"
t_ON = r"on"
t_USING = r"using"
t_FROM = r"from"
t_IN = r"in"
t_TICKETS = r"tickets"
t_AVAILABLE = r"AVAILABLE"
t_BY = r"BY"
t_PRICE = r"PRICE"
t_OUT = r"OUT"
t_MY = r"MY"
t_BOOKING = r"BOOKING"
t_DETAILS = r"DETAILS"


# Regular expressions for complex tokens
def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_DATE(t):
    r'"\d{4}-\d{2}-\d{2}"'
    t.value = t.value.strip('"')
    return t


def t_EVENT(t):
    r"\"[a-zA-Z0-9\s]+\" "
    t.value = t.value.strip('"')
    return t


def t_BOOKING_ID(t):
    r"\#\d+"
    return t


def t_TICKET_ID(t):
    r"\#\d+"
    return t


def t_REGION(t):
    r"\"[a-zA-Z\s]+\" "
    t.value = t.value.strip('"')
    return t


def t_API_URL(t):
    r"\"https?://[^\s]+\" "
    t.value = t.value.strip('"')
    return t


def t_PAYMENT_METHOD(t):
    r"CreditCard|PayPal|Crypto"
    return t


# Ignored characters (spaces, tabs, newlines)
t_ignore = " \t\n"


# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
def mylex(inp):
    lexer.input(inp)
    
    for token in lexer:
        print ("Token:", token)

# # Test the lexer
# if __name__ == "__main__":
#     data = 'BOOK 2 tickets for "Coldplay Concert" on "2025-07-15"'
#     lexer.input(data)
#     for tok in lexer:
#         print(tok)

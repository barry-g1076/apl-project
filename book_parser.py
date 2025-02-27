import ply.yacc as yacc
from book_lexer import tokens  # Import tokens from your lexer

# Parsing rules


# Symbol table to track ticket states
ticket_data = {
    "Coldplay Concert": {"available": 100, "reserved": 0, "confirmed": 0, "paid": 0},
}

# Start symbol
def p_statement(p):
    """statement : book_statement
    | status_statement
    | show_statement
    | select_statement
    | sort_statement
    | fetch_statement
    | reserve_statement
    | region_statement
    | speech_statement
    | list_statement
    | pay_statement
    | cancel_statement"""
    p[0] = p[1]  # Return the parsed result


# BOOK tickets
def p_book_statement(p):
    """book_statement : BOOK NUMBER TICKETS FOR EVENT ON DATE"""
    p[0] = f"Booking {p[2]} tickets for {p[5]} on {p[7]}"
    event = p[5].strip('"')
    num_tickets = int(p[2])

    if event not in ticket_data:
        print(f"Semantic Error: Event '{event}' does not exist.")
    elif num_tickets > ticket_data[event]["available"]:
        print(
            f"Semantic Error: Only {ticket_data[event]['available']} tickets left for {event}."
        )
    else:
        ticket_data[event]["available"] -= num_tickets
        ticket_data[event]["reserved"] += num_tickets
        print(f"Reserved {num_tickets} tickets for {event}.")


# STATUS of a booking
def p_status_statement(p):
    """status_statement : STATUS BOOKING_ID"""
    p[0] = f"Checking status of booking {p[2]}"


# SHOW available tickets
def p_show_statement(p):
    """show_statement : SHOW AVAILABLE TICKETS"""
    p[0] = "Displaying available tickets"


# SELECT ticket
def p_select_statement(p):
    """select_statement : SELECT TICKET_ID"""
    p[0] = f"Selecting ticket {p[2]}"


# SORT tickets by price
def p_sort_statement(p):
    """sort_statement : SORT TICKETS BY PRICE"""
    p[0] = "Sorting tickets by price"


# FETCH tickets from an API
def p_fetch_statement(p):
    """fetch_statement : FETCH TICKETS FROM API API_URL"""
    p[0] = f"Fetching tickets from API: {p[5]}"


# RESERVE tickets
def p_reserve_statement(p):
    """reserve_statement : RESERVE TICKETS FOR EVENT"""
    p[0] = f"Reserving tickets for {p[4]}"

# SHOW available tickets in a region
def p_region_statement(p):
    """region_statement : SHOW AVAILABLE TICKETS IN REGION"""
    p[0] = f"Displaying available tickets in {p[4]} region"


def p_speech_statement(p):
    """speech_statement : READ OUT MY BOOKING DETAILS
    | READ AVAILABLE TICKETS FOR EVENT"""
    if len(p) == 5:
        p[0] = "Reading out booking details"
    else:
        p[0] = f"Reading available tickets for {p[5]}"


# LIST events
def p_list_statement(p):
    """list_statement : LIST EVENTS"""
    p[0] = "Listing available events"


# PAY for a ticket
def p_pay_statement(p):
    """pay_statement : PAY BOOKING_ID USING PAYMENT_METHOD"""
    p[0] = f"Paying for {p[2]} using {p[4]}"


# CANCEL a booking
def p_cancel_statement(p):
    """cancel_statement : CANCEL BOOKING_ID"""
    p[0] = f"Cancelling booking {p[2]}"


# Error handling
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' on line {p.lineno}")
    else:
        print("Syntax error at EOF")


# Build the parser
parser = yacc.yacc()

# Test the parser
if __name__ == "__main__":
    while True:
        try:
            s = input("Enter command: ")
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(result)

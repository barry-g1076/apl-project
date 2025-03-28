import ply.yacc as yacc
import book_lexer
from semantic_analyzer import *
from utils import *
from testcode import data as testCode

tokens = book_lexer.tokens  # Import tokens from your lexer


# Todo: add a command to save data to file
# Todo: add a command to load data from file
# Todo: add a command to book with username
# Parser rules
def p_command(p):
    """command : booking
    | command booking
    | status
    | command status
    | view
    | command view
    | selection
    | command selection
    | sorting
    | command sorting
    | fetching
    | command fetching
    | region
    | command region
    | reservation
    | command reservation
    | listing
    | command listing
    | payment
    | command payment
    | dummy"""

    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


# Dummy rule to suppress the warning
def p_dummy(p):
    """dummy : ID"""
    pass  # Do nothing with this rule

def p_booking(p):
    """booking : BOOK NUMBER TICKETS FOR STRING ON DATE FOR EMAIL"""
    if isinstance(p[2], float):
        print(
            f"Warning: Fractional tickets ({p[2]}) are not allowed. Rounding to nearest integer."
        )
        p[2] = round(p[2])
    if not re.match(r"\d{4}-\d{2}-\d{2}", p[7]):
        print(f"Expected DATE in YYYY-MM-DD format but got '{p[7]}'")
    p[0] = ("booking", p[2], p[5], p[7], p[9])

# Error handling for booking
def p_booking_error(p):
    """booking : BOOK NUMBER TICKETS FOR STRING ON DATE FOR
    | BOOK error TICKETS FOR STRING ON DATE FOR EMAIL
    | BOOK NUMBER TICKETS FOR STRING ON error FOR EMAIL
    | BOOK NUMBER TICKETS FOR error ON DATE FOR EMAIL
    | BOOK error TICKETS FOR error ON DATE FOR EMAIL"""
    if len(p) == 10:
        if not isinstance(p[2], int) and not isinstance(p[2], float):
            print(f"Expected a integer but got '{check_type(p[2].value)}'")
        elif not isinstance(p[5], str):
            print(f"Expected STRING for event name but got '{check_type(p[5].value)}'")
        elif not re.match(r"\d{4}-\d{2}-\d{2}", p[7].value):
            print(f"Expected DATE in YYYY-MM-DD format but got '{p[7].value}'")
        else:
            print(f"Email is missing")
    elif len(p) == 9:
        if not isinstance(p[5], str):
            print(f"Expected STRING for event name but got '{check_type(p[5].value)}'")
        elif not isinstance(p[2], int):
            print(
                f"Expected a integer for number of tickets but got '{check_type(p[2].value)}'"
            )
        elif not re.match(r"\d{4}-\d{2}-\d{2}", p[7]):
            print(f"The Event Date is missing")
        else:
            print(f"Email is missing")
    else:
        print(f"Invalid syntax for booking tickets (line {p.lineno(1)})")

def p_status(p):
    """status : STATUS OF BOOKING BOOKING_ID FOR EMAIL
    | STATUS OF TICKETS FOR EMAIL"""
    if len(p) == 7:
        p[0] = ("status", p[4],p[6])
    else:
        p[0] = ("status", "tickets",p[5])


def p_status_error(p):
    """status : STATUS OF BOOKING error
    | STATUS OF BOOKING BOOKING_ID FOR error
    | STATUS OF error
    | STATUS OF
    """
    if len(p) == 7:
        if re.match(r"booking_[a-zA-Z0-9_]+", p[4].value):
            print(f"Expected a booking_id but got '{check_type(p[4].value)}'")
        else:
            print(f"Expected user email but got '{p[6].value}'")
    elif len(p) == 4:
        if p[3] != "TICKETS":
            if isinstance(p[3].value, str):
                print(f"Expected TICKETS keyword but got '{p[3].value}'")
            elif re.match(r"booking_[a-zA-Z0-9_]+", p[3].value):
                print(
                    f"Are you try to get the status of a booking?\nuse STATUS OF BOOKING {p[3].value} instead."
                )
            else:
                print(f"Expected user email but got '{p[3].value}'")
    else:
        print(f"Invalid syntax to retrieve status (line {p.lineno(1)})")

def p_view(p):
    """view : SHOW AVAILABLE TICKETS FOR STRING
    | SHOW MY RESERVATIONS
    | SHOW MY CONFIRMED BOOKINGS
    | SHOW MY PAID TICKETS
    | SHOW MY CANCELED BOOKINGS"""
    if len(p) == 6:
        p[0] = ("view", p[5])
    else:
        p[0] = ("view", p[3])


def p_view_error(p):
    """view : SHOW AVAILABLE TICKETS FOR error
    | SHOW MY error
    | SHOW MY error BOOKINGS
    | SHOW MY error TICKETS
    """
    if len(p) == 6:
        if not isinstance(p[5], str):
            print(f"Expected a String but got '{check_type(p[4].value)}'")
    else:
        if (
            p[3] != "TICKETS"
            and p[3] != "CONFIRMED"
            and p[3] != "PAID"
            and p[3] != "CANCELED"
        ):
            print(
                f"Expected one of 'TICKETS', 'CONFIRMED', 'PAID ', 'CANCELED' but got '{p[3].value}'"
            )
        else:
            print(f"Invalid syntax to view status (line {p.lineno(1)})")


def p_selection(p):
    "selection : SELECT TICKET TICKET_ID"
    p[0] = ("selection", p[3])


def p_selection_error(p):
    "selection : SELECT TICKET error"
    print(f"Expected the ticket id but got '{p[3].value}'")


def p_sorting(p):
    """sorting : SORT TICKETS BY NUMBER
    | SORT TICKETS BY DATE"""
    p[0] = ("sorting", p[4])


def p_sorting_error(p):
    """sorting : SORT TICKETS BY error"""
    print(f"Expected ticket price or date but got {p[4].value}")


def p_fetching(p):
    "fetching : FETCH TICKETS FROM API API_URL"
    p[0] = ("fetching", p[5])


def p_fetching_(p):
    "fetching : FETCH TICKETS FROM API error"
    print(f"Expected the API url but got '{p[5].value}'")

def p_region(p):
    "region : SHOW AVAILABLE TICKETS IN STRING"
    p[0] = ("region", p[5])


def p_region_error(p):
    "region : SHOW AVAILABLE TICKETS error"
    print(f"Expected the region but got '{p[4].value}'")


def p_reservation(p):
    "reservation : RESERVE NUMBER TICKETS FOR STRING ON DATE"
    if isinstance(p[2], float):
        print(
            f"Warning: Fractional tickets ({p[2]}) are not allowed. Rounding to nearest integer."
        )
        p[2] = round(p[2])
    p[0] = ("reservation", p[2], p[5], p[7])


def p_reservation_error(p):
    """reservation : RESERVE error FOR STRING ON DATE
    | RESERVE NUMBER FOR error ON DATE
    | RESERVE NUMBER FOR STRING ON error"""
    if len(p) == 7:
        if not isinstance(p[2], int) and not isinstance(p[2], float):
            print(f"Expected a integer but got '{check_type(p[2].value)}'")
        if not isinstance(p[4], str):
            print(f"Expected STRING for event name but got '{check_type(p[4].value)}'")
    elif len(p) == 6:
        if not isinstance(p[4], str):
            print(f"Expected STRING for event name but got '{check_type(p[4].value)}'")
        elif not isinstance(p[2], int):
            print(
                f"Expected a integer for number of tickets but got '{check_type(p[2].value)}'"
            )
        else:
            print(f"The Event Date is missing")
    else:
        print(f"Invalid syntax for reserving tickets (line {p.lineno(1)})")


def p_listing(p):
    "listing : LIST ALL EVENTS"
    p[0] = ("listing",)


def p_listing_error(p):
    "listing : LIST error"
    print(f"Expected the keyword 'ALL EVENTS' but got '{p[2].value}'")


def p_payment(p):
    """payment : PAY FOR ALL BOOKINGS BOOKING_ID USING PAYMENT_METHOD
    | CANCEL BOOKING BOOKING_ID"""
    if len(p) == 8:
        p[0] = ("payment", p[5], p[7])
    else:
        p[0] = ("cancel", p[3])


def p_payment_error(p):
    """payment : PAY FOR ALL BOOKINGS error USING PAYMENT_METHOD
    | PAY FOR ALL BOOKINGS BOOKING_ID USING error
    | CANCEL BOOKING error"""
    if len(p) == 7:
        if not re.match(r"booking_[a-zA-Z0-9_]+", p[5].value):
            print(f"Expected the booking ID but got '{p[5].value}' ")
        if not re.match(r"CreditCard|PayPal|Crypto", p[7]):
            print(f"Expected a payment method but got '{p[7].value}' ")
        else:
            print(f"Error in Payment Syntax'")
    elif len(p) == 4:
        if not re.match(r"booking_[a-zA-Z0-9_]+", p[3]):
            print(f"Expected the booking ID but got '{p[3].value}' ")
    else:
        print(f"Error in Payment Syntax'")


# Error handling for parser
def p_error(p):
    print(f"Syntax error at (line {p.lineno}, col {p.lexpos}) unexpected: '{p.value}'")


# Build the parser
parser = yacc.yacc()

# Test the parser
if __name__ == "__main__":
    # while True:
    # try:
    #     s = input('Enter command: ')
    # except EOFError:
    #     break
    # if not s:
    #     continue
    testCode = testCode.strip()
    result = parser.parse(testCode)
    # print(result)  # Output: 5
    sem = semantic_analyzer(result)
    if sem:
        print("Hi semantics working")

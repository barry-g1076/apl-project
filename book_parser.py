import ply.yacc as yacc
import book_lexer
from semantic_analyzer import *
from utils import *
from testcode import data as testCode
from utils.type_check import check_type
from utils.errors import error_collector
from utils.validations import DataValidator


tokens = book_lexer.tokens  # Import tokens from your lexer
syntaxWarnings = []


# Todo: add a command to save data to file
# Todo: add a command to load data from file
# Parser rules
def p_command(p):
    """command : statement
    | command statement"""

    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_statement(p):
    """command : booking
    | status
    | view
    | fetching
    | region
    | reservation
    | listing
    | payment
    | search
    | policy
    | dummy"""

    p[0] = p[1]


# Dummy rule to suppress the warning
def p_dummy(p):
    """dummy : ID"""
    pass  # Do nothing with this rule


def p_booking(p):
    """booking : BOOK NUMBER TICKETS FOR STRING ON DATE FOR EMAIL"""
    if DataValidator.is_float(p[2]):
        syntaxWarnings.append(
            f"Warning: Fractional tickets ({p[2]}) are not allowed. Rounding to nearest integer."
        )
        p[2] = round(p[2])
    if not DataValidator.validate_date(p[7]):
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
        if not DataValidator.is_int(p[2]) and not DataValidator.is_float(p[2]):
            error_collector.parse_errors.append(
                f"Expected a integer for the number of tickets but got '{check_type(p[2].value)}'"
            )
        elif not DataValidator.is_str[5]:
            error_collector.parse_errors.append(
                f"Expected STRING for event name but got '{check_type(p[5].value)}'"
            )
        elif not DataValidator.validate_date(p[7]):
            error_collector.parse_errors.append(
                f"Expected DATE in YYYY-MM-DD format but got '{p[7].value}'"
            )
        else:
            error_collector.parse_errors.append(f"Email is missing")
    elif len(p) == 9:
        if not DataValidator.is_str(p[5]):
            error_collector.parse_errors.append(
                f"Expected STRING for event name but got '{check_type(p[5].value)}'"
            )
        elif not DataValidator.is_int(p[2]):
            error_collector.parse_errors.append(
                f"Expected a integer for number of tickets but got '{check_type(p[2].value)}'"
            )
        elif not DataValidator.validate_date(p[7]):
            error_collector.parse_errors.append(f"The Event Date is missing")
        else:
            error_collector.parse_errors.append(f"Email is missing")
    else:
        error_collector.parse_errors.append(
            f"Invalid syntax for booking tickets (line {p.lineno(1)})"
        )


def p_status(p):
    """status : STATUS OF BOOKING BOOKING_ID FOR EMAIL
    | STATUS OF TICKETS FOR EMAIL"""
    if len(p) == 7:
        if not DataValidator.validate_booking_id(p[4]):
            error_collector.parse_errors.append(f"Invalid booking ID format: {p[4]}")
        if not DataValidator.validate_email(p[6]):
            error_collector.parse_errors.append(f"Invalid email format: {p[6].value}")
        p[0] = ("status", p[4], p[6])
    else:
        if not DataValidator.validate_email(p[5]):
            error_collector.parse_errors.append(f"Invalid email format: {p[5].value}")
        p[0] = ("status", "tickets", p[5])


def p_status_error(p):
    """status : STATUS OF BOOKING error
    | STATUS OF BOOKING BOOKING_ID FOR error
    | STATUS OF error
    | STATUS OF TICKETS FOR error"""
    if len(p) == 7:
        if not DataValidator.validate_booking_id(p[4]):
            error_collector.parse_errors.append(
                f"Expected a booking_id but got '{p[4]}'"
            )
        if not DataValidator.validate_email(p[6]):
            error_collector.parse_errors.append(f"Expected user email but got '{p[6]}'")
    elif len(p) == 4:
        if p[3] != "TICKETS":
            if isinstance(p[3], str):
                error_collector.parse_errors.append(
                    f"Expected TICKETS keyword but got '{p[3]}'"
                )
            elif DataValidator.validate_booking_id(p[3]):
                error_collector.parse_errors.append(
                    f"Are you trying to get the status of a booking?\nUse STATUS OF BOOKING {p[3]} instead."
                )
            else:
                error_collector.parse_errors.append(
                    f"Expected user email but got '{p[3]}'"
                )
    elif len(p) == 6:
        if not DataValidator.validate_email(p[5]):
            error_collector.parse_errors.append(f"Expected user email but got '{p[5]}'")
    else:
        error_collector.parse_errors.append(
            f"Invalid syntax to retrieve status (line {p.lineno(1)})"
        )


def p_view(p):
    """view : SHOW AVAILABLE TICKETS FOR STRING
    | SHOW RESERVATIONS FOR EMAIL
    | SHOW CONFIRMED BOOKINGS FOR EMAIL
    | SHOW PAID TICKETS FOR EMAIL
    | SHOW CANCELED BOOKINGS FOR EMAIL"""
    if len(p) == 6:
        if p[2] == "AVAILABLE":
            if not DataValidator.is_str(p[5]):
                error_collector.parse_errors.append(
                    f"Expected event name but got '{p[5]}'"
                )
        else:
            if not DataValidator.validate_email(p[5]):
                error_collector.parse_errors.append(f"Invalid email format: {p[5]}")
        p[0] = ("view", p[2].lower(), p[5])
    else:
        if not DataValidator.validate_email(p[4]):
            error_collector.parse_errors.append(f"Invalid email format: {p[4]}")
        p[0] = ("view", p[2].lower(), p[4])


def p_view_error(p):
    """view : SHOW error
    | SHOW AVAILABLE TICKETS FOR error
    | SHOW error FOR EMAIL
    | SHOW error BOOKINGS FOR EMAIL
    | SHOW error TICKETS FOR EMAIL
    | SHOW RESERVATIONS FOR error
    | SHOW CONFIRMED BOOKINGS FOR error
    | SHOW CANCELED BOOKINGS FOR error
    | SHOW CANCELED TICKETS FOR error"""
    if len(p) == 6:
        if p[2] == "AVAILABLE":
            if not isinstance(p[5], str):
                error_collector.parse_errors.append(
                    f"Expected event name but got '{p[5]}'"
                )
        else:
            if not DataValidator.validate_email(p[5]):
                error_collector.parse_errors.append(
                    f"Expected valid email but got '{p[5]}'"
                )
        if not DataValidator.validate_view_type(p[2].lower()):
            error_collector.parse_errors.append(
                f"Expected one of 'AVAILABLE', 'CONFIRMED', 'PAID', 'CANCELED' but got '{p[2]}'"
            )
    elif len(p) == 5:
        if not DataValidator.validate_email(p[4]):
            error_collector.parse_errors.append(
                f"Expected valid email but got '{p[4]}'"
            )
        if p[2] != "RESERVATIONS":
            error_collector.parse_errors.append(
                f"Expected 'RESERVATIONS' but got '{p[2]}'"
            )
    else:
        error_collector.parse_errors.append(
            f"Invalid syntax to view status (line {p.lineno(1)})"
        )


def p_fetching(p):
    "fetching : FETCH TICKETS FROM API API_URL"
    p[0] = ("fetching", p[5])


def p_fetching_error(p):
    "fetching : FETCH TICKETS FROM API error"
    error_collector.parse_errors.append(f"Expected API URL but got '{p[5]}'")


def p_region(p):
    "region : SHOW AVAILABLE TICKETS IN STRING"
    if not DataValidator.is_str(p[5]):
        error_collector.parse_errors.append(f"Expected region name but got '{p[5]}'")
    p[0] = ("region", p[5])


def p_region_error(p):
    "region : SHOW AVAILABLE TICKETS error"
    error_collector.parse_errors.append(f"Expected region name but got '{p[4]}'")


def p_reservation(p):
    "reservation : RESERVE NUMBER TICKETS FOR STRING ON DATE FOR EMAIL"
    if DataValidator.is_float(p[2]):
        syntaxWarnings.append(
            f"Warning: Fractional tickets ({p[2]}) are not allowed. Rounding to nearest integer."
        )
        p[2] = round(p[2])
    if not DataValidator.validate_date(p[7]):
        error_collector.parse_errors.append(
            f"Expected DATE in YYYY-MM-DD format but got '{p[7]}'"
        )
    if not DataValidator.validate_email(p[9]):
        error_collector.parse_errors.append(f"Invalid email format: {p[9]}")
    p[0] = ("reservation", p[2], p[5], p[7], p[9])


def p_reservation_error(p):
    """reservation : RESERVE NUMBER FOR STRING ON DATE FOR
    | RESERVE error FOR STRING ON DATE FOR EMAIL
    | RESERVE NUMBER FOR error ON DATE FOR EMAIL
    | RESERVE NUMBER FOR STRING ON DATE FOR error
    | RESERVE NUMBER FOR STRING ON error FOR EMAIL"""
    if len(p) == 10:
        if not DataValidator.is_int(p[2]) and not DataValidator.is_float(p[2]):
            error_collector.parse_errors.append(
                f"Expected integer for number of tickets but got '{check_type(p[2].value)}'"
            )
        elif not DataValidator.is_str(p[5]):
            error_collector.parse_errors.append(
                f"Expected event name but got '{check_type(p[5].value)}'"
            )
        elif not DataValidator.validate_date(p[7]):
            error_collector.parse_errors.append(
                f"Expected DATE in YYYY-MM-DD format but got '{p[7]}'"
            )
        elif not DataValidator.validate_email(p[9]):
            error_collector.parse_errors.append(f"Email is missing or invalid")
    elif len(p) == 9:
        if not DataValidator.is_str(p[5]):
            error_collector.parse_errors.append(
                f"Expected event name but got '{check_type(p[5].value)}'"
            )
        elif not DataValidator.is_int(p[2]):
            error_collector.parse_errors.append(
                f"Expected integer for number of tickets but got '{check_type(p[2].value)}'"
            )
        elif not DataValidator.validate_date(p[7]):
            error_collector.parse_errors.append(f"The Event Date is missing or invalid")
        else:
            error_collector.parse_errors.append(f"Email is missing")
    else:
        error_collector.parse_errors.append(
            f"Invalid syntax for reserving tickets (line {p.lineno(1)})"
        )


def p_listing(p):
    "listing : LIST ALL EVENTS"
    p[0] = ("listing",)


def p_listing_error(p):
    "listing : LIST error"
    error_collector.parse_errors.append(f"Expected 'ALL EVENTS' but got '{p[2]}'")


def p_payment(p):
    """payment : PAY FOR ALL BOOKINGS BOOKING_ID USING PAYMENT_METHOD FOR EMAIL
    | CANCEL BOOKING BOOKING_ID FOR EMAIL"""
    if len(p) == 10:
        if not DataValidator.validate_booking_id(p[5]):
            error_collector.parse_errors.append(f"Invalid booking ID format: {p[5]}")
        if not DataValidator.validate_payment_method(p[7]):
            error_collector.parse_errors.append(f"Invalid payment method: {p[7]}")
        if not DataValidator.validate_email(p[9]):
            error_collector.parse_errors.append(f"Invalid email format: {p[9]}")
        p[0] = ("payment", p[5], p[7], p[9])
    else:
        if not DataValidator.validate_booking_id(p[3]):
            error_collector.parse_errors.append(f"Invalid booking ID format: {p[3]}")
        if not DataValidator.validate_email(p[5]):
            error_collector.parse_errors.append(f"Invalid email format: {p[5]}")
        p[0] = ("cancel", p[3], p[5])


def p_payment_error(p):
    """payment : PAY FOR ALL BOOKINGS BOOKING_ID USING PAYMENT_METHOD FOR
    | PAY FOR ALL BOOKINGS error USING PAYMENT_METHOD FOR EMAIL
    | PAY FOR ALL BOOKINGS BOOKING_ID USING error FOR EMAIL
    | CANCEL BOOKING error FOR EMAIL"""
    if len(p) == 10:
        if not DataValidator.validate_booking_id(p[5]):
            error_collector.parse_errors.append(f"Expected booking ID but got '{p[5]}'")
        if not DataValidator.validate_payment_method(p[7]):
            error_collector.parse_errors.append(
                f"Expected payment method but got '{p[7]}'"
            )
        if not DataValidator.validate_email(p[9]):
            error_collector.parse_errors.append(
                f"Expected valid email but got '{p[9]}'"
            )
    elif len(p) == 6:
        if not DataValidator.validate_booking_id(p[3]):
            error_collector.parse_errors.append(f"Expected booking ID but got '{p[3]}'")
        if not DataValidator.validate_email(p[5]):
            error_collector.parse_errors.append(
                f"Expected valid email but got '{p[5]}'"
            )
    else:
        error_collector.parse_errors.append(
            f"Invalid payment/cancel syntax (line {p.lineno(1)})"
        )


##* AI -Grammar *##
def p_search(p):
    """search : SEARCH FOR STRING IN STRING"""
    if not DataValidator.is_str(p[3]):
        error_collector.parse_errors.append(
            f"Expected quoted string for search term but got '{check_type(p[3])}'"
        )
    if not DataValidator.is_str(p[5]):
        error_collector.parse_errors.append(
            f"Expected quoted string for region but got '{check_type(p[5])}'"
        )
    p[0] = ("search", p[3], p[5])


def p_search_error(p):
    """search : SEARCH FOR error IN STRING
    | SEARCH FOR STRING IN error
    | SEARCH error
    | SEARCH FOR error"""
    if len(p) == 6:
        if not DataValidator.is_str(p[3]):
            error_collector.parse_errors.append(
                f"Expected quoted string for search term but got '{check_type(p[3])}'"
            )
        if not DataValidator.is_str(p[5]):
            error_collector.parse_errors.append(
                f"Expected quoted string for region but got '{check_type(p[5])}'"
            )
    elif len(p) == 4:
        if p[2] != "FOR":
            error_collector.parse_errors.append(
                f"Expected 'FOR' keyword but got '{p[2]}'"
            )
        else:
            error_collector.parse_errors.append(f"Missing search term or region")
    elif len(p) == 3:
        error_collector.parse_errors.append(
            f"Expected search pattern 'SEARCH FOR <term> IN <region>'"
        )
    else:
        error_collector.parse_errors.append(
            f"Invalid search syntax (line {p.lineno(1)})"
        )


def p_policy(p):
    """policy : SHOW POLICIES FOR STRING"""
    if not DataValidator.is_str(p[4]):
        error_collector.parse_errors.append(
            f"Expected quoted string for event name but got '{check_type(p[4])}'"
        )
    p[0] = ("policy", p[4])


def p_policy_error(p):
    """policy : SHOW POLICIES FOR error
    | SHOW error
    | SHOW POLICIES error"""
    if len(p) == 5:
        if not DataValidator.is_str(p[4]):
            error_collector.parse_errors.append(
                f"Expected quoted string for event name but got '{check_type(p[4])}'"
            )
    elif len(p) == 3:
        if p[2] != "POLICIES":
            error_collector.parse_errors.append(
                f"Expected 'POLICIES' keyword but got '{p[2]}'"
            )
        else:
            error_collector.parse_errors.append(
                f"Missing event name after 'POLICIES FOR'"
            )
    else:
        error_collector.parse_errors.append(
            f"Invalid policy syntax (line {p.lineno(1)})"
        )


# Error handling for parser
def p_error(p):
    if p:
        error_msg = (
            f"Syntax error at (line {p.lineno}, col {p.lexpos}) unexpected: '{p.value}'"
        )
    else:
        error_msg = "Syntax error at end of input"

    error_collector.parse_errors.append(error_msg)


# Build the parser
parser = yacc.yacc()


def parse_input(data):
    error_collector.reset()
    result = parser.parse(data)
    # Return errors along with result (if any)
    return {
        "success": not any([error_collector.lex_errors, error_collector.parse_errors]),
        "result": result,
        "errors": error_collector.lex_errors + error_collector.parse_errors,
        "warnings": syntaxWarnings,
    }


# Test the parser
# if __name__ == "__main__":
#     # while True:
#     # try:
#     #     s = input('Enter command: ')
#     # except EOFError:
#     #     break
#     # if not s:
#     #     continue
#     testCode = testCode.strip()
#     result = parser.parse(testCode)
#     # print(result)  # Output: 5
#     sem = semantic_analyzer(result)
#     if sem:
#         print("Hi semantics working")

# def p_selection(p):
#     "selection : SELECT TICKET TICKET_ID"
#     p[0] = ("selection", p[3])


# def p_selection_error(p):
#     "selection : SELECT TICKET error"
#     print(f"Expected the ticket id but got '{p[3].value}'")


# def p_sorting(p):
#     """sorting : SORT TICKETS BY NUMBER
#     | SORT TICKETS BY DATE"""
#     p[0] = ("sorting", p[4])


# def p_sorting_error(p):
#     """sorting : SORT TICKETS BY error"""
#     print(f"Expected ticket price or date but got {p[4].value}")
# | selection
# | command selection
# | sorting
# | command sorting

import ply.yacc as yacc
import book_lexer
from semantic_analyzer import *
from utils import *
from testcode import data as testCode
from llm_integration import LLMBookingAssistant
import json
import os

tokens = book_lexer.tokens  # Import tokens from your lexer

# Initialize LLM assistant
llm_assistant = LLMBookingAssistant(os.getenv('OPENAI_API_KEY', ''))

# Todo: add a command to save data to file
# Todo: add a command to load data from file
# Parser rules
def p_command(p):
    """command : booking
    | command booking
    | status
    | command status
    | view
    | command view
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
# Symbol table to track ticket states
ticket_data = {}

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
    | cancel_statement
    | search_statement
    | policy_statement"""
    p[0] = p[1]

# SEARCH for events
def p_search_statement(p):
    """search_statement : SEARCH FOR QUOTED_STRING IN QUOTED_STRING"""
    event_name = p[3]
    region = p[5]
    
    events = llm_assistant.get_available_events(region)
    # Convert both event name and search term to lowercase for case-insensitive search
    event_name = event_name.lower()
    matching_events = []
    
    for event in events:
        # Check if the search term appears in the event name, category, or description
        if (event_name in event['name'].lower() or 
            event_name in event['category'].lower() or 
            event_name in event['description'].lower()):
            matching_events.append(event)
    
    if matching_events:
        print(f"Found {len(matching_events)} matching events in {region}:")
        for event in matching_events:
            print(f"- {event['name']}")
            print(f"  Date: {event['date']} at {event['time']}")
            print(f"  Location: {event['location']}")
            print(f"  Price: ${event['price']} {event['currency']}")
            print(f"  Available: {event['tickets_available']} tickets")
            print(f"  Status: {event['status']}")
            print(f"  Category: {event['category']}")
            print(f"  Description: {event['description']}")
            print("")
    else:
        print(f"No events matching '{event_name}' found in {region}")
    
    p[0] = f"Searched for {event_name} in {region}"

# Get booking policies
def p_policy_statement(p):
    """policy_statement : SHOW POLICIES FOR QUOTED_STRING"""
    event_name = p[4]
    policies = llm_assistant.get_booking_policies(event_name)
    
    if policies:
        print(f"Booking policies for {event_name}:")
        print(f"- Cancellation: {policies.get('cancellation_policy', 'N/A')}")
        print(f"- Payment: {policies.get('payment_policy', 'N/A')}")
        print(f"- Refund: {policies.get('refund_policy', 'N/A')}")
    else:
        print(f"No policies found for {event_name}")
    
    p[0] = f"Showed policies for {event_name}"

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
        p[0] = ("status", p[4], p[6])
# BOOK tickets
def p_book_statement(p):
    """book_statement : BOOK NUMBER TICKETS FOR QUOTED_STRING ON DATE"""
    event_name = p[5]
    date = p[7]
    num_tickets = int(p[2])
    
    # Validate booking with LLM
    if llm_assistant.validate_booking(event_name, date, num_tickets):
        if event_name not in ticket_data:
            ticket_data[event_name] = {"available": 0, "reserved": 0, "confirmed": 0, "paid": 0}
        
        ticket_data[event_name]["reserved"] += num_tickets
        print(f"Successfully reserved {num_tickets} tickets for {event_name} on {date}")
    else:
        print(f"Booking failed: Not enough tickets available for {event_name} on {date}")
    
    p[0] = f"Booking {num_tickets} tickets for {event_name} on {date}"

# STATUS of a booking
def p_status_statement(p):
    """status_statement : STATUS BOOKING_ID"""
    p[0] = f"Checking status of booking {p[2]}"

# SHOW available tickets
def p_show_statement(p):
    """show_statement : SHOW AVAILABLE TICKETS IN QUOTED_STRING"""
    region = p[4]
    events = llm_assistant.get_available_events(region)
    
    if events:
        print(f"Available tickets in {region}:")
        for event in events:
            print(f"- {event['name']} on {event['date']}")
            print(f"  Price: ${event['price']} {event['currency']}")
            print(f"  Available: {event['tickets_available']} tickets")
            print(f"  Location: {event['location']}")
            print(f"  Time: {event['time']}")
            print(f"  Status: {event['status']}")
            print(f"  Category: {event['category']}")
            print(f"  Description: {event['description']}")
    else:
        print(f"No events found in {region}")
    
    p[0] = f"Displaying available tickets in {region}"

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
    """reserve_statement : RESERVE TICKETS FOR QUOTED_STRING"""
    p[0] = f"Reserving tickets for {p[4]}"

# SHOW available tickets in a region
def p_region_statement(p):
    """region_statement : SHOW AVAILABLE TICKETS IN QUOTED_STRING"""
    p[0] = f"Displaying available tickets in {p[4]} region"

def p_speech_statement(p):
    """speech_statement : READ OUT MY BOOKING DETAILS
    | READ AVAILABLE TICKETS FOR QUOTED_STRING"""
    if len(p) == 5:
        p[0] = "Reading out booking details"
    else:
        p[0] = ("status", "tickets", p[5])


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
    | SHOW RESERVATIONS FOR EMAIL
    | SHOW CONFIRMED BOOKINGS FOR EMAIL
    | SHOW PAID TICKETS FOR EMAIL
    | SHOW CANCELED BOOKINGS FOR EMAIL"""
    if len(p) == 6:
        p[0] = ("view", p[2], p[5])
    else:
        p[0] = ("view", p[2], p[4])


def p_view_error(p):
    """view : SHOW error
    | SHOW AVAILABLE TICKETS FOR error
    | SHOW error FOR EMAIL
    | SHOW error BOOKINGS FOR EMAIL
    | SHOW error TICKETS FOR EMAIL
    | SHOW RESERVATIONS FOR error
    | SHOW CONFIRMED BOOKINGS FOR error
    | SHOW CANCELED BOOKINGS FOR error
    | SHOW CANCELED TICKETS FOR error
    """
    if len(p) == 6:
        if not isinstance(p[5], str) and p[2] == "AVAILABLE":
            print(f"Expected a String but got '{check_type(p[5])}'")
        elif not isinstance(p[5], str):
            if not re.match(
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", p[5].value
            ):
                print(f"Expected user email but got: {p[5].value}")
        if (
            p[2] != "tickets"
            and p[2] != "confirmed"
            and p[2] != "paid"
            and p[2] != "canceled"
            and p[2] != "available"
        ):
            print(
                f"Expected one of 'TICKETS', 'CONFIRMED', 'PAID ', 'CANCELED', 'AVAILABLE' but got '{p[2].value}'"
            )
    elif len(p) == 5:
        if (
            not re.match(
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", p[4].value
            )
            and p[2] == "RESERVATIONS"
        ):
            print(f"Expected user email but got: {p[4].value}")
        elif p[2] != "reservations":
            print(f"Expected 'RESERVATIONS' but got '{p[2]}'")
    else:
        print(f"Invalid syntax to view status (line {p.lineno(1)})")

def p_fetching(p):
    "fetching : FETCH TICKETS FROM API API_URL"
    p[0] = ("fetching", p[5])

# LIST events
def p_list_statement(p):
    """list_statement : LIST EVENTS"""
    p[0] = "Listing available events"

# PAY for tickets
def p_pay_statement(p):
    """pay_statement : PAY BOOKING_ID USING PAYMENT_METHOD"""
    booking_id = p[2]
    payment_method = p[4]
    print(f"Processing payment for {booking_id} using {payment_method}")
    p[0] = f"Payment processed for {booking_id}"

# CANCEL booking
def p_cancel_statement(p):
    """cancel_statement : CANCEL BOOKING_ID"""
    booking_id = p[2]
    print(f"Cancelling booking {booking_id}")
    p[0] = f"Cancelled booking {booking_id}"

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
    "reservation : RESERVE NUMBER TICKETS FOR STRING ON DATE FOR EMAIL"
    if isinstance(p[2], float):
        print(
            f"Warning: Fractional tickets ({p[2]}) are not allowed. Rounding to nearest integer."
        )
        p[2] = round(p[2])
    p[0] = ("reservation", p[2], p[5], p[7],p[9])


def p_reservation_error(p):
    """reservation : RESERVE NUMBER FOR STRING ON DATE FOR
    | RESERVE error FOR STRING ON DATE FOR EMAIL
    | RESERVE NUMBER FOR error ON DATE FOR EMAIL
    | RESERVE NUMBER FOR STRING ON DATE FOR error
    | RESERVE NUMBER FOR STRING ON error FOR EMAIL"""
    if len(p) == 10:
        if not isinstance(p[2], int) and not isinstance(p[2], float):
            print(f"Expected a integer but got '{check_type(p[2].value)}'")
        elif not isinstance(p[5], str):
            print(f"Expected STRING for event name but got '{check_type(p[5].value)}'")
        elif not re.match(r"\d{4}-\d{2}-\d{2}", p[7].value):
            print(f"Expected DATE in YYYY-MM-DD format but got '{p[7].value}'")
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
        print(f"Invalid syntax for reserving tickets (line {p.lineno(1)})")


def p_listing(p):
    "listing : LIST ALL EVENTS"
    p[0] = ("listing",)


def p_listing_error(p):
    "listing : LIST error"
    print(f"Expected the keyword 'ALL EVENTS' but got '{p[2].value}'")


def p_payment(p):
    """payment : PAY FOR ALL BOOKINGS BOOKING_ID USING PAYMENT_METHOD FOR EMAIL
    | CANCEL BOOKING BOOKING_ID FOR EMAIL"""
    if len(p) == 10:
        p[0] = ("payment", p[5], p[7], p[9])
    else:
        p[0] = ("cancel", p[3],p[5])


def p_payment_error(p):
    """payment : PAY FOR ALL BOOKINGS BOOKING_ID USING PAYMENT_METHOD FOR
    | PAY FOR ALL BOOKINGS error USING PAYMENT_METHOD FOR EMAIL
    | PAY FOR ALL BOOKINGS BOOKING_ID USING error FOR EMAIL
    | CANCEL BOOKING error FOR EMAIL"""
    if len(p) == 10:
        if not isinstance(p[5], str):
            if not re.match(r"booking_[a-zA-Z0-9_]+", p[5].value):
                print(f"Expected the booking ID but got '{p[5].value}' ")
        elif not re.match(r"CreditCard|PayPal|Crypto", p[7].value):
            print(f"Expected a payment method but got '{p[7].value}' ")
        elif not re.match(
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", p[9].value
            ):
            print(f"Expected a valid email but got '{p[9].value}' ")
        else:
            print(f"Error in Payment Syntax'")
    elif len(p) == 6:
        if not re.match(r"booking_[a-zA-Z0-9_]+", p[3]):
            print(f"Expected the booking ID but got '{p[3].value}' ")
        elif not re.match(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", p[5].value
        ):
            print(f"Expected a valid email but got '{p[5].value}' ")
    else:
        print(
            f"user email is missing'"
        )


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
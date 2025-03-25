import ply.yacc as yacc
from book_lexer import tokens
from llm_integration import LLMBookingAssistant
import json
import os

# Initialize LLM assistant
llm_assistant = LLMBookingAssistant(os.getenv('OPENAI_API_KEY', ''))

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
        p[0] = f"Reading available tickets for {p[5]}"

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

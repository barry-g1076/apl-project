import re
from testcode import jsonEvent
from datetime import date, datetime
from typing import Dict, List, Optional, Tuple, Union, Any
from book_printer import ColorErrorPrinter
import uuid
from dataclasses import dataclass
from enum import Enum, auto
import requests
from fastapi import Request

# Constants
MAX_TICKETS_PER_USER = 5
VALID_TICKET_STATUSES = {
    "booked",
    "confirmed",
    "pending",
    "canceled",
    "reservations",
    "paid",
}


# Data models
class TicketStatus(Enum):
    BOOKED = auto()
    CONFIRMED = auto()
    PENDING = auto()
    CANCELED = auto()


@dataclass
class Ticket:
    ticket_id: str
    status: TicketStatus


@dataclass
class Booking:
    booking_id: str
    tickets: List[Ticket]
    created_at: datetime = datetime.now()


# Initialize printer
printer = ColorErrorPrinter()

# Sample data - would normally come from a database
EVENT_DATA = jsonEvent
USER_DATA = {
    "Jazz Festival 2025": {
        "ticketNo": 5,
        "bookings": [
            {
                "booking_id": "booking_59c133d1",
                "tickets": [
                    {"ticket_id": "ticket_3b353612", "status": "booked"},
                    {"ticket_id": "ticket_20350e02", "status": "booked"},
                ],
            },
            {
                "booking_id": "booking_a7d829f4",
                "tickets": [
                    {"ticket_id": "ticket_89e021bb", "status": "pending"},
                    {"ticket_id": "ticket_63fce910", "status": "pending"},
                    {"ticket_id": "ticket_1a2b3c4d", "status": "pending"},
                ],
            },
        ],
    },
    "Rock Night 2025": {
        "ticketNo": 3,
        "bookings": [
            {
                "booking_id": "booking_5c67f3e1",
                "tickets": [
                    {"ticket_id": "ticket_9d8e7f6a", "status": "confirmed"},
                    {"ticket_id": "ticket_11223344", "status": "confirmed"},
                    {"ticket_id": "ticket_abcd1234", "status": "confirmed"},
                ],
            }
        ],
    },
}


def generate_id(prefix: str) -> str:
    """Generate a unique ID with the given prefix."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def validate_event_date(event_date: date) -> bool:
    """Validate that the event date is in the future."""
    return event_date >= date.today()


def validate_ticket_quantity(ticket_no: int) -> Tuple[bool, Optional[str]]:
    """Validate the ticket quantity."""
    if ticket_no <= 0:
        return False, "Number of tickets must be greater than 0"
    if ticket_no > MAX_TICKETS_PER_USER:
        return False, f"Number of tickets cannot exceed {MAX_TICKETS_PER_USER} per user"
    return True, None


def find_event(event_name: str) -> Optional[dict]:
    """Find an event by name."""
    return next((e for e in EVENT_DATA if e["name"] == event_name), None)


def check_ticket_availability(
    event: dict, ticket_no: int
) -> Tuple[bool, Optional[str]]:
    """Check if there are enough tickets available."""
    if event["tickets_available"] < ticket_no:
        return (
            False,
            f"Not enough tickets available (available: {event['tickets_available']})",
        )
    return True, None


def check_user_ticket_limit(
    event_name: str, ticket_no: int, email: str
) -> Tuple[bool, Optional[str]]:
    """Check if user hasn't exceeded ticket limit for the specific event.
    Checks the user's email first, then looks at their tickets for the specified event.
    """

    # Check if user exists in USER_DATA
    if email not in USER_DATA:
        return True, None

    user_data = USER_DATA[email]

    # Check if user has any tickets for this event
    if event_name not in user_data:
        return True, None

    event_data = user_data[event_name]
    current_tickets = event_data.get("ticketNo", 0)

    if current_tickets + ticket_no > MAX_TICKETS_PER_USER:
        return (
            False,
            f"Cannot book more than {MAX_TICKETS_PER_USER} tickets for {event_name}",
        )

    return True, None


def semantic_analyzer(ast: List) -> bool:
    """Process the abstract syntax tree of commands."""
    results = []
    for node in ast:
        if node is None:
            continue
        try:
            if node[0] == "booking":
                results.append(handle_booking(node))
            elif node[0] == "status":
                results.append(handle_status(node[1]))
            elif node[0] == "view":
                results.append(handle_view(node))
            elif node[0] == "fetching":
                results.append(handle_fetch(node[1]))
            elif node[0] == "region":
                results.append(handle_region(node[1]))
            elif node[0] == "reservation":
                results.append(handle_reservation(node))
            elif node[0] == "listing":
                results.append(handle_listing())
            elif node[0] == "payment" or node[0] == "cancel":
                results.append(handle_payment(node))
            elif node[0] == "search":
                results.append(handle_search(node))
            elif node[0] == "policy":
                results.append(handle_policy(node))
        except Exception as e:
            printer.critical(f"Error processing command: {str(e)}")
            results.append(False)
    return all(results)


def handle_booking(node: List) -> bool:
    """Process a booking request with comprehensive validation."""
    if len(node) < 4:
        printer.critical("Invalid booking data format")
        return False

    try:
        ticket_no, event_name, event_date_str, email = (
            node[1],
            node[2],
            node[3],
            node[4],
        )
        ticket_no = int(ticket_no)
        event_date = datetime.strptime(event_date_str, "%Y-%m-%d").date()
    except (ValueError, IndexError) as e:
        printer.critical(f"Invalid booking data format: {str(e)}")
        return False

    # Validate date
    if not validate_event_date(event_date):
        printer.critical("Event date cannot be in the past")
        return False

    # Validate ticket quantity
    is_valid, message = validate_ticket_quantity(ticket_no)
    if not is_valid:
        printer.critical(message)
        return False

    # Find and validate event
    event = find_event(event_name)
    if not event:
        printer.critical("Event not found")
        return False

    # Check ticket availability
    is_available, message = check_ticket_availability(event, ticket_no)
    if not is_available:
        printer.critical(message)
        return False

    # Check user ticket limit
    can_book, message = check_user_ticket_limit(event_name, ticket_no, email)
    if not can_book:
        printer.critical(message)
        return False

    # Process booking
    return create_booking(event, event_name, ticket_no, email)


def create_booking(event: dict, event_name: str, ticket_no: int, email: str) -> bool:
    """Create a new booking and update system state.

    Args:
        event: The event dictionary containing ticket availability
        event_name: Name of the event being booked
        ticket_no: Number of tickets to book
        email: Email of the user making the booking

    Returns:
        bool: True if booking was successful, False otherwise
    """
    try:
        # Update event tickets
        event["tickets_available"] -= ticket_no

        if email not in USER_DATA:
            USER_DATA[email] = {}

        # Initialize user data if not exists
        if event_name not in USER_DATA[email]:
            USER_DATA[email][event_name] = {"ticketNo": 0, "bookings": []}

        # Create booking
        booking_id = generate_id("booking")
        tickets = [
            {"ticket_id": generate_id("ticket"), "status": "confirmed"}
            for _ in range(ticket_no)
        ]

        booking_details = {
            "booking_id": booking_id,
            "tickets": tickets,
            "status": "confirmed",
            "created_at": datetime.now().isoformat(),
        }

        # Update user data
        USER_DATA[email][event_name]["bookings"].append(booking_details)
        USER_DATA[email][event_name]["ticketNo"] += ticket_no

        printer.info(
            f"Successfully booked {ticket_no} tickets for event {event_name} for {email}"
        )
        # printer.info(f"Booking details: {USER_DATA}")
        return True
    except Exception as e:
        printer.critical(f"Failed to create booking: {str(e)}")
        return False


def handle_status(booking_reference: str) -> bool:
    """Display status of bookings or tickets."""
    found = False

    for event_name, event_data in USER_DATA.items():
        for booking in event_data["bookings"]:
            if (
                booking_reference.lower() == "tickets"
                or booking["booking_id"] == booking_reference
            ):
                found = True
                print_booking_status(event_name, booking)

    if not found and booking_reference.lower() != "tickets":
        printer.warning(f"No booking found with ID: {booking_reference}")

    return found


def print_booking_status(event_name: str, booking: dict) -> None:
    """Print formatted booking status."""
    printer.info(
        f"\nEvent: {event_name}\n"
        f"Booking ID: {booking['booking_id']}\n"
        f"Created: {booking.get('created_at', 'N/A')}\n"
        f"Status: {booking.get('status', 'N/A')}\n"
        "Tickets:"
    )

    for ticket in booking["tickets"]:
        printer.info(f"  - {ticket['ticket_id']}: {ticket['status'].upper()}")


def handle_view(node: list) -> bool:
    """Display event information or filtered ticket statuses."""

    view_type, email = node[1], node[2]
    # Check if viewing an event
    event = find_event(view_type)
    if event:
        print_event_details(event)
        return True

    # Check if viewing ticket statuses
    if view_type in VALID_TICKET_STATUSES:
        return print_tickets_by_status(view_type, email)

    printer.warning(f"Invalid view type: {view_type}")
    return False


def print_event_details(event: dict) -> None:
    """Print formatted event details."""
    printer.info(
        f"\nEvent: {event['name']}\n"
        f"Date: {event['date']} {event.get('time', '')}\n"
        f"Description: {event.get('description', 'N/A')}\n"
        f"Location: {event.get('location', 'N/A')}\n"
        f"Tickets available: {event['tickets_available']}"
    )


def print_tickets_by_status(status: str, email: str) -> bool:
    """Print tickets filtered by status."""
    found_data = False

    for event_name, event_data in USER_DATA[email].items():
        for booking in event_data["bookings"]:
            for ticket in booking["tickets"]:
                if ticket["status"].lower() == status.lower():
                    found_data = True
                    printer.info(
                        f"Event: {event_name}, "
                        f"Booking ID: {booking['booking_id']}, "
                        f"Ticket ID: {ticket['ticket_id']}, "
                        f"Status: {ticket['status'].upper()}, "
                        f"Email: {email}"
                    )

    if not found_data:
        printer.info(f"No tickets found with status: {status.upper()}")

    return found_data


def handle_fetch(url: str, timeout: float = 10.0) -> bool:
    """
    Fetch data from a URL and update the event data if successful.

    Args:
        url: The URL to fetch data from
        timeout: Request timeout in seconds (default: 10.0)

    Returns:
        bool: True if fetch and update were successful, False otherwise
    """
    # Validate URL format
    if not url.startswith(("http://", "https://")):
        printer.critical(f"Invalid URL format: {url}")
        return False

    try:
        response = requests.get(
            url, timeout=timeout, headers={"Accept": "application/json"}
        )
        response.raise_for_status()  # Raises HTTPError for bad responses

        data = response.json()

        # Validate response data structure
        if not validate_event_data(data):
            printer.critical("Invalid data structure received from API")
            return False

        for event in data:
            EVENT_DATA.append(event)
            printer.info(
                f"Successfully fetched and added event: {event.get('name', 'Unnamed event')}"
            )
        return True

    except requests.exceptions.Timeout:
        printer.critical(f"Request timed out after {timeout} seconds")
    except requests.exceptions.HTTPError as e:
        printer.critical(f"HTTP error occurred: {str(e)}")
    except requests.exceptions.JSONDecodeError:
        printer.critical("Invalid JSON response from server")
    except requests.exceptions.RequestException as e:
        printer.critical(f"Network error occurred: {str(e)}")
    except Exception as e:
        printer.critical(f"Unexpected error: {str(e)}")

    return False


def validate_event_data(data: Dict[str, Any]) -> bool:
    """
    Validate that the fetched data contains required event fields.

    Args:
        data: Dictionary containing event data

    Returns:
        bool: True if data is valid, False otherwise
    """
    required_fields = {"name", "date", "tickets_available"}

    # If data is a list, validate each item
    if isinstance(data, list):
        return all(validate_event_data(item) for item in data)

    # If data is not a dict, reject
    if not isinstance(data, dict):
        return False

    # Check required fields
    if not all(field in data for field in required_fields):
        return False

    try:
        datetime.strptime(data["date"], "%Y-%m-%d")
        if (
            not isinstance(data["tickets_available"], int)
            or data["tickets_available"] < 0
        ):
            return False
    except (ValueError, KeyError):
        return False

    return True


def handle_region(region: str) -> bool:
    """
    Handle the region of the event.
    Args:
    region: The region of the event.
    Returns:
    bool: True if the region is valid, False otherwise.
    """
    matching_events = [e for e in EVENT_DATA if region.lower() in e["location"].lower()]
    if matching_events:
        print(f"\nEvents in region '{region}':")
        print("―" * 40)
        for event in matching_events:
            print(f"• Event: {event.get('name', 'Unnamed')}")
            print(f"  Location: {event['location']}")
            print(f"  Date: {event.get('date', 'N/A')}")
            print(f"  Tickets: {event.get('tickets_available', 'N/A')}")
            print("―" * 40)
        return True
    else:
        printer.info(f"No events found in region: {region}")
        return False


def handle_reservation(node: List) -> bool:
    """Process a reservation request with comprehensive validation."""
    if len(node) < 4:
        printer.critical("Invalid reservation data format")
        return False

    try:
        ticket_no, event_name, event_date_str, email = (
            node[1],
            node[2],
            node[3],
            node[4],
        )
        ticket_no = int(ticket_no)
        event_date = datetime.strptime(event_date_str, "%Y-%m-%d").date()
    except (ValueError, IndexError) as e:
        printer.critical(f"Invalid reservation data format: {str(e)}")
        return False

    # Validate date
    if not validate_event_date(event_date):
        printer.critical("Event date cannot be in the past")
        return False

    # Validate ticket quantity
    is_valid, message = validate_ticket_quantity(ticket_no)
    if not is_valid:
        printer.critical(message)
        return False

    # Find and validate event
    event = find_event(event_name)
    if not event:
        printer.critical("Event not found")
        return False

    # Check ticket availability
    is_available, message = check_ticket_availability(event, ticket_no)
    if not is_available:
        printer.critical(message)
        return False

    # Check user ticket limit
    can_book, message = check_user_ticket_limit(event_name, ticket_no, email)
    if not can_book:
        printer.critical(message)
        return False

    # Process reservation
    return create_reservation(event, event_name, ticket_no, email)


def create_reservation(
    event: dict, event_name: str, ticket_no: int, email: str
) -> bool:
    """Create a new reservation and update system state."""
    try:
        # Update event tickets
        event["tickets_available"] -= ticket_no

        if email not in USER_DATA:
            USER_DATA[email] = {}
        # Initialize user data if not exists
        if event_name not in USER_DATA:
            USER_DATA[email][event_name] = {"ticketNo": 0, "reservations": []}

        # Create reservation
        reservation_id = generate_id("reservation")
        tickets = [
            {"ticket_id": generate_id("ticket"), "status": "reserved"}
            for _ in range(ticket_no)
        ]

        reservation_details = {
            "reservation_id": reservation_id,
            "tickets": tickets,
            "status": "reserved",
            "created_at": datetime.now().isoformat(),
        }

        # Update user data
        USER_DATA[email][event_name]["reservations"].append(reservation_details)
        USER_DATA[email][event_name]["ticketNo"] += ticket_no

        printer.info(f"Successfully reserved {ticket_no} tickets for {event_name}")
        # printer.info(f"Reservation details: {USER_DATA}")
        return True
    except Exception as e:
        printer.critical(f"Failed to create reservation: {str(e)}")
        return False


def handle_listing() -> bool:
    """Handle listing of all available events.

    Returns:
        bool: True if events were found and displayed, False if no events available
    """
    if not EVENT_DATA:
        printer.info("No events available")
        return False

    for event in EVENT_DATA:
        printer.info(
            f"Event: {event['name']}\n"
            f"Tickets available: {event['tickets_available']}\n"
            "---"
        )
    return True


def handle_payment(node) -> bool:
    """Handle reservation of tickets for an event by processing payment and updating ticket status.

    Args:
        node: A tuple containing reservation data (payment_type, booking_id, ...)

    Returns:
        bool: True if reservation was successful, False otherwise
    """
    VALID_PAYMENT_TYPES = {"CreditCard", "PayPal", "Crypto"}

    if len(node) < 4 and len(node) < 3:
        printer.critical("Invalid node format - missing payment type or booking ID")
        return False

    if len(node) == 4:
        booking_id, payment_type, email = node[1], node[2], node[3]

        # Validate payment type
        if payment_type not in VALID_PAYMENT_TYPES:
            printer.critical(f"Invalid payment type: {payment_type}")
            return False

        # Search for booking across all events
        booking_found = False
        for event_name, event_data in USER_DATA[email].items():
            for booking in event_data.get("bookings", []):
                if booking.get("booking_id") == booking_id:
                    booking_found = True
                    success = _process_tickets(
                        booking.get("tickets", []), event_name, "paid"
                    )
                    if not success:
                        return False

        if not booking_found:
            printer.info(f"Booking ID {booking_id} not found")
            return False
    else:
        booking_id, email = node[1], node[2]
        for event_name, event_data in USER_DATA[email].items():
            for booking in event_data.get("bookings", []):
                if booking.get("booking_id") == booking_id:
                    booking_found = True
                    success = _process_tickets(
                        booking.get("tickets", []), event_name, "cancel"
                    )
                    if not success:
                        return False
    return True


def _process_tickets(tickets: list, event_name: str, status: str) -> bool:
    """Process individual tickets for a booking.

    Args:
        tickets: List of ticket dictionaries
        event_name: Name of the event for logging

    Returns:
        bool: True if all tickets were processed successfully
    """
    if not tickets:
        printer.warning(f"No tickets found for booking in event {event_name}")
        return False

    success = True
    for ticket in tickets:
        if ticket.get("status") != status:
            try:
                ticket["status"] = status
                printer.info(
                    f"Ticket {ticket.get('ticket_id', 'UNKNOWN')} "
                    f"for {event_name} has been {status}"
                )
            except Exception as e:
                printer.error(f"Failed to process ticket: {str(e)}")
                success = False

    return success


##* AI -Semantics and Analyzer *##


def handle_search(request: Request,node: List) -> bool:
    """Process a search request with comprehensive validation."""
    if len(node) < 3:
        printer.critical("Invalid search data format")
        return False

    try:
        assistant = request.app.state.llm_assistant
        search_term, region = node[1], node[2]

        # Remove quotes if present
        search_term = search_term.strip("\"'")
        region = region.strip("\"'")

        if not search_term:
            printer.critical("Search term cannot be empty")
            return False

        if not region:
            printer.critical("Region cannot be empty")
            return False

        events = assistant.get_available_events(region)
        if not events:
            printer.info(f"No events found in region: {region}")
            return True

        # Convert to lowercase for case-insensitive search
        search_term = search_term.lower()
        matching_events = []

        for event in events:
            # Check if the search term appears in the event name, category, or description
            if (
                search_term in event["name"].lower()
                or search_term in event["category"].lower()
                or search_term in event["description"].lower()
            ):
                matching_events.append(event)

        if matching_events:
            printer.info(f"Found {len(matching_events)} matching events in {region}:")
            for event in matching_events:
                printer.info(f"- {event['name']}")
                printer.info(f"  Date: {event['date']} at {event['time']}")
                printer.info(f"  Location: {event['location']}")
                printer.info(f"  Price: ${event['price']} {event['currency']}")
                printer.info(f"  Available: {event['tickets_available']} tickets")
                printer.info(f"  Status: {event['status']}")
                printer.info(f"  Category: {event['category']}")
                printer.info(f"  Description: {event['description']}")
                printer.info("")
        else:
            printer.info(f"No events matching '{search_term}' found in {region}")

        return True

    except Exception as e:
        printer.critical(f"Search failed: {str(e)}")
        return False


def handle_policy(request: Request,node: List) -> bool:
    """Process a policy request with comprehensive validation."""
    if len(node) < 2:
        printer.critical("Invalid policy request format")
        return False

    try:
        assistant = request.app.state.llm_assistant
        event_name = node[1].strip("\"'")  # Remove quotes

        if not event_name:
            printer.critical("Event name cannot be empty")
            return False

        policies = assistant.get_booking_policies(event_name)

        if policies:
            printer.info(f"Booking policies for {event_name}:")
            printer.info(
                f"- Cancellation: {policies.get('cancellation_policy', 'N/A')}"
            )
            printer.info(f"- Payment: {policies.get('payment_policy', 'N/A')}")
            printer.info(f"- Refund: {policies.get('refund_policy', 'N/A')}")
        else:
            printer.info(f"No policies found for {event_name}")

        return True

    except Exception as e:
        printer.critical(f"Failed to retrieve policies: {str(e)}")
        return False

import re
from testcode import jsonEvent
from datetime import date, datetime
from typing import Dict, List, Optional, Tuple, Union
from book_printer import ColorErrorPrinter
import uuid
from dataclasses import dataclass
from enum import Enum, auto

# Constants
MAX_TICKETS_PER_USER = 5
VALID_TICKET_STATUSES = {"booked", "confirmed", "pending", "canceled", "reservations","paid"}


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
    event_name: str, ticket_no: int
) -> Tuple[bool, Optional[str]]:
    """Check if user hasn't exceeded ticket limit for the event."""
    user_tickets = USER_DATA.get(event_name, {}).get("ticketNo", 0)
    if user_tickets + ticket_no > MAX_TICKETS_PER_USER:
        return (
            False,
            f"Cannot book more than {MAX_TICKETS_PER_USER} tickets total for this event",
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
                results.append(handle_view(node[1]))
            else:
                results.append(handle_status(node[1]))
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
        ticket_no, event_name, event_date_str = node[1], node[2], node[3]
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
    can_book, message = check_user_ticket_limit(event_name, ticket_no)
    if not can_book:
        printer.critical(message)
        return False

    # Process booking
    return create_booking(event, event_name, ticket_no)


def create_booking(event: dict, event_name: str, ticket_no: int) -> bool:
    """Create a new booking and update system state."""
    try:
        # Update event tickets
        event["tickets_available"] -= ticket_no

        # Initialize user data if not exists
        if event_name not in USER_DATA:
            USER_DATA[event_name] = {"ticketNo": 0, "bookings": []}

        # Create booking
        booking_id = generate_id("booking")
        tickets = [
            {"ticket_id": generate_id("ticket"), "status": "booked"}
            for _ in range(ticket_no)
        ]

        booking_details = {
            "booking_id": booking_id,
            "tickets": tickets,
            "status": "booked",
            "created_at": datetime.now().isoformat(),
        }

        # Update user data
        USER_DATA[event_name]["bookings"].append(booking_details)
        USER_DATA[event_name]["ticketNo"] += ticket_no

        printer.info(f"Successfully booked {ticket_no} tickets for {event_name}")
        printer.debug(f"Booking details: {booking_details}")
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


def handle_view(view_type: str) -> bool:
    """Display event information or filtered ticket statuses."""

    # Check if viewing an event
    event = find_event(view_type)
    if event:
        print_event_details(event)
        return True

    # Check if viewing ticket statuses
    if view_type in VALID_TICKET_STATUSES:
        return print_tickets_by_status(view_type)

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


def print_tickets_by_status(status: str) -> bool:
    """Print tickets filtered by status."""
    found_data = False

    for event_name, event_data in USER_DATA.items():
        for booking in event_data["bookings"]:
            for ticket in booking["tickets"]:
                if ticket["status"].lower() == status.lower():
                    found_data = True
                    printer.info(
                        f"Event: {event_name}, "
                        f"Booking ID: {booking['booking_id']}, "
                        f"Ticket ID: {ticket['ticket_id']}, "
                        f"Status: {ticket['status'].upper()}"
                    )

    if not found_data:
        printer.info(f"No tickets found with status: {status}")

    return found_data

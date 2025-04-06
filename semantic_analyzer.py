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
USER_DATA = {}


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


def semantic_analyzer(ast: List) -> list:
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
            results.append(f"Error processing command: {str(e)}")
    return results, USER_DATA


def handle_booking(node: List) -> str:
    """Process a booking request with comprehensive validation."""
    if len(node) < 4:
        return "Invalid booking data format"

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
        return f"Invalid booking data format: {str(e)}"

    # Validate date
    if not validate_event_date(event_date):
        return "Event date cannot be in the past"

    # Validate ticket quantity
    is_valid, message = validate_ticket_quantity(ticket_no)
    if not is_valid:
        return message

    # Find and validate event
    event = find_event(event_name)
    if not event:
        return "Event not found"

    # Check ticket availability
    is_available, message = check_ticket_availability(event, ticket_no)
    if not is_available:
        return message

    # Check user ticket limit
    can_book, message = check_user_ticket_limit(event_name, ticket_no, email)
    if not can_book:
       return message

    # Process booking
    return create_booking(event, event_name, ticket_no, email)


def create_booking(event: dict, event_name: str, ticket_no: int, email: str) -> str:
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

        return f"Successfully booked {ticket_no} tickets for event {event_name} for {email}"

        # printer.info(f"Booking details: {USER_DATA}")
    except Exception as e:
        return f"Failed to create booking: {str(e)}"


def handle_status(booking_reference: str) -> str:
    """Display status of bookings or tickets."""
    found = False
    result = []

    for event_name, event_data in USER_DATA.items():
        for booking in event_data["bookings"]:
            if (
                booking_reference.lower() == "tickets"
                or booking["booking_id"] == booking_reference
            ):
                found = True
                result.append(format_booking_status(event_name, booking))

    if not found and booking_reference.lower() != "tickets":
        return f"No booking found with ID: {booking_reference}"

    return "\n".join(result) if result else "No bookings found"


def format_booking_status(event_name: str, booking: dict) -> str:
    """Format booking status as string."""
    status = [
        f"\nEvent: {event_name}",
        f"Booking ID: {booking['booking_id']}",
        f"Created: {booking.get('created_at', 'N/A')}",
        f"Status: {booking.get('status', 'N/A')}",
        "Tickets:",
    ]

    for ticket in booking["tickets"]:
        status.append(f"  - {ticket['ticket_id']}: {ticket['status'].upper()}")

    return "\n".join(status)


def handle_view(node: list) -> str:
    """Display event information or filtered ticket statuses."""
    view_type, email = node[1], node[2]

    # Check if viewing an event
    event = find_event(view_type)
    if event:
        return format_event_details(event)

    # Check if viewing ticket statuses
    if view_type in VALID_TICKET_STATUSES:
        return get_tickets_by_status(view_type, email)

    return f"Invalid view type: {view_type}"


def format_event_details(event: dict) -> str:
    """Format event details as string."""
    return (
        f"\nEvent: {event['name']}\n"
        f"Date: {event['date']} {event.get('time', '')}\n"
        f"Description: {event.get('description', 'N/A')}\n"
        f"Location: {event.get('location', 'N/A')}\n"
        f"Tickets available: {event['tickets_available']}"
    )


def get_tickets_by_status(status: str, email: str) -> str:
    """Get tickets filtered by status as string."""
    result = []

    if email not in USER_DATA:
        return f"No tickets found with status: {status.upper()}"

    for event_name, event_data in USER_DATA[email].items():
        for booking in event_data["bookings"]:
            for ticket in booking["tickets"]:
                if ticket["status"].lower() == status.lower():
                    result.append(
                        f"Event: {event_name}, "
                        f"Booking ID: {booking['booking_id']}, "
                        f"Ticket ID: {ticket['ticket_id']}, "
                        f"Status: {ticket['status'].upper()}, "
                        f"Email: {email}"
                    )

    if not result:
        return f"No tickets found with status: {status.upper()}"

    return "\n".join(result)


def handle_fetch(url: str, timeout: float = 10.0) -> str:
    """Fetch data from a URL and update the event data if successful."""
    if not url.startswith(("http://", "https://")):
        return f"Invalid URL format: {url}"

    try:
        response = requests.get(
            url, timeout=timeout, headers={"Accept": "application/json"}
        )
        response.raise_for_status()

        data = response.json()

        if not validate_event_data(data):
            return "Invalid data structure received from API"

        for event in data:
            EVENT_DATA.append(event)
            return f"Successfully fetched and added event: {event.get('name', 'Unnamed event')}"

    except requests.exceptions.Timeout:
        return f"Request timed out after {timeout} seconds"
    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {str(e)}"
    except requests.exceptions.JSONDecodeError:
        return "Invalid JSON response from server"
    except requests.exceptions.RequestException as e:
        return f"Network error occurred: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


def validate_event_data(data: Dict[str, Any]) -> bool:
    """Validate that the fetched data contains required event fields."""
    required_fields = {"name", "date", "tickets_available"}

    if isinstance(data, list):
        return all(validate_event_data(item) for item in data)

    if not isinstance(data, dict):
        return False

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


def handle_region(region: str) -> str:
    """Handle the region of the event."""
    matching_events = [e for e in EVENT_DATA if region.lower() in e["location"].lower()]
    if not matching_events:
        return f"No events found in region: {region}"

    result = [f"\nEvents in region '{region}':", "―" * 40]
    for event in matching_events:
        result.extend(
            [
                f"• Event: {event.get('name', 'Unnamed')}",
                f"  Location: {event['location']}",
                f"  Date: {event.get('date', 'N/A')}",
                f"  Tickets: {event.get('tickets_available', 'N/A')}",
                "―" * 40,
            ]
        )

    return "\n".join(result)


def handle_reservation(node: List) -> str:
    """Process a reservation request with comprehensive validation."""
    if len(node) < 4:
        return "Invalid reservation data format"

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
        return f"Invalid reservation data format: {str(e)}"

    # Validate date
    if not validate_event_date(event_date):
        return "Event date cannot be in the past"

    # Validate ticket quantity
    is_valid, message = validate_ticket_quantity(ticket_no)
    if not is_valid:
        return message

    # Find and validate event
    event = find_event(event_name)
    if not event:
        return "Event not found"

    # Check ticket availability
    is_available, message = check_ticket_availability(event, ticket_no)
    if not is_available:
        return message

    # Check user ticket limit
    can_book, message = check_user_ticket_limit(event_name, ticket_no, email)
    if not can_book:
        return message

    # Process reservation
    return create_reservation(event, event_name, ticket_no, email)


def create_reservation(event: dict, event_name: str, ticket_no: int, email: str) -> str:
    """Create a new reservation and update system state."""
    try:
        # Update event tickets
        event["tickets_available"] -= ticket_no

        if email not in USER_DATA:
            USER_DATA[email] = {}
        if event_name not in USER_DATA[email]:
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

        return f"Successfully reserved {ticket_no} tickets for {event_name}"
    except Exception as e:
        return f"Failed to create reservation: {str(e)}"


def handle_listing() -> str:
    """Handle listing of all available events."""
    if not EVENT_DATA:
        return "No events available"

    result = []
    for event in EVENT_DATA:
        result.append(
            f"Event: {event['name']}\n"
            f"Tickets available: {event['tickets_available']}\n"
            "---"
        )
    return "\n".join(result)


def handle_payment(node) -> str:
    """Handle reservation of tickets for an event by processing payment and updating ticket status."""
    VALID_PAYMENT_TYPES = {"CreditCard", "PayPal", "Crypto"}

    if len(node) < 4 and len(node) < 3:
        return "Invalid node format - missing payment type or booking ID"

    if len(node) == 4:
        booking_id, payment_type, email = node[1], node[2], node[3]

        if payment_type not in VALID_PAYMENT_TYPES:
            return f"Invalid payment type: {payment_type}"

        booking_found = False
        for event_name, event_data in USER_DATA[email].items():
            for booking in event_data.get("bookings", []):
                if booking.get("booking_id") == booking_id:
                    booking_found = True
                    success, message = process_tickets(
                        booking.get("tickets", []), event_name, "paid"
                    )
                    if not success:
                        return message

        if not booking_found:
            return f"Booking ID {booking_id} not found"
    else:
        booking_id, email = node[1], node[2]
        for event_name, event_data in USER_DATA[email].items():
            for booking in event_data.get("bookings", []):
                if booking.get("booking_id") == booking_id:
                    booking_found = True
                    success, message = process_tickets(
                        booking.get("tickets", []), event_name, "cancel"
                    )
                    if not success:
                        return message
    return "Payment processed successfully"


def process_tickets(tickets: list, event_name: str, status: str) -> Tuple[bool, str]:
    """Process individual tickets for a booking."""
    if not tickets:
        return False, f"No tickets found for booking in event {event_name}"

    result = []
    for ticket in tickets:
        if ticket.get("status") != status:
            try:
                ticket["status"] = status
                result.append(
                    f"Ticket {ticket.get('ticket_id', 'UNKNOWN')} "
                    f"for {event_name} has been {status}"
                )
            except Exception as e:
                return False, f"Failed to process ticket: {str(e)}"

    return True, "\n".join(result)


##* AI -Semantics and Analyzer *##


def handle_search(request: Request, node: List) -> str:
    """Process a search request with comprehensive validation."""
    if len(node) < 3:
        return "Invalid search data format"

    try:
        assistant = request.app.state.llm_assistant
        search_term, region = node[1], node[2]

        # Remove quotes if present
        search_term = search_term.strip("\"'")
        region = region.strip("\"'")

        if not search_term:
            return "Search term cannot be empty"

        if not region:
            return "Region cannot be empty"

        events = assistant.get_available_events(region)
        if not events:
            return f"No events found in region: {region}"

        search_term = search_term.lower()
        matching_events = []

        for event in events:
            if (
                search_term in event["name"].lower()
                or search_term in event["category"].lower()
                or search_term in event["description"].lower()
            ):
                matching_events.append(event)

        if not matching_events:
            return f"No events matching '{search_term}' found in {region}"

        result = [f"Found {len(matching_events)} matching events in {region}:"]
        for event in matching_events:
            result.extend(
                [
                    f"- {event['name']}",
                    f"  Date: {event['date']} at {event['time']}",
                    f"  Location: {event['location']}",
                    f"  Price: ${event['price']} {event['currency']}",
                    f"  Available: {event['tickets_available']} tickets",
                    f"  Status: {event['status']}",
                    f"  Category: {event['category']}",
                    f"  Description: {event['description']}",
                    "",
                ]
            )

        return "\n".join(result)

    except Exception as e:
        return f"Search failed: {str(e)}"


def handle_policy(request: Request, node: List) -> str:
    """Process a policy request with comprehensive validation."""
    if len(node) < 2:
        return "Invalid policy request format"

    try:
        assistant = request.app.state.llm_assistant
        event_name = node[1].strip("\"'")

        if not event_name:
            return "Event name cannot be empty"

        policies = assistant.get_booking_policies(event_name)

        if not policies:
            return f"No policies found for {event_name}"

        return (
            f"Booking policies for {event_name}:\n"
            f"- Cancellation: {policies.get('cancellation_policy', 'N/A')}\n"
            f"- Payment: {policies.get('payment_policy', 'N/A')}\n"
            f"- Refund: {policies.get('refund_policy', 'N/A')}"
        )

    except Exception as e:
        return f"Failed to retrieve policies: {str(e)}"


# def print_booking_status(event_name: str, booking: dict) -> None:
#     """Print formatted booking status."""
#     printer.info(
#         f"\nEvent: {event_name}\n"
#         f"Booking ID: {booking['booking_id']}\n"
#         f"Created: {booking.get('created_at', 'N/A')}\n"
#         f"Status: {booking.get('status', 'N/A')}\n"
#         "Tickets:"
#     )

#     for ticket in booking["tickets"]:
#         printer.info(f"  - {ticket['ticket_id']}: {ticket['status'].upper()}")

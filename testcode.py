dataErrors = """
BOOK 2 TICKETS FOR "COLDPLAY CONCERT" ON
BOOK hey TICKETS FOR "COLDPLAY CONCERT" ON 2025-09-12
BOOK 5 TICKETS FOR 9 ON 2025-08-13
BOOK 6.9 TICKETS FOR "COLDPLAY CONCERT" ON 2025-05-14
BOOK 0 TICKETS FOR "COLDPLAY CONCERT" ON 2025-09-12
STATUS OF 2
STATUS OF booking_12345
SHOW MY ertyui
SHOW MY wertyu BOOKINGS
SHOW MY rtyuil TICKETS
SHOW MY tyuighjk BOOKINGS
SORT TICKETS BY WQERT
SELECT TICKET 5678
BOOK 3 TICKETS FOR "Jazz Festival 2025" ON  FOR black@gmail.com
BOOK 3 TICKETS FOR  ON 2025-06-01 FOR black@gmail.com
BOOK  TICKETS FOR "Jazz Festival 2025" ON 2025-06-01 FOR black@gmail.com
"""

data = """
BOOK 3 TICKETS FOR "Jazz Festival 2025" ON 2025-06-01 FOR black@gmail.com
"""
# PAY FOR ALL BOOKINGS booking_5c67f3e1 USING CreditCard
# CANCEL BOOKING booking_5c67f3e1
# FETCH TICKETS FROM API http://127.0.0.1:8000/api/events
# LIST ALL EVENTS
# SHOW AVAILABLE TICKETS IN "San Francisco"
# RESERVE 3 TICKETS FOR "Tech Conference 2025" ON 2025-07-15
# BOOK 2 TICKETS FOR "Blockchain Summit" ON 2025-06-01

# SHOW AVAILABLE TICKETS FOR "Jazz Festival 2025"
# SHOW MY RESERVATIONS
# SHOW MY CONFIRMED BOOKINGS
# SHOW MY PAID TICKETS
# SHOW MY CANCELED BOOKINGS
# STATUS OF BOOKING booking_59c133d1
# STATUS OF TICKETS
# STATUS OF BOOKING booking_59c133d2
# BOOK 1 TICKETS FOR "Jazz Festival 2025" ON 2025-06-01
# BOOK 2 TICKETS FOR "COLDPLAY CONCERT" ON 2025-09-12
# USER INPUT: BOOK 2 TICKETS FOR "COLDPLAY CONCERT" ON 2025-03-23
# BOOK 5 TICKETS FOR "COLDPLAY CONCERT" ON 2025-08-13
# BOOK 5 TICKETS FOR "COLDPLAY CONCERT" ON 2025-04-14
# STATUS OF TICKETS
# SELECT TICKET ticket_1234
# SORT TICKETS BY 12.98
# SORT TICKETS BY 2025-08-13
# RESERVE 3 FOR "Coldplay Concert" ON 2025-07-15
# LIST all events
# PAY FOR BOOKING booking_12346 USING CreditCard


jsonEvent = [
    {
        "id": 1,
        "name": "Tech Conference 2025",
        "location": "San Francisco, CA",
        "date": "2025-06-15",
        "time": "10:00 AM",
        "tickets_available": 150,
        "price": 99.99,
        "currency": "USD",
        "status": "Available",
        "organizer": "Tech World Inc.",
        "category": "Technology",
        "description": "A conference for tech enthusiasts covering AI, Web3, and more.",
    },
    {
        "id": 2,
        "name": "Jazz Festival 2025",
        "location": "New Orleans, LA",
        "date": "2025-07-22",
        "time": "6:00 PM",
        "tickets_available": 200,
        "price": 49.99,
        "currency": "USD",
        "status": "Available",
        "organizer": "Jazz Association",
        "category": "Music",
        "description": "Enjoy live jazz performances from world-renowned artists.",
    },
    {
        "id": 3,
        "name": "Blockchain Summit",
        "location": "New York, NY",
        "date": "2025-08-10",
        "time": "9:00 AM",
        "tickets_available": 80,
        "price": 129.99,
        "currency": "USD",
        "status": "Sold Out",
        "organizer": "Crypto Innovations",
        "category": "Finance",
        "description": "A deep dive into blockchain, DeFi, and the future of crypto.",
    },
]

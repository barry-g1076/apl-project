dataErrors = """
BOOK 2 TICKETS FOR "COLDPLAY CONCERT" ON
BOOK hey TICKETS FOR "COLDPLAY CONCERT" ON 2025-09-12
BOOK 5 TICKETS FOR 9 ON 2025-08-13
BOOK 6.9 TICKETS FOR "COLDPLAY CONCERT" ON 2025-05-14
BOOK 0 TICKETS FOR "COLDPLAY CONCERT" ON 2025-09-12
STATUS OF 2
STATUS OF booking_12345
SORT TICKETS BY WQERT
SELECT TICKET 5678
BOOK 3 TICKETS FOR "Jazz Festival 2025" ON  FOR black@gmail.com
BOOK 3 TICKETS FOR  ON 2025-06-01 FOR black@gmail.com
BOOK  TICKETS FOR "Jazz Festival 2025" ON 2025-06-01 FOR black@gmail.com
SHOW ertyui
SHOW wertyu BOOKINGS FOR black@gmail.com
SHOW rtyuil TICKETS FOR black@gmail.com
SHOW tyuighjk BOOKINGS FOR black@gmail.com
RESERVE 3 TICKETS FOR "Jazz Festival 2025" ON FOR 
RESERVE 3 TICKETS FOR "Jazz Festival 2025" ON 2025-06-01 FOR bgrteasdfghjk
RESERVE  TICKETS FOR "Jazz Festival 2025" ON 2025-06-01 FOR black@gmail.com
PAY FOR ALL BOOKINGS ertyui USING CreditCard FOR black@gmail.com
PAY FOR ALL BOOKINGS booking_59c133d1 USING sdfghj FOR black@gmail.com
PAY FOR ALL BOOKINGS booking_59c133d1 USING CreditCard FOR 
"""

data = """
BOOK 3 TICKETS FOR "Jazz Festival 2025" ON 2025-06-01 FOR black@gmail.com
PAY FOR ALL BOOKINGS booking_59c133d1 USING CreditCard FOR black@gmail.com
RESERVE 5 TICKETS FOR "Blockchain Summit" ON 2025-06-01 FOR black@gmail.com
SHOW RESERVATIONS FOR  black@gmail.com
SHOW CONFIRMED BOOKINGS FOR black@gmail.com
SHOW PAID TICKETS FOR  black@gmail.com
SHOW CANCELED BOOKINGS FOR black@gmail.com
PAY FOR ALL BOOKINGS booking_5c67f3e1 USING CreditCard FOR black@gmail.com
FETCH TICKETS FROM API http://127.0.0.1:8000/api/events
CANCEL BOOKING booking_5c67f3e1 for black@gmail.com
"""
# LIST ALL EVENTS
# SHOW AVAILABLE TICKETS IN "San Francisco"
# RESERVE 3 TICKETS FOR "Tech Conference 2025" ON 2025-07-15
# BOOK 2 TICKETS FOR "Blockchain Summit" ON 2025-06-01
# STATUS OF BOOKING booking_59c133d1 FOR black@gmail.com
# STATUS OF TICKETS FOR black@gmail.com
# STATUS OF BOOKING booking_59c133d2 FOR black@gmail.com

# SHOW AVAILABLE TICKETS FOR "Jazz Festival 2025"
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

import re
from datetime import *
from book_parser import parser

MAX_TICKETS_PER_USER = 5


def semantic_analyzer(ast):
    working = False
    for x in ast:
        if x == None:
            continue
        elif x[0] == "booking":
            working = handle_booking(x)
        else:
            working = True
            continue
    return working


def handle_booking(node):
    current_date = date.today()
    ticketNo, event, eventDate = node[1], node[2], node[3]
    eventDate = datetime.strptime(eventDate, "%Y-%m-%d").date()
    if eventDate < current_date:
        raise ValueError("Booking date cannot be in the past")
    if ticketNo <= 0:
        raise ValueError("Number of tickets can not be less than or equal to 0")
    if ticketNo > MAX_TICKETS_PER_USER:  # todo: Update to be dynamic later on
        raise ValueError("Number of tickets can not be more than 5")
    return True


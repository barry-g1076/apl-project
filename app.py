from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict
import json  # Add JSON module for serialization
from book_parser import parse_input
from fastapi.templating import Jinja2Templates

from llm_integration import LLMBookingAssistant
import os
from dotenv import load_dotenv

load_dotenv()
# Load environment variables from .env file
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

app = FastAPI()
app.state.llm_assistant = LLMBookingAssistant(api_key=api_key)
# Mount static files directory (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Optional: Mount node_modules if you want to serve frontend dependencies directly
app.mount("/node_modules", StaticFiles(directory="node_modules"), name="node_modules")
templates = Jinja2Templates(directory="templates")
# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic model for event validation and documentation
class Event(BaseModel):
    id: int
    name: str
    location: str
    date: str
    time: str
    tickets_available: int
    price: float
    currency: str
    status: str
    organizer: str
    category: str
    description: str


# Original events data converted to a dictionary for O(1) lookups
events_data = [
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
    {
        "id": 4,
        "name": "Food & Wine Festival",
        "location": "Napa Valley, CA",
        "date": "2025-09-12",
        "time": "11:00 AM",
        "tickets_available": 300,
        "price": 79.99,
        "currency": "USD",
        "status": "Available",
        "organizer": "Gourmet Experiences LLC",
        "category": "Food & Drink",
        "description": "Sample exquisite wines and gourmet dishes from top chefs and wineries.",
    },
    {
        "id": 5,
        "name": "Marathon 2025",
        "location": "Chicago, IL",
        "date": "2025-10-08",
        "time": "7:00 AM",
        "tickets_available": 10000,
        "price": 120.00,
        "currency": "USD",
        "status": "Available",
        "organizer": "Run Nation",
        "category": "Sports",
        "description": "Annual city marathon with routes through Chicago's most scenic neighborhoods.",
    },
    {
        "id": 6,
        "name": "Digital Art Exhibition",
        "location": "Miami, FL",
        "date": "2025-11-15",
        "time": "10:00 AM",
        "tickets_available": 500,
        "price": 25.50,
        "currency": "USD",
        "status": "Available",
        "organizer": "Modern Art Collective",
        "category": "Art",
        "description": "Immersive digital art experience featuring works from emerging NFT artists.",
    },
    {
        "id": 7,
        "name": "Startup Pitch Competition",
        "location": "Austin, TX",
        "date": "2025-05-20",
        "time": "1:00 PM",
        "tickets_available": 150,
        "price": 45.00,
        "currency": "USD",
        "status": "Limited Availability",
        "organizer": "Venture Capital Network",
        "category": "Business",
        "description": "Watch promising startups pitch to top investors for funding opportunities.",
    },
    {
        "id": 8,
        "name": "Yoga Retreat",
        "location": "Sedona, AZ",
        "date": "2025-04-05",
        "time": "8:00 AM",
        "tickets_available": 30,
        "price": 299.99,
        "currency": "USD",
        "status": "Available",
        "organizer": "Mindful Living",
        "category": "Wellness",
        "description": "Weekend retreat with daily yoga sessions, meditation, and healthy meals.",
    },
    {
        "id": 9,
        "name": "Comedy Night Special",
        "location": "New York, NY",
        "date": "2025-08-22",
        "time": "8:30 PM",
        "tickets_available": 200,
        "price": 35.75,
        "currency": "USD",
        "status": "Available",
        "organizer": "Laugh Factory",
        "category": "Entertainment",
        "description": "An evening of stand-up comedy featuring top comedians from Netflix specials.",
    },
    {
        "id": 10,
        "name": "Science Fair Expo",
        "location": "Boston, MA",
        "date": "2025-03-30",
        "time": "9:00 AM",
        "tickets_available": 400,
        "price": 15.00,
        "currency": "USD",
        "status": "Available",
        "organizer": "STEM Education Foundation",
        "category": "Education",
        "description": "Interactive science exhibits and workshops for all ages.",
    },
    {
        "id": 11,
        "name": "Film Festival",
        "location": "Park City, UT",
        "date": "2025-01-18",
        "time": "10:00 AM",
        "tickets_available": 1000,
        "price": 50.00,
        "currency": "USD",
        "status": "Early Bird",
        "organizer": "Independent Cinema Guild",
        "category": "Film",
        "description": "Premieres of independent films with Q&A sessions with directors.",
    },
    {
        "id": 12,
        "name": "Gaming Tournament",
        "location": "Las Vegas, NV",
        "date": "2025-07-05",
        "time": "12:00 PM",
        "tickets_available": 800,
        "price": 65.25,
        "currency": "USD",
        "status": "Available",
        "organizer": "eSports United",
        "category": "Gaming",
        "description": "National championship for popular competitive video games with cash prizes.",
    },
    {
        "id": 13,
        "name": "Literary Festival",
        "location": "Portland, OR",
        "date": "2025-09-28",
        "time": "10:00 AM",
        "tickets_available": 350,
        "price": 29.99,
        "currency": "USD",
        "status": "Available",
        "organizer": "Bookworms Society",
        "category": "Literature",
        "description": "Meet famous authors, attend readings, and participate in writing workshops.",
    },
    {
        "id": 14,
        "name": "Sustainable Living Expo",
        "location": "Seattle, WA",
        "date": "2025-04-22",
        "time": "9:30 AM",
        "tickets_available": 600,
        "price": 20.00,
        "currency": "USD",
        "status": "Available",
        "organizer": "Green Future Initiative",
        "category": "Environment",
        "description": "Learn about eco-friendly technologies and sustainable living practices.",
    },
    {
        "id": 15,
        "name": "Broadway Musical",
        "location": "New York, NY",
        "date": "2025-12-05",
        "time": "7:30 PM",
        "tickets_available": 50,
        "price": 149.99,
        "currency": "USD",
        "status": "Limited Availability",
        "organizer": "Great White Way Productions",
        "category": "Theater",
        "description": "Tony Award-winning musical with original cast members.",
    },
]

events_dict: Dict[int, Event] = {event["id"]: event for event in events_data}


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def safe_send(self, websocket: WebSocket, message: str):
        try:
            parsed = parse_input(message)
            await websocket.send_text(json.dumps(parsed))
        except RuntimeError as e:
            print(f"Connection closed, removing: {e}")
            self.disconnect(websocket)
        except Exception as e:
            print(f"Error sending message: {e}")
            self.disconnect(websocket)

    async def broadcast(self, message: str):
        closed_connections = []
        for connection in self.active_connections:
            try:
                parsed = parse_input(message)
                await connection.send_text(json.dumps(parsed))
            except (RuntimeError, WebSocketDisconnect):
                closed_connections.append(connection)
            except Exception as e:
                print(f"Broadcast error: {e}")
                closed_connections.append(connection)
        # Clean up closed connections
        for connection in closed_connections:
            self.disconnect(connection)

manager = ConnectionManager()

class ChatConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            print("connections")
            response = app.state.llm_assistant.chat(message)
            await connection.send_text(response)


chat_manager = ChatConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})

@app.get("/api/events", response_model=List[Event])
async def get_events():
    """
    Retrieve a list of all upcoming events with complete details.
    """
    return events_data


@app.get("/api/events/{event_id}", response_model=Event)
async def get_event(event_id: int):
    """
    Get detailed information about a specific event by ID.

    - **event_id**: The unique identifier of the event (1-15)
    """
    event = events_dict.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time communication.

    Clients can connect to send and receive live updates.
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("A client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)

@app.websocket("/chat")
async def websocket_chat(websocket: WebSocket):
    """ WebSocket endpoint for real-time chat communication."""
    await chat_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await chat_manager.broadcast(data)
    except WebSocketDisconnect:
        chat_manager.disconnect(websocket)
        await chat_manager.broadcast("A client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        chat_manager.disconnect(websocket)

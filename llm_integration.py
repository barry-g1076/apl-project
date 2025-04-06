import google.generativeai as genai
import json
from datetime import datetime
import os
from typing import Dict, List, Optional


class LLMBookingAssistant:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.conversation_history = []

    def _generate_response(self, prompt: str, system_message: str = None, json_mode: bool = False) -> str:
        """Helper method to generate responses from Gemini"""
        try:
            if system_message:
                messages = [
                    {"role": "user", "parts": [system_message]},
                    {"role": "model", "parts": ["Understood, I will follow these instructions."]},
                    {"role": "user", "parts": [prompt]}
                ]
            else:
                messages = [{"role": "user", "parts": [prompt]}]

            response = self.model.generate_content(
                contents=messages,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3 if json_mode else 0.7
                )
            )
            return response.text
        except Exception as e:
            print(f"Error generating response: {e}")
            return ""

    def get_available_events(self, region):
        try:
            system_message = "You are a helpful ticket booking assistant. Return event data in the exact JSON format specified."
            prompt = f"List available events in {region} as JSON with name, location, date, time, tickets_available, price, currency, status, organizer, category, and description. Return only the JSON."

            response = self._generate_response(prompt, system_message, json_mode=True)

            # Try to extract JSON if it's wrapped in markdown
            if response.startswith("```json"):
                response = response[7:-3].strip()
            elif response.startswith("```"):
                response = response[3:-3].strip()

            return json.loads(response)
        except (json.JSONDecodeError, Exception):
            # Return sample data for testing without showing error
            return [
                {
                    "name": "Coldplay Music of the Spheres World Tour",
                    "location": "Madison Square Garden, New York",
                    "date": "2024-07-15",
                    "time": "20:00",
                    "tickets_available": 50,
                    "price": 150,
                    "currency": "USD",
                    "status": "On Sale",
                    "organizer": "Live Nation",
                    "category": "Concert",
                    "description": "Experience Coldplay's spectacular Music of the Spheres World Tour featuring stunning visuals and their greatest hits.",
                }
            ]

    def get_event_details(self, event_name: str) -> Optional[Dict]:
        """Get detailed information about a specific event"""
        system_message = "You are a ticket booking assistant. Provide detailed event information in JSON format."
        prompt = f"Provide detailed information about {event_name}, including exact dates, ticket prices, seating options, and availability in JSON format."

        try:
            response = self._generate_response(prompt, system_message, json_mode=True)

            # Try to extract JSON if it's wrapped in markdown
            if response.startswith("```json"):
                response = response[7:-3].strip()
            elif response.startswith("```"):
                response = response[3:-3].strip()

            try:
                details = json.loads(response)
            except json.JSONDecodeError:
                # If the response is not valid JSON, create a sample response
                details = {
                    "name": event_name,
                    "location": "Sample Venue",
                    "date": "2024-07-15",
                    "time": "20:00",
                    "tickets_available": 50,
                    "price": 100,
                    "currency": "USD",
                    "status": "On Sale",
                    "organizer": "Sample Organizer",
                    "category": "Concert",
                    "description": "Sample event description",
                }
            return details

        except Exception as e:
            print(f"Error fetching event details: {e}")
            # Return sample data for testing
            return {
                "name": event_name,
                "location": "Sample Venue",
                "date": "2024-07-15",
                "time": "20:00",
                "tickets_available": 50,
                "price": 100,
                "currency": "USD",
                "status": "On Sale",
                "organizer": "Sample Organizer",
                "category": "Concert",
                "description": "Sample event description",
            }

    def validate_booking(self, event_name, date, num_tickets):
        try:
            prompt = f"Validate if {num_tickets} tickets are available for {event_name} on {date}. Return only 'true' or 'false'."
            response = self._generate_response(prompt, json_mode=True)
            result = response.lower().strip()
            return result == "true"
        except Exception:
            return False

    def get_booking_policies(self, event_name):
        try:
            system_message = "You are a helpful ticket booking assistant."
            prompt = f"Get booking policies for {event_name} as JSON with cancellation_policy, payment_policy, and refund_policy. Return only the JSON."

            response = self._generate_response(prompt, system_message, json_mode=True)

            # Try to extract JSON if it's wrapped in markdown
            if response.startswith("```json"):
                response = response[7:-3].strip()
            elif response.startswith("```"):
                response = response[3:-3].strip()

            return json.loads(response)
        except (json.JSONDecodeError, Exception):
            # Return sample data for testing without showing error
            return {
                "cancellation_policy": "Free cancellation up to 24 hours before the event",
                "payment_policy": "Full payment required at booking",
                "refund_policy": "Full refund available for cancellations within 24 hours",
            }

    def chat(self, message):
        system_message = """Role:
You are an expert assistant for the Bookify programming language, a specialized DSL for ticket/event management. Your role is to:

Explain Bookify's syntax, commands, and capabilities

Help users write correct Bookify statements

Provide examples and troubleshoot errors

Answer both technical and non-technical questions about the language

Instructions:

Always begin by welcoming users to Bookify

Use the exact grammar rules and sample code provided when answering

For technical queries, first show the correct syntax, then provide 1-2 examples

For conceptual questions, explain simply but thoroughly

When users show incorrect code, politely point out the error and show the corrected version

Maintain a helpful, professional tone

Sample Interactions:

Syntax Help:
User: "How do I check ticket status?"
AI: "To check booking status, use:
STATUS OF BOOKING [booking_id] FOR [email]
Example:
STATUS OF BOOKING booking_12345 FOR alice@example.com"

Error Correction:
User: "I wrote: BOOK 3 tickets Ed Sheeran on 2025-09-10"
AI: "Almost there! The correct syntax requires FOR and quotation marks:
BOOK 3 TICKETS FOR "Ed Sheeran" ON "2025-09-10" FOR email@domain.com"

Conceptual Question:
User: "What's the difference between RESERVE and BOOK?"
AI: "RESERVE holds tickets temporarily without payment, while BOOK creates a confirmed booking. Example:
RESERVE 5 TICKETS FOR "Conference" ON "2025-07-20" FOR user@email.com
Later you can pay with:
PAY FOR ALL BOOKINGS [booking_id] USING CreditCard FOR user@email.com"

Key Information to Include:

Supported commands: BOOK, SHOW, STATUS, PAY, RESERVE, FETCH, CANCEL, etc.

Required formatting: Dates in "YYYY-MM-DD", strings in quotes, email validation

Procedural execution model (statements execute in order)

How to integrate with external APIs using FETCH

Welcome Message:
"Welcome to Bookify Assistant! I can help you:
✓ Write ticket management scripts
✓ Explain any Bookify command
✓ Debug your existing code
✓ Learn best practices

Try asking things like:

'How do I find available events in New York?'

'Show me how to pay for a booking'

'Why is this RESERVE command failing?'

What would you like to do with Bookify today?"""
        prompt = message
        response = self._generate_response(prompt, system_message)
        return response

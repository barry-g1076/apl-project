import { createChatWebSocket, sendChatMessage, on } from "./customWebSocket.js";


createChatWebSocket();
// Function to handle message sending and AI response
async function sendMessage() {
    const chatInput = document.getElementById("chatInput");
    const chatArea = document.getElementById("chatArea");
    const message = chatInput.value.trim();
    sendChatMessage(message)
    if (message) {
        // User message
        chatArea.innerHTML += `<div class="message user-message"><strong>You:</strong> ${message}</div>`;

        // Scroll to bottom of chat
        chatArea.scrollTop = chatArea.scrollHeight;

        // Simulate AI thinking with dots animation
        const thinkingMsg = document.createElement('div');
        thinkingMsg.className = 'message ai-message thinking';
        thinkingMsg.innerHTML = '<strong>Bookify AI:</strong> <span class="typing-dots">Thinking<span>.</span><span>.</span><span>.</span></span>';
        chatArea.appendChild(thinkingMsg);
        chatArea.scrollTop = chatArea.scrollHeight;

        // Get AI response (simulated for demo)
        on('message', (message) => {
            if (!thinkingMsg || !document.contains(thinkingMsg)) {
                return; // Exit the function
            }
            // Remove thinking message
            chatArea.removeChild(thinkingMsg);

            // Add AI response
            chatArea.innerHTML += `<div class="message ai-message"><strong>Bookify AI:</strong> ${message}</div>`;

            // Scroll to bottom
            chatArea.scrollTop = chatArea.scrollHeight;
        });
        

        // Clear the input
        chatInput.value = "";
    }
}

// Function to get a simulated AI response based on keywords
function getSimulatedResponse(message) {
    const lowerMsg = message.toLowerCase();

    if (lowerMsg.includes('book') || lowerMsg.includes('ticket') || lowerMsg.includes('reserve')) {
        return "I can help you book tickets! Just type your destination, date, and number of passengers in the Bookify Compiler, or ask me for available routes.";
    } else if (lowerMsg.includes('schedule') || lowerMsg.includes('time') || lowerMsg.includes('when')) {
        return "Our schedules are updated daily. You can check availability by running 'listEvents()' in the compiler, or tell me your travel date and I'll assist you.";
    } else if (lowerMsg.includes('cancel') || lowerMsg.includes('refund')) {
        return "To cancel a booking, use 'cancelBooking(bookingId)' in the compiler. Refunds are processed within 3-5 business days.";
    } else if (lowerMsg.includes('hello') || lowerMsg.includes('hi') || lowerMsg.includes('hey')) {
        return "Hello! How can I assist with your travel plans today?";
    } else if (lowerMsg.includes('help')) {
        return "I can help with bookings, schedules, cancellations, and travel information. Type what you need or use the Bookify Compiler for direct commands.";
    } else {
        return "I'm here to help with your booking needs. Would you like to check availability, make a reservation, or learn about our services?";
    }
}

// Function to insert emoji into chat input
function insertEmoji(emoji) {
    const chatInput = document.getElementById("chatInput");
    chatInput.value += emoji;
    chatInput.focus();
}

// Function to speak the AI's response
function speakAIResponse() {
    const aiMessages = document.querySelectorAll('.ai-message');
    if (aiMessages.length === 0) return;

    const latestMessage = aiMessages[aiMessages.length - 1];
    const messageText = latestMessage.textContent.replace("Bookify AI:", "").trim();

    if (messageText && !messageText.includes("Thinking")) {
        const speech = new SpeechSynthesisUtterance(messageText);
        speech.lang = 'en-US';
        window.speechSynthesis.speak(speech);

        // Visual indication that speech is happening
        document.getElementById("speakButton").innerHTML = '<i class="fas fa-volume-up fa-pulse"></i> Speaking...';

        speech.onend = function () {
            document.getElementById("speakButton").innerHTML = '<i class="fas fa-volume-up"></i> Listen to Response';
        };
    }
}

// Process Bookify Language input
function processTicketLang() {
    const inputText = document.getElementById("ticketLangInput").value.trim();
    const outputArea = document.getElementById("outputArea");
    const historyArea = document.getElementById("bookingHistoryText");
    let output = '';
    let historyEntry = '';
    const timestamp = new Date().toLocaleString();

    if (inputText.includes('listEvents')) {
        output = `Available Events:
- Jamaica Jazz Festival | June 15, 2025 | Kingston
- Beach Concert Series | July 10-12, 2025 | Montego Bay
- International Film Festival | August 5-8, 2025 | Ocho Rios
- Cultural Heritage Exhibition | September 20, 2025 | Port Antonio`;
        historyEntry = `[${timestamp}] COMMAND: listEvents()\n`;
    }
    else if (inputText.includes('reserveTicket')) {
        // Extract event name using regex if possible
        let eventMatch = inputText.match(/reserveTicket\(['"](.+?)['"]/) || ['', 'Event'];
        let eventName = eventMatch[1];
        output = `✅ Success: Ticket reserved for "${eventName}"
Booking ID: BK-${Math.floor(10000 + Math.random() * 90000)}
Please check your email for confirmation.`;
        historyEntry = `[${timestamp}] COMMAND: ${inputText}\n`;
    }
    else if (inputText.includes('cancelBooking')) {
        output = '✅ Booking cancelled successfully. Refund will be processed in 3-5 business days.';
        historyEntry = `[${timestamp}] COMMAND: ${inputText}\n`;
    }
    else if (inputText.includes('checkAvailability')) {
        output = `Available seats: 28
Ticket types:
- Standard: $45
- Premium: $75
- VIP: $120 (3 remaining)`;
        historyEntry = `[${timestamp}] COMMAND: ${inputText}\n`;
    }
    else {
        output = '❌ Error: Unknown command or incorrect syntax. Try listEvents(), reserveTicket(), or checkAvailability().';
        historyEntry = `[${timestamp}] ERROR: Invalid command - ${inputText}\n`;
    }

    outputArea.textContent = output;
    historyArea.value = historyEntry + (historyArea.value ? '\n' + historyArea.value : '');
}

// Save Bookify Commands to localStorage
function saveTicketLang() {
    const ticketLangInput = document.getElementById("ticketLangInput").value;
    localStorage.setItem("savedBookifyCommands", ticketLangInput);

    // Show save confirmation
    const outputArea = document.getElementById("outputArea");
    outputArea.textContent = "✅ Commands saved successfully!";

    setTimeout(() => {
        outputArea.textContent = "Commands are stored in your browser and will be available next time.";
    }, 2000);
}

// Clear input area
function eraseTicketLang() {
    document.getElementById("ticketLangInput").value = "";
    document.getElementById("outputArea").textContent = "";
}

// Clear booking history
function clearHistory() {
    document.getElementById("bookingHistoryText").value = "";
}

// Auto-resize the textarea input for chat
function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = (textarea.scrollHeight) + 'px';
}

// Load saved commands if they exist
function loadSavedCommands() {
    const savedCommands = localStorage.getItem("savedBookifyCommands");
    if (savedCommands) {
        document.getElementById("ticketLangInput").value = savedCommands;
    }
}

// Event listeners setup
document.addEventListener("DOMContentLoaded", function () {
    // Chat input auto-resize
    const chatInput = document.getElementById("chatInput");
    if (chatInput) {
        chatInput.addEventListener("input", function () {
            autoResizeTextarea(this);
        });
    }

    // Attach event listeners to buttons
    const sendButton = document.getElementById("sendButton");
    const speakButton = document.getElementById("speakButton");
    const runButton = document.getElementById("runButton");
    const saveButton = document.getElementById("saveButton");
    const eraseButton = document.getElementById("eraseButton");
    const clearHistoryButton = document.getElementById("clearHistoryButton");

    if (sendButton) sendButton.addEventListener("click", sendMessage);
    if (speakButton) speakButton.addEventListener("click", speakAIResponse);
    if (runButton) runButton.addEventListener("click", processTicketLang);
    if (saveButton) saveButton.addEventListener("click", saveTicketLang);
    if (eraseButton) eraseButton.addEventListener("click", eraseTicketLang);
    if (clearHistoryButton) clearHistoryButton.addEventListener("click", clearHistory);

    // Allow sending messages with Enter key
    if (chatInput) {
        chatInput.addEventListener("keypress", function (e) {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    }

    // Load any saved commands
    loadSavedCommands();
});
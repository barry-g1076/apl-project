let socket = null;
let reconnectAttempts = 0;
const maxReconnectAttempts = 5;
const reconnectInterval = 3000;
const messageQueue = [];

function createWebSocket() {
    if (socket) {
        console.warn('WebSocket already exists');
        return;
    }
    socket = new WebSocket("ws://localhost:8000/ws");
    // console.log("hi")

    socket.addEventListener('open', (event) => {
        console.log("[open] Connection established");
        reconnectAttempts = 0;
        // Process queued messages
        while (messageQueue.length > 0) {
            const message = messageQueue.shift();
            socket.send(message);
        }
    });

    socket.addEventListener('message', (event) => {
        try {
            const output = document.getElementById('outputArea');
            const historyOutput = document.getElementById('bookingHistoryText');
            if (!output || !historyOutput) return;

            // Parse incoming data
            const data = typeof event.data === 'string' ? JSON.parse(event.data) : event.data;
            console.log('Received WebSocket message:', data);

            // Process main message output
            if (data.success || data.errors) {
                const messageContainer = document.createElement('div');
                messageContainer.classList.add('message-container');

                if (data.success && data.result) {
                    // Process successful results
                    const results = Array.isArray(data.result) ? data.result : [data.result];
                    results.filter(result => result != null).forEach(result => {
                        const resultElement = document.createElement('p');
                        resultElement.textContent = result;
                        resultElement.classList.add('message-success');
                        messageContainer.appendChild(resultElement);
                    });
                } else if (data.errors) {
                    // Process errors
                    const errors = Array.isArray(data.errors) ? data.errors :
                        (data.errors ? [data.errors] : ['Unknown error']);
                    errors.forEach(error => {
                        const errorElement = document.createElement('p');
                        errorElement.textContent = error;
                        errorElement.classList.add('message-error');
                        messageContainer.appendChild(errorElement);
                    });
                }

                // Append messages if we have content
                if (messageContainer.children.length > 0) {
                    output.appendChild(messageContainer);
                    output.scrollTop = output.scrollHeight;
                }
            }

            // Process booking history if present
            if (data.booking_history && Object.keys(data.booking_history).length > 0) {
                let historyText = '';

                for (const [eventName, eventData] of Object.entries(data.booking_history)) {
                    historyText += `Event: ${eventName}\n`;
                    historyText += `Total Tickets: ${eventData.ticketNo}\n`;

                    eventData.bookings.forEach((booking, index) => {
                        historyText += `\nBooking ${index + 1} (ID: ${booking.booking_id}):\n`;

                        booking.tickets.forEach(ticket => {
                            historyText += `- Ticket ${ticket.ticket_id}: ${ticket.status}\n`;
                        });
                    });

                    historyText += '\n' + '─'.repeat(40) + '\n\n';
                }

                historyOutput.value = historyText.trim();
                historyOutput.scrollTop = historyOutput.scrollHeight;
            }

        } catch (error) {
            console.error('Error processing WebSocket message:', error);

            // Display error to user
            const output = document.getElementById('outputArea');
            if (output) {
                const errorElement = document.createElement('p');
                errorElement.textContent = 'Error processing server response';
                errorElement.classList.add('message-error');
                output.appendChild(errorElement);
                output.scrollTop = output.scrollHeight;
            }
        }
    });

    socket.addEventListener('close', (event) => {
        console.log('[close] Connection closed');
        socket = null;

        if (event.wasClean) {
            console.log(`Code: ${event.code}, Reason: ${event.reason}`);
        } else {
            console.error('Connection interrupted');
            if (reconnectAttempts < maxReconnectAttempts) {
                setTimeout(() => {
                    reconnectAttempts++;
                    console.log(`Reconnection attempt ${reconnectAttempts}`);
                    createWebSocket();
                }, reconnectInterval);
            }
        }
    });

    socket.addEventListener('error', (error) => {
        console.log(`[error] ${error.message}`);
    });
}

function sendMessage(data) {
    
    if (!socket || socket.readyState !== WebSocket.OPEN) {
        console.log('Connection not ready - queuing message');
        messageQueue.push(data);
        if (!socket || socket.readyState === WebSocket.CLOSED) {
            createWebSocket();
        }
        return;
    }

    try {
        socket.send(data);
    } catch (error) {
        console.error('Error sending message:', error);
        messageQueue.push(data);
    }
}

export {
    createWebSocket, // Make sure this matches exactly with import name
    sendMessage
};
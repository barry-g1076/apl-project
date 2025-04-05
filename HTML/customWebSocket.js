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
            if (!output) return;

            let data;
            try {
                data = typeof event.data === 'string' ? JSON.parse(event.data) : event.data;
            } catch (parseError) {
                console.error('Failed to parse message data:', parseError);
                return;
            }


            console.log('Received WebSocket message:', data);

            // Create container for all messages
            const messageContainer = document.createElement('div');
            messageContainer.classList.add('message-container');

            if (data.success) {
                // Handle multiple results (array or single value)
                const results = Array.isArray(data.result) ? data.result : [data.result];
                results.forEach(result => {
                    if (result != null) {  // Skip null/undefined results
                        const resultElement = document.createElement('p');
                        resultElement.textContent = result;
                        resultElement.classList.add('message-success');
                        messageContainer.appendChild(resultElement);
                    }
                });
            } else {
                // Handle multiple errors (array or single value)
                const errors = Array.isArray(data.errors) ? data.errors :
                    (data.errors ? [data.errors] : ['Unknown error']);
                errors.forEach(error => {
                    const errorElement = document.createElement('p');
                    errorElement.textContent = error;
                    errorElement.classList.add('message-error');
                    messageContainer.appendChild(errorElement);
                });
            }

            // Only append if we have content
            if (messageContainer.children.length > 0) {
                const fragment = document.createDocumentFragment();
                fragment.appendChild(messageContainer);
                output.appendChild(fragment);
                output.scrollTop = output.scrollHeight;
            }
        } catch (error) {
            console.error('Error processing WebSocket message:', error);
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
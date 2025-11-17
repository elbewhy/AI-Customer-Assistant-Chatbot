const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

// Function to add a message to the chat history
function addMessage(sender, message) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message-bubble', 'shadow-sm');

    if (sender === 'user') {
        messageDiv.classList.add('user-message', 'self-end');
    } else {
        messageDiv.classList.add('ai-message', 'self-start');
    }
    
    // Use innerHTML to handle potential Markdown formatting from the AI
    messageDiv.innerHTML = message; 

    chatHistory.appendChild(messageDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight; // Scroll to bottom
}

// Function to send message to Flask backend
async function sendMessage() {
    const message = userInput.value.trim();
    if (message === '') return; // Don't send empty messages

    addMessage('user', message);
    userInput.value = ''; // Clear input field
    sendButton.disabled = true; // Disable button while waiting for response
    userInput.disabled = true; // Disable input too

    // Display a typing indicator or loading message
    const loadingMessageDiv = document.createElement('div');
    loadingMessageDiv.classList.add('message-bubble', 'ai-message', 'self-start', 'shadow-sm', 'animate-pulse');
    loadingMessageDiv.innerHTML = '<span>.</span><span>.</span><span>.</span>'; // Simple typing indicator
    chatHistory.appendChild(loadingMessageDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        });

        // Remove typing indicator before processing response
        chatHistory.removeChild(loadingMessageDiv);

        if (!response.ok) {
            const errorData = await response.json();
            // Handle errors returned from the server (e.g., empty message, API key missing)
            throw new Error(errorData.reply || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        // --- THE FIX: Reading data.reply instead of data.response ---
        addMessage('ai', data.reply); 

    } catch (error) {
        console.error('Error sending message:', error);
        addMessage('ai', `Oops! Something went wrong: ${error.message}`);
    } finally {
        sendButton.disabled = false; // Re-enable button
        userInput.disabled = false; // Re-enable input
        userInput.focus(); // Focus back on input
    }
}

// Allow sending message with Enter key
userInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

// Initial focus on the input field
window.onload = () => {
    userInput.focus();
};

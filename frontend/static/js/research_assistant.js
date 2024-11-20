document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('send-button');
    const userInput = document.getElementById('user-input');

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;

        // Display the user's message
        addMessage(message, 'user');

        // Send the input to the backend
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({ 
                prompt: message 
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Display the AI response
            addMessage(data.response, 'ai');
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('Sorry, there was an error processing your request.', 'ai');
        })
        .finally(() => {
            // Clear input field
            userInput.value = '';
        });
    }

    function addMessage(text, type) {
        const messageContainer = document.querySelector('.chat-messages');
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(type === 'user' ? 'user-message' : 'ai-message');
        messageElement.textContent = text;
        messageContainer.appendChild(messageElement);
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }

    function loadChat(title) {
        fetch(`/load_chat?title=${encodeURIComponent(title)}`)
        .then(response => response.json())
        .then(chats => {
            const messageContainer = document.querySelector('.chat-messages');
            messageContainer.innerHTML = '';
            
            chats.forEach(chat => {
                addMessage(chat.query, 'user');
                addMessage(chat.response, 'ai');
            });
        })
        .catch(error => {
            console.error('Error loading chat:', error);
        });
    }
});
document.addEventListener('DOMContentLoaded', () => {

    // --- Chatbot Logic ---
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const closeChatBtn = document.getElementById('close-chat');
    const chatWindow = document.getElementById('chat-window');
    const sendBtn = document.getElementById('send-btn');
    const userInputField = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');

    // Make regular webpage buttons trigger the Chatbot!
    const bookButtons = document.querySelectorAll('.chat-trigger');
    bookButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            // Open chat if hidden
            if (chatWindow.classList.contains('hidden')) {
                toggleChat();
            } else {
                // Just focus the input if already open
                userInputField.focus();
            }
            // Pre-fill a message for the user if they want
            setTimeout(() => {
                userInputField.value = "I want to book an appointment";
                sendBtn.removeAttribute('disabled');
            }, 600);
        });
    });

    userInputField.addEventListener('input', () => {
        if (userInputField.value.trim() !== '') {
            sendBtn.removeAttribute('disabled');
        } else {
            sendBtn.setAttribute('disabled', 'true');
        }
    });

    function toggleChat() {
        if (chatWindow.classList.contains('hidden')) {
            chatWindow.classList.remove('hidden');
            chatbotToggle.classList.add('open');
            setTimeout(() => userInputField.focus(), 400); // Wait for open animation
        } else {
            chatWindow.classList.add('hidden');
            chatbotToggle.classList.remove('open');
        }
    }

    chatbotToggle.addEventListener('click', toggleChat);
    closeChatBtn.addEventListener('click', toggleChat);

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function appendMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');

        if (sender === 'bot') {
            messageDiv.innerHTML = text;
        } else {
            messageDiv.textContent = text;
        }

        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    function showTypingIndicator() {
        const typingItem = document.createElement('div');
        typingItem.classList.add('message', 'bot-message');
        typingItem.id = 'typing-indicator';
        typingItem.innerHTML = '<i>Typing...</i>';

        chatMessages.appendChild(typingItem);
        scrollToBottom();
    }

    function removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    async function sendMessage() {
        const text = userInputField.value.trim();
        if (!text) return;

        appendMessage(text, 'user');

        userInputField.value = '';
        sendBtn.setAttribute('disabled', 'true');

        showTypingIndicator();

        try {
            const response = await fetch('http://localhost:8000/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: text, history: [] })
            });

            if (!response.ok) {
                throw new Error('API response was not ok');
            }

            const data = await response.json();

            setTimeout(() => {
                removeTypingIndicator();
                appendMessage(data.reply, 'bot');
            }, 600);

        } catch (error) {
            console.error('Error:', error);
            removeTypingIndicator();
            appendMessage("Connection error: Ensure Backend is running locally.", 'bot');
        }
    }

    sendBtn.addEventListener('click', sendMessage);

    userInputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

});

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const data = urlParams.get('data');
const jsonData = JSON.parse(decodeURIComponent(data));

function showText() {
    return jsonData.description
}

function showSummary() {
    return jsonData.summary
}

function showSection(sectionId) {
    document.getElementById('text').style.display = 'none';
    document.getElementById('summary').style.display = 'none';
    document.getElementById('chat-app').style.display = 'none';
    document.getElementById(sectionId).style.display = 'block';

    if (sectionId === 'text') {
        document.getElementById('text-content').textContent = showText();
    } else if (sectionId === 'summary') {
        document.getElementById('summary-content').textContent = showSummary();
    } else if (sectionId === 'chat-app') {
        startChat();
    }
}

function startChat() {
    // chat app
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const connectionStatus = document.getElementById('connection-status');  

    // In a real implementation, replace this with your actual WebSocket server address
    const socket = new WebSocket('ws://0.0.0.0:8000/ws');

    socket.onopen = function(event) {
        connectionStatus.textContent = 'Connected';
        connectionStatus.style.color = '#4caf50';
    };

    socket.onmessage = function(event) {
        addMessage('AI', event.data, 'ai-message');
    };

    socket.onclose = function(event) {
        connectionStatus.textContent = 'Disconnected';
        connectionStatus.style.color = '#f44336';
    };

    socket.onerror = function(error) {
        connectionStatus.textContent = 'Error: ' + error.message;
        connectionStatus.style.color = '#f44336';
    };

    function sendMessage() {
        const message = userInput.value.trim();
        if (message && socket.readyState === WebSocket.OPEN) {
            addMessage('You', message, 'user-message');
            socket.send(message);
            userInput.value = '';
        }
    }

    function addMessage(sender, message, className) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message ' + className;
        messageElement.textContent = message;
        chatContainer.appendChild(messageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

}

// Initialize with text section visible
showSection('text');



        
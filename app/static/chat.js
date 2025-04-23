// Get the logged-in user's username and chat partner's username from Django template
const user = JSON.parse(document.getElementById('user').textContent);
const chatPartnerUsername = "{{ chat_partner.username }}";

// Dynamic room name
const roomName = `${user}-${chatPartnerUsername}`;

const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
);

// Display incoming messages
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const message = `${data.username}: ${data.message}`;
    document.getElementById('chat-log').innerHTML += message + '<br>';
};

// Send message function
function sendMessage() {
    const messageInput = document.getElementById('chat-message-input');
    const message = messageInput.value.trim();
    if (message) {
        chatSocket.send(JSON.stringify({'message': message, 'username': user}));
        messageInput.value = '';
    }
}

// Button click sends message
document.getElementById('chat-message-submit').onclick = sendMessage;

// Enter key sends message
document.getElementById('chat-message-input').addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault(); // Prevent newline
        sendMessage();
    }
});

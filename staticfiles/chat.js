// Get the logged-in user's username and chat partner's username from Django template
const user = JSON.parse(document.getElementById('user').textContent); // Using json_script to safely load the username
const chatPartnerUsername = "{{ chat_partner.username }}"; // Directly embed the username

// Dynamic room name
const roomName = `${user}-${chatPartnerUsername}`;  // Use backticks for template literals

const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const message = `${data.username}: ${data.message}`; // Fix the message formatting
    document.getElementById('chat-log').innerHTML += message + '<br>';
};

document.getElementById('chat-message-submit').onclick = function() {
    const messageInput = document.getElementById('chat-message-input');
    const message = messageInput.value;
    chatSocket.send(JSON.stringify({'message': message, 'username': user}));
    messageInput.value = '';
};

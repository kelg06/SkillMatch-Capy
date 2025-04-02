document.addEventListener("DOMContentLoaded", function () {
    let profileContainer = document.getElementById("profile-container");

    function setupSwipeButtons() {
        let profileCards = document.querySelectorAll(".profile-card");
        
        profileCards.forEach((card) => {
            let profileId = card.getAttribute("data-profile-id");

            card.querySelector(".dislike-btn").addEventListener("click", function () {
                card.classList.add("fade-out");
                setTimeout(() => card.remove(), 300);
            });

            card.querySelector(".like-btn").addEventListener("click", function () {
                fetch(`/like/${profileId}/`, { method: "POST", headers: { "X-CSRFToken": getCSRFToken() }})
                    .then(() => {
                        card.classList.add("fade-out");
                        setTimeout(() => card.remove(), 300);
                    })
                    .catch(error => console.error("Error:", error));
            });
        });
    }

    function getCSRFToken() {
        return document.cookie.split("; ").find(row => row.startsWith("csrftoken="))?.split("=")[1];
    }

    setupSwipeButtons();
});
function acceptFriend(profileId) {
    fetch(`/accept-friend-request/${profileId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    }).then(response => response.json())
      .then(data => {
        if (data.success) {
            alert(data.message);
            // Remove from pending requests
            const pendingRequestItem = document.querySelector(`li[data-profile-id='${profileId}']`);
            if (pendingRequestItem) {
                pendingRequestItem.remove();
            }
            // Add to friends list
            const friendsList = document.querySelector('.friends-list'); 
            const newFriendItem = document.createElement('li');
            newFriendItem.textContent = data.friend_username;
            friendsList.appendChild(newFriendItem);
        } else {
            alert(data.message);
        }
    });
}




function declineFriend(profileId) {
    fetch(`/decline-friend-request/${profileId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    }).then(response => response.json())
      .then(data => {
        if (data.success) {
            alert(data.message);
            // Remove from pending requests
            const pendingRequestItem = document.querySelector(`li[data-profile-id='${profileId}']`);
            if (pendingRequestItem) {
                pendingRequestItem.remove();
            }
        } else {
            alert(data.message);
        }
    });
}


function acceptFriend(profileId) {
    fetch(`/accept-friend-request/${profileId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    }).then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            // Optionally, update the UI to reflect the accepted friend request
            removeCard(profileId);
            location.reload();  // Refresh the page to update the friends list
        }
    }).catch(error => {
        console.error("Error accepting friend request:", error);
        alert("Failed to accept friend request.");
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrfToken = getCookie('csrftoken');

function unfriend(profileId) {
    fetch(`/unfriend/${profileId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    }).then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            // Ensure the friend list item ID matches the pattern
            const friendElement = document.querySelector(`#friend-${profileId}`);
            if (friendElement) {
                friendElement.remove();
            }
        }
    }).catch(error => {
        console.error("Error unfriending:", error);
        alert("Failed to unfriend.");
    });
}

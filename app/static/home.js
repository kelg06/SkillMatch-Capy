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
    }).then(response => {
        if (response.ok) {
            alert("Friend request accepted!");
            // Remove from pending requests
            const pendingRequestItem = document.querySelector(`li[data-profile-id='${profileId}']`);
            if (pendingRequestItem) {
                pendingRequestItem.remove();
            }
            // Add to friends section
            const friendsList = document.querySelector('.friends-list'); // Ensure you have a class for the friends list
            const newFriendItem = document.createElement('li');
            newFriendItem.textContent = `Friend: ${profileId}`; // Adjust as necessary
            friendsList.appendChild(newFriendItem);
        } else {
            alert("Failed to accept friend request.");
        }
    });
}



function declineFriend(profileId) {
    fetch(`/decline-friend-request/${profileId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        }
    }).then(response => {
        if (response.ok) {
            alert("Friend request declined!");
            location.reload();  // Refresh to update the profile list
        } else {
            alert("Failed to decline friend request.");
        }
    });
}

function sendFriendRequest(profileId) {
    fetch(`/send-friend-request/${profileId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    }).then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            removeCard(profileId);
        }
    }).catch(error => {
        console.error("Error sending friend request:", error);
    });
}
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

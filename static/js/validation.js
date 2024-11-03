// Function to check if email is already in use
document.getElementById("email").addEventListener("input", function () {
    const email = this.value;
    if (email.length > 0) { // Start checking as soon as there's any input
        fetch("/check_email", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email: email }),
        })
        .then(response => response.json())
        .then(data => {
            const feedback = document.getElementById("emailFeedback");
            feedback.textContent = data.message;
            feedback.style.color = data.exists ? "red" : "green";
        });
    } else {
        document.getElementById("emailFeedback").textContent = ""; // Clear feedback if input is empty
    }
});

// Function to check if name is already in use
document.getElementById("name").addEventListener("input", function () {
    const name = this.value;
    const feedback = document.getElementById("nameFeedback");
    if (name.length < 4) {
        feedback.textContent = "Username must be at least 5 characters long.";
        feedback.style.color = "red";
    } else {
        fetch("/check_name", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name: name }),
        })
        .then(response => response.json())
        .then(data => {
            feedback.textContent = data.message;
            feedback.style.color = data.exists ? "red" : "green";
        });
    }
    
    if (name.length === 0) {
        feedback.textContent = ""; // Clear feedback if input is empty
    }
});

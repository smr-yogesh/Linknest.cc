// Function to check if email is already in use
document.getElementById("email").addEventListener("input", function () {
    const email = this.value;
    if (email.length > 1) { // Start checking as soon as there's any input
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
    if (name.length < 5) {
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

// Function to change animation style live
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("anim").addEventListener("input", function () {
        const selectedAnimation = this.value.trim(); // Use trim to remove any extra spaces
        const scriptElement = document.getElementById("animation-script");

        // Check if the input is valid against the options
        if (selectedAnimation === "Dots" || selectedAnimation === "Lines") {
            // Remove the old script tag
            scriptElement.parentNode.removeChild(scriptElement);

            // Create a new script element with the new animation
            const newScript = document.createElement("script");
            newScript.id = "animation-script";

            // Dynamically change the `src` based on the selected option
            if (selectedAnimation === "Dots") {
                newScript.src = animations.dots;
            } else if (selectedAnimation === "Lines") {
                newScript.src = animations.lines;
            }

            // Append the new script tag to the body
            document.body.appendChild(newScript);
        }
    });
});

// Password matching 

$(document).ready(function () {
    // Password matching logic
    $('#new-password, #confirm-password').on('input', function () {
        const newPassword = $('#new-password').val();
        const confirmPassword = $('#confirm-password').val();

        if (newPassword === confirmPassword && newPassword.length > 0) {
            $('#passwordFeedback')
                .text('Passwords match')
                .css('color', 'green');
            $('#submitButton').prop('disabled', false);
        } else if (newPassword.length > 0 || confirmPassword.length > 0) {
            $('#passwordFeedback')
                .text('Passwords do not match')
                .css('color', 'red');
            $('#submitButton').prop('disabled', true);
        } else {
            $('#passwordFeedback').text('');
            $('#submitButton').prop('disabled', true);
        }
    });
});



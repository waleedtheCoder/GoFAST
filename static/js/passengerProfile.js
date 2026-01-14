// Profile Picture Click Behavior
document.getElementById('profile-pic').addEventListener('click', function() {
    alert("Profile picture upload coming soon!");
});

document.getElementById("profile-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    
    const userID = document.getElementById("userID").value;
    const phone = document.getElementById("phone").value;
    const pickup = document.getElementById("pickup").value;
    const drop = document.getElementById("drop").value;
    const pass = document.getElementById("pass").value;

    const payload = {
        userID,
        phone,
        pickup,
        drop,
        pass
    };

    try {
        const response = await fetch('/update_profile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        const result = await response.json();
        if (response.ok) {
            // Log a notification about the profile update
            const notificationPayload = {
                userID: userID,
                message: "Your profile has been updated successfully.",
                status: 'unread'
            };

            // Send notification to be logged
            await fetch('/log_notification', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(notificationPayload),
            });

            alert("Profile updated successfully!");
            window.location.href = '/passengerDashboard';
        } else {
            alert(`Error: ${result.error}`);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An unexpected error occurred.");
    }
});
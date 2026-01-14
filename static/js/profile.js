// Save Profile Changes
document.getElementById("profile-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    // Collecting input values from the form
    const userID = document.getElementById("userID").value;
    const phone = document.getElementById("phone").value;
    const licensePlate = document.getElementById("licensePlate").value;
    const availableSeats = document.getElementById("availableSeats").value;
    const make_model = document.getElementById("make_model").value;
    const pass = document.getElementById("pass").value;

    const payload = {
        userID,
        phone,
        licensePlate,
        availableSeats,
        make_model,
        pass
    };

    try {
        const response = await fetch('/update_dprofile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        const result = await response.json();
        if (response.ok) {
            alert("Profile updated successfully!");
            window.location.href = '/profile';
        } else {
            alert(`Error: ${result.error}`);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An unexpected error occurred.");
    }
});

// Update the form on page load with current data
window.onload = updateProfileForm;
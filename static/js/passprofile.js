// Make the profile picture clickable
document.getElementById("profile-pic").addEventListener("click", function () {
    document.getElementById("file-input").click(); // Trigger file input dialog
});

// Handle the file selection for profile picture
document.getElementById("file-input").addEventListener("change", function (event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            const profilePicUrl = e.target.result; // Get the image data URL

            // Update the profile picture immediately
            document.getElementById("profile-pic").src = profilePicUrl;

            // Save the profile picture URL to localStorage
            let profileData = JSON.parse(localStorage.getItem("profileData")) || {};
            profileData.profilePic = profilePicUrl; // Update the profile picture in the data
            localStorage.setItem("profileData", JSON.stringify(profileData)); // Save to localStorage
        };

        reader.readAsDataURL(file); // Read the file as a Data URL
    }
});

// On page load, populate the profile picture and form data from localStorage
window.onload = function () {
    const profileData = JSON.parse(localStorage.getItem("profileData"));
    if (profileData) {
        document.getElementById("profile-pic").src = profileData.profilePic || "profile.png"; // Fallback image
        document.getElementById("name").value = profileData.name || "Jane Doe";
        document.getElementById("email").value = profileData.email || "jane.doe@example.com";
        document.getElementById("address").value = profileData.address || "Model Town, Lahore";
    }
};

// Save Profile Changes
document.getElementById("profile-form").addEventListener("submit", function (event) {
    event.preventDefault();

    // Collecting input values from the form
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const address = document.getElementById("address").value;

    const profileData = {
        name,
        email,
        address,
        profilePic: document.getElementById("profile-pic").src // Save the current profile picture
    };

    // Save the profile data to localStorage
    localStorage.setItem("profileData", JSON.stringify(profileData));

    alert("Profile changes saved successfully!");
});

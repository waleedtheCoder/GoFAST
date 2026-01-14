
document.addEventListener("DOMContentLoaded", () => {
    const ctaButton = document.getElementById("cta-button");

    ctaButton.addEventListener("click", () => {
        // Redirect to login or signup page (modify paths as necessary)
        window.location.href = "/login"; // If a login route exists
    });
})


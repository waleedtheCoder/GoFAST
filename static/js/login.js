document.getElementById('login-form').addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevent default form submission behavior

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (response.status === 200) {
        window.location.href = '/passengerDash'; // Temporary profile route, update later
    } else {
        const errorMessage = document.getElementById('error-message');
        errorMessage.textContent = data.message;
        errorMessage.style.display = 'block';
    }
});

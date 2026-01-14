document.getElementById('register-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent default form submission

    // Retrieve input values
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const address = document.getElementById('address').value;
    const password = document.getElementById('password').value;
    const role = document.getElementById('role').value;

    const feedbackMessage = document.getElementById('feedback-message');

    // Validate email
    const emailPattern = /^[a-zA-Z0-9._%+-]+@lhr\.nu\.edu\.pk$/;
    if (!emailPattern.test(email)) {
        feedbackMessage.className = 'message error';
        feedbackMessage.innerText = 'Email must end with @lhr.nu.edu.pk';
        return;
    }

    // Validate phone number
    const phonePattern = /^92\d{10}$/;
    if (!phonePattern.test(phone)) {
        feedbackMessage.className = 'message error';
        feedbackMessage.innerText = 'Phone number must start with 92 and be 12 digits long';
        return;
    }

    // Prepare registration data
    const registrationData = {
        name: name,
        email: email,
        phone: phone,
        address: address,
        password: password,
        role: role,
    };

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(registrationData),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.message === 'OTP sent to your email address') {
                feedbackMessage.className = 'message success';
                feedbackMessage.innerText = 'An OTP has been sent to your email. Please verify to complete registration.';
                // Redirect to OTP verification page
                window.location.href = '/verify';
            } else {
                feedbackMessage.className = 'message error';
                feedbackMessage.innerText = data.error;
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            feedbackMessage.className = 'message error';
            feedbackMessage.innerText = 'An error occurred. Please try again.';
        });
});
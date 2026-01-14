document.getElementById('driver-details-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent default form submission

    const carMakeModel = document.getElementById('car-make-model').value;
    const licenseNumber = document.getElementById('license-number').value;
    const numberPlate = document.getElementById('number-plate').value;

    const feedbackMessage = document.getElementById('feedback-message');

    // Basic Validation Check
    if (!carMakeModel || !licenseNumber || !numberPlate) {
        feedbackMessage.className = 'message error';
        feedbackMessage.innerText = 'All fields are required!';
        return;
    }

    const driverDetails = {
        carMakeModel: carMakeModel,
        licenseNumber: licenseNumber,
        numberPlate: numberPlate,
    };

    // Send data to the backend
    fetch('/submitDriverDetails', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(driverDetails),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) { // Check the 'success' key
                feedbackMessage.className = 'message success';
                feedbackMessage.innerText = data.message; // Use the message from the response
                setTimeout(() => {
                    window.location.href = '/passengerDash'; // Redirect to driver's dashboard
                }, 2000);
            } else {
                feedbackMessage.className = 'message error';
                feedbackMessage.innerText = data.message; // Use the error message from the response
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            feedbackMessage.className = 'message error';
            feedbackMessage.innerText = 'An error occurred. Please try again.';
        });
});

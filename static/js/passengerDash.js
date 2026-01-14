document.addEventListener('DOMContentLoaded', () => {
    const acceptedOffersContainer = document.getElementById('accepted-offers');

    // Fetch offers from the backend
    fetch('/get_accepted_offers')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const offers = data.offers;
                const currentTime = new Date(); // Get the current time

                // Filter offers to include only those within the last 2 minutes
                const filteredOffers = offers.filter(offer => {
                    const offerTimestamp = new Date(offer.offerTimestamp); // Parse offer timestamp to a Date object
                    const timeDifference = (currentTime - offerTimestamp) / 1000; // Difference in seconds

                    return timeDifference <= 43200; // Only show offers made within the last 2 minutes (120 seconds)
                });

                if (filteredOffers.length === 0) {
                    acceptedOffersContainer.innerHTML = '<p>No accepted offers available in the last 2 minutes.</p>';
                } else {
                    acceptedOffersContainer.innerHTML = ''; // Clear the loading message

                    filteredOffers.forEach(offer => {
                        const offerElement = document.createElement('div');
                        offerElement.classList.add('offer-item');
                        offerElement.innerHTML = `
                            <p><strong>Driver Name:</strong> ${offer.driverName}</p>
                            <p><strong>Requested Car:</strong> ${offer.carName}</p>
                            <p><strong>Driver Car:</strong> ${offer.vehicleName}</p>
                            <p><strong>Driver Car Number:</strong> ${offer.vehicleNumber}</p>
                            <p><strong>Status:</strong> ${offer.status}</p>
                            <p><strong>Offer Timestamp:</strong> ${offer.offerTimestamp}</p>
                            <button class="start-ride-btn" data-passenger-offer-id="${offer.passengerOfferID}" data-driver-offer-id="${offer.driverOfferID}">Start Ride</button>
                        `;
                        acceptedOffersContainer.appendChild(offerElement);
                    });

                    // Attach event listeners to "Start Ride" buttons
                    const startRideButtons = document.querySelectorAll('.start-ride-btn');
                    startRideButtons.forEach(button => {
                        button.addEventListener('click', function () {
                            const passengerOfferID = this.getAttribute('data-passenger-offer-id');
                            const driverOfferID = this.getAttribute('data-driver-offer-id');
                            startRide(passengerOfferID, driverOfferID);
                        });
                    });
                }
            } else {
                acceptedOffersContainer.innerHTML = `<p>Error: ${data.message}</p>`;
            }
        })
        .catch(error => {
            console.error('Error fetching accepted offers:', error);
            acceptedOffersContainer.innerHTML = '<p>Error loading accepted offers. Please try again later.</p>';
        });
});

// Function to start a ride
function startRide(passengerOfferID, driverOfferID) {
    fetch('/start_ride', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            passengerOfferID: passengerOfferID,
            driverOfferID: driverOfferID,
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Ride has been started successfully!');
                window.location.href = '/passenger-ride'; // Redirect to /passenger-ride
            } else {
                alert(`Error: ${data.message}`);
            }
        })
        .catch(error => {
            console.error('Error starting ride:', error);
            alert('An error occurred while starting the ride. Please try again.');
        });
}
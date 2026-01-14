// Fetch available passenger offers
function fetchOffers() {
    fetch('/get_offers')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayOffers(data.offers);
            } else {
                alert('Failed to load offers.');
            }
        })
        .catch(error => {
            console.error('Error fetching offers:', error);
            alert('An error occurred while fetching offers.');
        });
}

// Display offers on the page
function displayOffers(offers) {
    const offersList = document.getElementById('offers-list');
    offersList.innerHTML = ''; // Clear existing offers

    offers.forEach(offer => {
        const offerCard = document.createElement('div');
        offerCard.classList.add('offer-card');

        offerCard.innerHTML = `
            <p><strong>From:</strong> ${offer.startLocation}</p>
            <p><strong>To:</strong> ${offer.endLocation}</p>
            <p><strong>Offer Timestamp:</strong> ${offer.offerTimestamp}</p>
            <p><strong>Car:</strong> ${offer.carName} (Capacity: ${offer.carCapacity})</p>
            <p><strong>Note:</strong> ${offer.additionalNote || 'None'}</p>
            <button class="accept-btn" data-offer-id="${offer.offerID}">Accept Offer</button>
            <button class="reject-btn" data-offer-id="${offer.offerID}">Reject Offer</button>
        `;

        // Add click event to the Accept button
        offerCard.querySelector('.accept-btn').addEventListener('click', () => {
            acceptOffer(offer.offerID);
        });

        // Add click event to the Reject button
        offerCard.querySelector('.reject-btn').addEventListener('click', () => {
            rejectOffer(offer.offerID);
        });

        offersList.appendChild(offerCard);
    });
}

// Accept an offer
function acceptOffer(offerID) {
    fetch('/accept_offer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ offerID }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Offer accepted successfully!');
                window.location.href = '/driver-ride'; // Redirect to /driver-ride
            } else {
                alert('Failed to accept the offer.');
            }
        })
        .catch(error => {
            console.error('Error accepting offer:', error);
            alert('An error occurred while accepting the offer.');
        });
}

// Reject an offer
function rejectOffer(offerID) {
    fetch('/reject_offer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ offerID }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Offer rejected successfully!');
                fetchOffers(); // Refresh the offers list
            } else {
                alert('Failed to reject the offer.');
            }
        })
        .catch(error => {
            console.error('Error rejecting offer:', error);
            alert('An error occurred while rejecting the offer.');
        });
}

// Fetch offers on page load
document.addEventListener('DOMContentLoaded', fetchOffers);
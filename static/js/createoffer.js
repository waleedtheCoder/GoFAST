const API_BASE_URL = "http://127.0.0.1:5000"; // Backend URL
let map, directionsService, directionsRenderer;
let pickupMarker, dropoffMarker; // Markers for pickup and drop-off
const fastNucesCoordinates = { lat: 31.481460922909925, lng: 74.30363352166144 };

async function fetchPlacesSuggestions(inputId, suggestionsId) {
    const query = document.getElementById(inputId).value;

    if (query.trim() === "") {
        document.getElementById(suggestionsId).innerHTML = ""; // Clear suggestions
        return;
    }

    try {
        // Use Google Maps Places Autocomplete service to get suggestions
        const service = new google.maps.places.AutocompleteService();
        service.getQueryPredictions({ input: query }, (predictions, status) => {
            if (status === google.maps.places.PlacesServiceStatus.OK) {
                displaySuggestions(predictions, inputId, suggestionsId);
            } else {
                console.error("Error fetching suggestions:", status);
            }
        });
    } catch (error) {
        console.error("Error:", error);
    }
}

function displaySuggestions(predictions, inputId, suggestionsId) {
    const suggestionsElement = document.getElementById(suggestionsId);
    suggestionsElement.innerHTML = ""; // Clear previous suggestions

    predictions.forEach((prediction) => {
        const suggestionItem = document.createElement('div');
        suggestionItem.classList.add('suggestion-item');
        suggestionItem.innerHTML = prediction.description;
        suggestionItem.onclick = () => {
            document.getElementById(inputId).value = prediction.description; // Set the input value to the selected suggestion
            suggestionsElement.innerHTML = ""; // Clear suggestions after selection
        };
        suggestionsElement.appendChild(suggestionItem);
    });
}

let offers = []; // Store created offers

// Handle offer form submission
document.getElementById('offerForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the page from refreshing on form submission

    // Retrieve values from the form
    const startLocation = document.getElementById('start-location').value.trim();
    const endLocation = document.getElementById('end-location').value.trim();  // New end location field
    const carCapacity = parseInt(document.getElementById('car-capacity').value.trim());
    const carName = document.getElementById('car-name').value.trim();
    const note = document.getElementById('note').value.trim();

    const availableSeats = 1; // Set available seats as a constant value of 1

    // Required location
    const requiredLocation = "National University Of Computer and Emerging Sciences, Milaad Street, Block B Faisal Town, Lahore, Pakistan";

    // Check if either the start or end location matches the required location
    if (startLocation !== requiredLocation && endLocation !== requiredLocation) {
        alert('Either the starting or ending location must be "National University Of Computer and Emerging Sciences, Milaad Street, Block B Faisal Town, Lahore, Pakistan".');
        return;
    }

    // Validate form inputs
    if (!startLocation || !endLocation || !carCapacity || !carName) {  // No need to check availableSeats
        alert('Please fill in all required fields.');
        return;
    }

    // Prepare data to send to the server
    const offerData = {
        startLocation,
        endLocation, // Include endLocation in the data
        carCapacity,
        availableSeats,
        carName,
        note
    };

    // Send the offer data to the server using fetch (AJAX)
    fetch('/create_offer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(offerData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // If the offer was successfully created, add it to the local offers array
            offers.push(offerData);
            updateOffersDisplay(); // Update the offers display
            document.getElementById('offerForm').reset(); // Clear the form
        } else {
            alert('Error creating the offer. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
});

// Function to update the offers display
function updateOffersDisplay() {
    const offersList = document.getElementById('offers-list');
    offersList.innerHTML = ''; // Clear previous offers

    if (offers.length === 0) {
        offersList.innerHTML = '<p>No offers created yet.</p>';
        return;
    }

    // Loop through each offer and display it
    offers.forEach((offer) => {
        const offerItem = document.createElement('div');
        offerItem.classList.add('offer-item');
        offerItem.innerHTML = `
            <p><strong>From:</strong> ${offer.startLocation}</p>
            <p><strong>To:</strong> ${offer.endLocation}</p>  <!-- Display the end location -->
            <p><strong>Car:</strong> ${offer.carName} (Capacity: ${offer.carCapacity})</p>
            ${offer.note ? `<p><strong>Note:</strong> ${offer.note}</p>` : ''}
        `;
        offersList.appendChild(offerItem);
    });
}

// Initialize the page (with no offers)
updateOffersDisplay();

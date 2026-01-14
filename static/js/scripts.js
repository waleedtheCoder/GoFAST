        const API_BASE_URL = "http://127.0.0.1:5000"; // Backend URL
        let map, directionsService, directionsRenderer;
        let pickupMarker, dropoffMarker; // Markers for pickup and drop-off
        const fastNucesCoordinates = { lat: 31.481460922909925, lng: 74.30363352166144 };

        // Your existing JavaScript functions here

        // Initialize Google Map with Directions API
function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 31.5204, lng: 74.3587 }, // Center on Lahore, Pakistan
        zoom: 12,
    });

    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);

    // Add click event listener for selecting pickup and drop-off points
    map.addListener("click", (event) => handleMapClick(event));
}

// Handle map click for selecting pickup and drop-off locations
function handleMapClick(event) {
    const clickedLocation = {
        lat: event.latLng.lat(),
        lng: event.latLng.lng(),
    };

    // If pickup marker is not set, set it
    if (!pickupMarker) {
        pickupMarker = new google.maps.Marker({
            position: clickedLocation,
            map: map,
            label: "Pickup",
        });
        document.getElementById("origin").value = `${clickedLocation.lat}, ${clickedLocation.lng}`;
    }
    // If dropoff marker is not set, set it
    else if (!dropoffMarker) {
        dropoffMarker = new google.maps.Marker({
            position: clickedLocation,
            map: map,
            label: "Dropoff",
        });
        document.getElementById("destination").value = `${clickedLocation.lat}, ${clickedLocation.lng}`;
    } else {
        alert("Both pickup and drop-off points are already set! Use Reset to select again.");
    }
}

// Reset markers and inputs
function resetMarkers() {
    if (pickupMarker) {
        pickupMarker.setMap(null);
        pickupMarker = null;
    }
    if (dropoffMarker) {
        dropoffMarker.setMap(null);
        dropoffMarker = null;
    }
    document.getElementById("origin").value = "";
    document.getElementById("destination").value = "";
}

// Function to fetch place autocomplete suggestions
async function fetchPlacesSuggestions(inputId, suggestionsId) {
    const query = document.getElementById(inputId).value;

    if (query.trim() === "") {
        document.getElementById(suggestionsId).innerHTML = ""; // Clear suggestions
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/places?query=${encodeURIComponent(query)}`);
        if (response.ok) {
            const suggestions = await response.json();
            displaySuggestions(suggestions, inputId, suggestionsId);
        } else {
            console.error("Error fetching suggestions:", await response.json());
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

// Function to display suggestions in a dropdown list
function displaySuggestions(suggestions, inputId, suggestionsId) {
    const suggestionsList = document.getElementById(suggestionsId);
    suggestionsList.innerHTML = ""; // Clear old suggestions

    if (suggestions.length === 0) {
        suggestionsList.innerHTML = "<li>No results found</li>";
        return;
    }

    suggestions.forEach((suggestion) => {
        const li = document.createElement("li");
        li.textContent = suggestion.description;
        li.onclick = () => selectSuggestion(inputId, suggestion.description, suggestionsId);
        suggestionsList.appendChild(li);
    });
}

// Function to handle selection of a suggestion
function selectSuggestion(inputId, place, suggestionsId) {
    document.getElementById(inputId).value = place;
    document.getElementById(suggestionsId).innerHTML = ""; // Clear suggestions
}

// Function to calculate distance and duration
async function calculateDistance() {
    const origin = document.getElementById("origin").value;
    const destination = document.getElementById("destination").value;

    if (!origin || !destination) {
        alert("Both origin and destination are required!");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/distance`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ origin, destination }),
        });

        if (response.ok) {
            const result = await response.json();
            document.getElementById("distance-result").innerText = 
                `Distance: ${result.distance}, Duration: ${result.duration}`;
        } else {
            const error = await response.json();
            document.getElementById("distance-result").innerText = `Error: ${error.error}`;
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("distance-result").innerText = "Error fetching distance.";
    }
}

// Function to display the route on the map
function displayRoute() {
    const origin = document.getElementById("origin").value;
    const destination = document.getElementById("destination").value;

    if (!origin || !destination) {
        alert("Both origin and destination are required!");
        return;
    }

    // If origin or destination is in lat,lng format, convert it to LatLng object
    const originLatLng = parseLatLng(origin);
    const destinationLatLng = parseLatLng(destination);

    // If the input is not in lat,lng format, it must be a place name, so use it as is
    const request = {
        origin: originLatLng || origin,
        destination: destinationLatLng || destination,
        travelMode: google.maps.TravelMode.DRIVING,
    };

    // Make the DirectionsService call
    directionsService.route(request, function(result, status) {
        if (status === google.maps.DirectionsStatus.OK) {
            // If multiple routes are returned, loop through and display them
            if (result.routes.length > 1) {
                alert("Multiple routes found. Displaying the first one.");
            }

            // Set the directions on the map
            directionsRenderer.setDirections(result);

            // Set styling for the route line (blue color)
            directionsRenderer.setOptions({
                polylineOptions: {
                    strokeColor: "#1a73e8", // Blue color
                    strokeWeight: 5, // Line thickness
                    strokeOpacity: 0.7, // Line opacity
                },
            });
        } else {
            console.error("Directions request failed due to: ", status);
            alert(`Could not display the route. Error: ${status}`);
        }
    });
}

// Function to parse lat,lng strings into LatLng objects
function parseLatLng(str) {
    const regex = /^(-?\d+\.\d+),\s*(-?\d+\.\d+)$/;
    const match = str.match(regex);
    if (match) {
        return new google.maps.LatLng(parseFloat(match[1]), parseFloat(match[2]));
    }
    return null;
}

// Function to use current location as pickup point
function useCurrentLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            const currentLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude,
            };

            // Set marker for pickup location
            if (pickupMarker) {
                pickupMarker.setMap(null); // Remove any existing pickup marker
            }

            pickupMarker = new google.maps.Marker({
                position: currentLocation,
                map: map,
                label: "Pickup",
            });

            // Update input field with current location
            document.getElementById("origin").value = `${currentLocation.lat}, ${currentLocation.lng}`;

            // Center the map on the current location
            map.setCenter(currentLocation);
            map.setZoom(14); // Zoom in a bit more to show the user
        });
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

// Function to set FAST Nuces as pickup location
function setFastNucesPickup() {
    if (pickupMarker) {
        pickupMarker.setMap(null); // Remove any existing pickup marker
    }

    pickupMarker = new google.maps.Marker({
        position: fastNucesCoordinates,
        map: map,
        label: "Pickup",
    });

    // Update input field with FAST Nuces coordinates
    document.getElementById("origin").value = `${fastNucesCoordinates.lat}, ${fastNucesCoordinates.lng}`;
}

// Function to set FAST Nuces as drop-off location
function setFastNucesDropoff() {
    if (dropoffMarker) {
        dropoffMarker.setMap(null); // Remove any existing drop-off marker
    }

    dropoffMarker = new google.maps.Marker({
        position: fastNucesCoordinates,
        map: map,
        label: "Dropoff",
    });

    // Update input field with FAST Nuces location as the destination
    document.getElementById("destination").value = "FAST Nuces, Lahore";
}
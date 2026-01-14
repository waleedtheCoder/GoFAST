// Function to fetch and filter users based on the role (driver or passenger)
function filterUsers(role) {
    fetch(`/admin/dashboard?role=${role}`)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('tableBody');
            const tableHeaders = document.getElementById('tableHeaders');
            tableBody.innerHTML = '';

            // Clear existing headers and set new ones based on the role
            tableHeaders.innerHTML = '';
            if (role === 'driver') {
                tableHeaders.innerHTML = `
                    <th>User ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone Number</th>
                    <th>Vehicle ID</th>
                    <th>License Plate</th>
                    <th>Make & Model</th>
                    <th>Capacity</th>
                    <th>Available Seats</th>
                    <th>Rating</th>
                `;
            } else if (role === 'passenger') {
                tableHeaders.innerHTML = `
                    <th>User ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone Number</th>
                    <th>Preferred Pickup Location</th>
                    <th>Preferred Drop Location</th>
                    <th>Rating</th>
                `;
            }

            // Add rows to the table dynamically based on the fetched data
            data.forEach(user => {
                const row = document.createElement('tr');
                if (role === 'driver') {
                    row.innerHTML = `
                        <td>${user.userID}</td>
                        <td>${user.name}</td>
                        <td>${user.email}</td>
                        <td>${user.phoneNumber}</td>
                        <td>${user.vehicleID}</td>
                        <td>${user.licensePlate}</td>
                        <td>${user.makeModel}</td>
                        <td>${user.capacity}</td>
                        <td>${user.availableSeats}</td>
                        <td>${user.rating}</td>
                    `;
                } else if (role === 'passenger') {
                    row.innerHTML = `
                        <td>${user.userID}</td>
                        <td>${user.name}</td>
                        <td>${user.email}</td>
                        <td>${user.phoneNumber}</td>
                        <td>${user.preferredPickupLocation}</td>
                        <td>${user.preferredDropLocation}</td>
                        <td>${user.rating}</td>
                    `;
                }
                tableBody.appendChild(row);
            });
        });
}

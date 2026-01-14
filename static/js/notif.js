// Fetching the container where notifications will be displayed
const notificationsContainer = document.getElementById('notificationsContainer');

// Function to dynamically fetch and render notifications
async function loadNotifications() {
    try {
        const response = await fetch('/get-notifications'); // API endpoint for fetching notifications
        if (!response.ok) {
            throw new Error('Failed to fetch notifications');
        }

        const notifications = await response.json(); // Assuming backend sends an array of notifications

        if (notifications.length === 0) {
            notificationsContainer.innerHTML = '<p>No notifications available.</p>';
        } else {
            notifications.forEach((notification) => {
                // Create a div for each notification
                const notificationDiv = document.createElement('div');
                notificationDiv.classList.add('notification-item');

                // Create a message paragraph
                const messageElement = document.createElement('p');
                messageElement.textContent = notification.message;

                // Append the message to the notification div
                notificationDiv.appendChild(messageElement);

                // Append the notification div to the container
                notificationsContainer.appendChild(notificationDiv);
            });
        }
    } catch (error) {
        console.error('Error loading notifications:', error);
        notificationsContainer.innerHTML = '<p>Error loading notifications. Please try again later.</p>';
    }
}

// Call the function to load notifications on page load
window.onload = loadNotifications;
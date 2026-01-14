let schedule = []; // Temporary storage for the schedule

// Function to add/update a schedule entry
function addSchedule(event) {
    event.preventDefault();

    const day = document.getElementById('day').value;
    const time = document.getElementById('time').value;

    // Check if the day already exists in the schedule
    const existingEntry = schedule.find(entry => entry.day === day);
    if (existingEntry) {
        // Update the existing entry
        existingEntry.time = time;
    } else {
        // Add a new entry
        schedule.push({ day, time });
    }

    // Update the schedule display
    updateScheduleDisplay();

    // Clear the form
    document.getElementById('scheduleForm').reset();
}

// Function to display the schedule
function updateScheduleDisplay() {
    const scheduleList = document.getElementById('schedule-list');
    scheduleList.innerHTML = '';

    if (schedule.length === 0) {
        scheduleList.innerHTML = '<p>No schedule uploaded yet.</p>';
        return;
    }

    schedule.forEach(entry => {
        const scheduleItem = document.createElement('div');
        scheduleItem.classList.add('schedule-item');
        scheduleItem.innerHTML = `<p><strong>${capitalize(entry.day)}:</strong> ${entry.time}</p>`;
        scheduleList.appendChild(scheduleItem);
    });
}

// Utility function to capitalize the first letter
function capitalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

// Add event listener for the form
document.getElementById('scheduleForm').addEventListener('submit', addSchedule);

// Initial display of the schedule
updateScheduleDisplay();

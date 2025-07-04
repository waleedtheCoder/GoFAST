import pyodbc
import uuid
from datetime import datetime

# Connection string for Windows Authentication (with encryption disabled)
server = 'LAPTOP-ITJUVA2H\SQLExpress'  # Replace with your SQL Server name or IP address
database = 'GOFASTT'  # Replace with your database name
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;Encrypt=no'


# Establishing a connection
def connect():
    return pyodbc.connect(connection_string)

# Fetch user details
def get_user_details(user_id):
    conn = connect()
    cursor = conn.cursor()
    try:
        query = "SELECT name, email, phoneNumber, profilePicture, rating, password FROM Userr WHERE userID = ?"
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        if row:
            return {
                "name": row[0],
                "email": row[1],
                "phoneNumber": row[2],
                "profilePicture": row[3],
                "rating": row[4],
                "password": row[5]
            }
        else:
            return None
    finally:
        cursor.close()
        conn.close()

# Fetch passenger details
def get_passenger_details(user_id):
    conn = connect()
    cursor = conn.cursor()
    try:
        query = "SELECT passengerID, preferredPickupLocation, preferredDropLocation FROM Passenger WHERE userID = ?"
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        if row:
            return {
                "passengerID": row[0],  # Add passengerID
                "preferredPickupLocation": row[1],
                "preferredDropLocation": row[2]
            }
        else:
            return None
    finally:
        cursor.close()
        conn.close()

def get_driver_details(user_id):
    
    conn = connect()
    cursor = conn.cursor()
    try:
        query = """
                SELECT v.vehicleID, v.licensePlate, v.make_model, d.availableSeats
                FROM Driver d
                INNER JOIN Vehicle v ON d.vehicleID = v.vehicleID
                WHERE d.userID = ?
                """
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        if row:
            return {
                "vehicleID": row[0],
                "licensePlate": row[1], 
                "make_model": row[2],
                "availableSeats": row[3]
            }
        else:
            return None
    finally:
        cursor.close()
        conn.close()


# Update passenger profile
def update_passenger_profile(user_id, phone, pickup, drop, password):
    """
    Update a passenger's phone number, preferred pickup location, drop location and password
    """
    conn = connect()
    cursor = conn.cursor()
    try:
        # Update user phone number in Userr table
        query_user = "UPDATE Userr SET phoneNumber = ?, password = ? WHERE userID = ?"
        # Update pickup and drop locations in Passenger table
        query_passenger = """
            UPDATE Passenger
            SET preferredPickupLocation = ?, preferredDropLocation = ?
            WHERE userID = ?
        """
        cursor.execute(query_user, (phone, password, user_id))
        cursor.execute(query_passenger, (pickup, drop, user_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Error updating passenger profile:", e)
        raise
    finally:
        cursor.close()
        conn.close()

def update_driver_profile(user_id, phone,licensePlate, availableSeats, make_model, password):
    conn = connect()
    cursor = conn.cursor()
    try:
        # Update user phone number in Userr table
        query_user = "UPDATE Userr SET phoneNumber = ?, password = ? WHERE userID = ?"
        # Update pickup and drop locations in Passenger table
        query_driver = """
            UPDATE Driver
            SET availableSeats = ?
            WHERE userID = ?
        """
        query_vehicle = """
            UPDATE Vehicle
            SET licensePlate = ?, make_model = ?
            WHERE vehicleID = ?
        """

        cursor.execute(query_user, (phone, password, user_id))
        cursor.execute(query_driver, (availableSeats, user_id))
        cursor.execute(query_vehicle, (licensePlate, make_model, user_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Error updating driver profile:", e)
        raise
    finally:
        cursor.close()
        conn.close()

# Function to get all driver details
def get_drivers():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT  v.vehicleID, v.licensePlate, v.make_model, v.capacity, 
               
        FROM Driver d
        INNER JOIN Vehicle v ON d.vehicleID = v.vehicleID
    """)
    drivers = []
    for row in cursor.fetchall():
        driver = {
            'userID': row.userID,
            'name': row.name,
            'email': row.email,
            'phoneNumber': row.phoneNumber,
            'driverID': row.driverID,
            'vehicleID': row.vehicleID,
            'licensePlate': row.licensePlate,
            'makeModel': row.make_model,
            'capacity': row.capacity,
            'availableSeats': row.availableSeats,
            'rating': row.rating
        }
        drivers.append(driver)
    cursor.close()
    conn.close()
    return drivers


# Function to get all passenger details
def get_passengers():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.userID, u.name, u.email, u.phoneNumber, p.preferredPickupLocation, p.preferredDropLocation, p.rating
        FROM Userr u
        INNER JOIN Passenger p ON u.userID = p.userID
    """)
    passengers = []
    for row in cursor.fetchall():
        passenger = {
            'userID': row.userID,
            'name': row.name,
            'email': row.email,
            'phoneNumber': row.phoneNumber,
            'preferredPickupLocation': row.preferredPickupLocation,
            'preferredDropLocation': row.preferredDropLocation,
            'rating': row.rating
        }
        passengers.append(passenger)
    
    conn.close()
    return passengers

def log_notification(user_id, message, status='unread'):
    """
    Log a notification message to the database.
    Args:
        user_id (str): The ID of the user receiving the notification
        message (str): The notification message
        status (str): Status of notification (default 'unread')
    """
    notification_id = str(uuid.uuid4())
    conn = connect()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO Notification (notificationID, message, timestamp, status, userID)
            VALUES (?, ?, GETDATE(), ?, ?)
        """
        cursor.execute(query, (notification_id, message, status, user_id))
        conn.commit()
    except Exception as e:
        print(f"Error logging notification: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_user_notifications(user_id):
    """
    Get all notifications for a specific user
    """
    conn = connect()
    cursor = conn.cursor()
    try:
        query = """
            SELECT notificationID, message, timestamp, status
            FROM Notification
            WHERE userID = ?
            ORDER BY timestamp DESC
        """
        cursor.execute(query, (user_id,))
        notifications = [{
            'notificationID': row.notificationID,
            'message': row.message,
            'timestamp': row.timestamp,
            'status': row.status
        } for row in cursor.fetchall()]
        return notifications
    finally:
        cursor.close()
        conn.close()


# Fetch all users from the Userr table
def fetch_all_users():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Userr')
    rows = cursor.fetchall()
    users = []
    for row in rows:
        users.append({
            "userID": row.userID,
            "name": row.name,
            "email": row.email,
            "phoneNumber": row.phoneNumber,
            "role": row.role,
            "profilePicture": row.profilePicture,
            "rating": row.rating
        })
    conn.close()
    return users

# Fetch a user by userID
def fetch_user_by_id(user_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Userr WHERE userID = ?', user_id)
    row = cursor.fetchone()
    if row:
        user = {
            "userID": row.userID,
            "name": row.name,
            "email": row.email,
            "phoneNumber": row.phoneNumber,
            "role": row.role,
            "profilePicture": row.profilePicture,
            "rating": row.rating
        }
        conn.close()
        return user
    conn.close()
    return None

#fetch driver by userid
def fetch_driver_by_id(user_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Driver WHERE userID = ?', user_id)
    row = cursor.fetchone()
    if row:
        conn.close()
        return True
    conn.close()
    return False

# Insert a new user into the Userr table
def insert_user(user_id, name, email, phone_number, password, role, profile_picture, rating):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Userr (userID, name, email, phoneNumber, password, role, profilePicture, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, name, email, phone_number, password, role, profile_picture, rating))
    conn.commit()
    conn.close()
    return True

# Fetch notifications for a user from the Notification table
def fetch_notifications_for_user(user_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Notification WHERE userID = ?', user_id)
    rows = cursor.fetchall()
    notifications = []
    for row in rows:
        notifications.append({
            "notificationID": row.notificationID,
            "message": row.message,
            "timestamp": row.timestamp,
            "status": row.status
        })
    conn.close()
    return notifications

#function to fetch all drivers

def fetch_all_drivers():
    conn = connect()  # Ensure `connect()` is defined and returns a valid DB connection
    cursor = conn.cursor()
    
    # Execute the SQL query to fetch all drivers
    cursor.execute('SELECT * FROM Driver')
    rows = cursor.fetchall()
    
    # Convert rows into a list of dictionaries
    drivers = []
    for row in rows:
        drivers.append({
            "driverID": row.driverID,
            "licenseNumber": row.licenseNumber,
            "availableSeats": row.availableSeats,
            "rating": row.rating,
            "userID": row.userID,
            "vehicleID": row.vehicleID
        })
    
    # Close the connection and return the data
    conn.close()
    return drivers

# Function to validate a user by email and password
def validate_user(email, password):
    try:
        conn = connect()  # Ensure `connect()` is defined and returns a valid DB connection
        cursor = conn.cursor()
        
        # Query to check the credentials in the Userr table
        query = """
        SELECT * FROM Userr
        WHERE email = ? AND password = ?
        """
        
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        conn.close()

        # Return user if found, otherwise return None
        return user if user else None
    except Exception as e:
        print(f"Error validating user: {e}")
        return None
    
def register_user(name, email, phone, password):
    userID = str(uuid.uuid4())
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Userr (userID, name, email, phoneNumber, password, role)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (userID, name, email, phone, password, 'user'))  # Default role if needed
    conn.commit()
    conn.close()
    return userID

def insert_vehicle(vehicleID, make_model, capacity, licensePlate):
    
    vehicleID = str(uuid.uuid4())
    
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(''' INSERT INTO Vehicle (vehicleID, capacity, licensePlate, make_model) VALUES (?, ?, ?, ?) ''', (vehicleID, capacity, licensePlate, make_model))
    conn.commit()
    conn.close()

    return vehicleID


# Insert a new driver into the Driver table
def insert_driver(driver_id, license_number, available_seats, rating, user_id, vehicle_id, make_model, licensePlate):
    
    driver_id = str(uuid.uuid4())
    vehicle_id = insert_vehicle(vehicle_id, make_model, 0, licensePlate)
    
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Driver (driverID, licenseNumber, availableSeats, rating, userID, vehicleID)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (driver_id, license_number, available_seats, rating, user_id, vehicle_id))
    conn.commit()
    conn.close()
    return True

# Insert a new passenger into the Passenger table
def insert_passenger(preferred_pickup_location, preferred_drop_location, rating, user_id):
    
    passengerID = str(uuid.uuid4())
    
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Passenger (passengerID, preferredPickupLocation, preferredDropLocation, rating, userID)
        VALUES (?, ?, ?, ?, ?)
    ''', (passengerID, preferred_pickup_location, preferred_drop_location, rating, user_id))
    conn.commit()
    conn.close()
    return True

def insert_passenger_offer(user_id, start_location, end_location, available_seats, car_capacity, car_name, additional_note):
    conn = connect()
    cursor = conn.cursor()
    
    # Insert the offer into the PassengerOffer table
    cursor.execute("""
        INSERT INTO PassengerOffer (userID, startLocation, endLocation, availableSeats, carCapacity, carName, additionalNote, offerTimestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, user_id, start_location, end_location, available_seats, car_capacity, car_name, additional_note, datetime.now())
    
    conn.commit()  # Commit the transaction
    cursor.close()
    conn.close()


def get_passenger_offers():
    conn = connect()
    cursor = conn.cursor()

    # SQL Query to fetch passenger offers
    query = """
    SELECT 
        offerID, 
        userID, 
        startLocation, 
        endLocation, 
        availableSeats, 
        carCapacity, 
        carName, 
        additionalNote, 
        offerTimestamp 
    FROM PassengerOffer
    """
    cursor.execute(query)

    # Fetch all results
    offers = cursor.fetchall()

    # Format data as a list of dictionaries
    offers_list = []
    for row in offers:
        offers_list.append({
            "offerID": row[0],
            "userID": row[1],
            "startLocation": row[2],
            "endLocation": row[3],
            "availableSeats": row[4],
            "carCapacity": row[5],
            "carName": row[6],
            "additionalNote": row[7],
            "offerTimestamp": row[8],
        })
    return offers_list        
        
# Fetch all offers
def fetch_offers():
    conn = connect()
    cursor = conn.cursor()
    query = """
        SELECT 
            offerID, startLocation, endLocation, availableSeats, carCapacity, carName, additionalNote, offerTimestamp
        FROM 
            PassengerOffer
        WHERE 
            availableSeats > 0
        ORDER BY 
            offerTimestamp DESC
    """
    cursor.execute(query)
    offers = cursor.fetchall()
    conn.close()
    return offers

# Insert a driver acceptance into the DriverOffer table
def insert_driver_offer(passenger_offer_id, driver_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO DriverOffer (passengerOfferID, driverID, status)
        VALUES (?, ?, ?)
    """, (passenger_offer_id, driver_id, 'accepted'))
    conn.commit()
    conn.close()

def get_driver_id_by_user_id(user_id):
    """
    Fetches the driverID based on the given userID.
    
    Args:
        user_id (int): The user ID for which to fetch the driver ID.
    
    Returns:
        int: The driver ID if found, or None if no matching record exists.
    """
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT driverID FROM Driver WHERE userID = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        print(f"Error fetching driverID for userID {user_id}: {e}")
        return None


# Function to fetch accepted offers for a passenger and also get the driver's name, car details
def get_accepted_offers_for_passenger(user_id):
    query = """
    SELECT 
        d.driverOfferID,
        d.driverID,
        u.name AS driverName,  -- Fetch the driver's name from the Userr table
        v.vehicleID,  -- Fetch the vehicle ID from the Driver table
        v.make_model AS vehicleName,  -- Fetch the vehicle name (make and model) from the Vehicle table
        v.licensePlate AS vehicleNumber,  -- Fetch the vehicle license plate from the Vehicle table
        p.startLocation,
        p.endLocation,
        p.availableSeats,
        p.carName,
        d.status,
        d.offerTimestamp
    FROM 
        DriverOffer d
    INNER JOIN 
        PassengerOffer p
    ON 
        d.passengerOfferID = p.offerID
    INNER JOIN 
        Driver driverDetails
    ON
        d.driverID = driverDetails.driverID  -- Match the driverID
    INNER JOIN 
        Userr u
    ON 
        driverDetails.userID = u.userID  -- Match the userID from driverDetails to get the driver's name
    INNER JOIN
        Vehicle v
    ON
        driverDetails.vehicleID = v.vehicleID  -- Match the vehicleID from driverDetails to get vehicle details
    WHERE 
        p.userID = ? AND d.status = 'accepted'
    """
    
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Format the results into a dictionary
    offers = [
        {
            "driverOfferID": row[0],
            "driverID": row[1],
            "driverName": row[2],
            "vehicleID": row[3],  # Include vehicle ID
            "vehicleName": row[4],  # Include vehicle name
            "vehicleNumber": row[5],  # Include vehicle license plate number
            "startLocation": row[6],
            "endLocation": row[7],
            "availableSeats": row[8],
            "carName": row[9],
            "status": row[10],
            "offerTimestamp": row[11].strftime('%Y-%m-%d %H:%M:%S')  # Format timestamp to string
        }
        for row in rows
    ]
    
    return offers


    
# Function to create a new ride
def create_ride(passenger_offer_id, driver_offer_id):
    connection = connect()
    cursor = connection.cursor()
    try:
        query = """
            INSERT INTO Ride (passengerOfferID, driverOfferID, rideStatus)
            VALUES (?, ?, 'ongoing');
        """
        cursor.execute(query, (passenger_offer_id, driver_offer_id))
        connection.commit()
        return True
    except Exception as e:
        print("Error in create_ride:", e)
        return False
    finally:
        connection.close()

# Function to update ride status to 'completed'
def complete_ride(ride_id):
    connection = connect()
    cursor = connection.cursor()
    try:
        query = """
            UPDATE Ride
            SET rideStatus = 'completed', endTime = GETDATE()
            WHERE rideID = ?;
        """
        cursor.execute(query, (ride_id,))
        connection.commit()
        return True
    except Exception as e:
        print("Error in complete_ride:", e)
        return False
    finally:
        connection.close()



# Function to get the most recent passenger offer ID created by a passenger
def get_recent_passenger_offer(passenger_id):
    try:
        # Establish connection to the database
        conn = connect()
        cursor = conn.cursor()
        
        # SQL query to find the most recent passengerOfferID based on passengerID
        query = '''
        SELECT TOP 1 offerID
        FROM PassengerOffer
        WHERE userID = ?
        ORDER BY offerTimestamp DESC
        '''
        
        # Execute the query with the provided passengerID
        cursor.execute(query, (passenger_id,))
        
        # Fetch the result
        result = cursor.fetchone()
        
        if result:
            # Return the passengerOfferID
            return result.offerID
        else:
            return None  # No matching passenger offer found
        
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()
        
        
# Function to get the most recent driver offer ID based on the passenger offer ID
def get_recent_driver_offer(passenger_offer_id):
    try:
        # Establish connection to the database
        conn = connect()
        cursor = conn.cursor()
        
        # SQL query to find the most recent driverOfferID based on passengerOfferID
        query = '''
        SELECT TOP 1 driverOfferID
        FROM DriverOffer
        WHERE passengerOfferID = ?
        ORDER BY offerTimestamp DESC
        '''
        
        # Execute the query with the provided passengerOfferID
        cursor.execute(query, (passenger_offer_id,))
        
        # Fetch the result
        result = cursor.fetchone()
        
        if result:
            # Return the driverOfferID
            return result.driverOfferID
        else:
            return None  # No matching driver offer found
        
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()
        
        
# Function to fetch the most recent ride for a specific passenger
def fetch_most_recent_passenger_ride(user_id):
    conn = connect()  # Assuming connect() provides the correct database connection
    cursor = conn.cursor()
    
    query = """
    SELECT 
        passenger.name AS "Name of Passenger", 
        driver.name AS "Name of Driver",
        driver.phoneNumber AS "Driver Phone Number", 
        passengerOffer.startLocation AS "Starting Location", 
        passengerOffer.endLocation AS "Ending Location", 
        ride.rideStatus AS "Status of Ride", 
        ride.startTime AS "Start Time", 
        ride.endTime AS "End Time"
    FROM 
        Ride ride
    JOIN 
        PassengerOffer passengerOffer ON ride.passengerOfferID = passengerOffer.offerID
    JOIN 
        DriverOffer driverOffer ON ride.driverOfferID = driverOffer.driverOfferID
    JOIN 
        Userr passenger ON passengerOffer.userID = passenger.userID
    JOIN 
        Driver driverDetails ON driverOffer.driverID = driverDetails.driverID
    JOIN 
        Userr driver ON driverDetails.userID = driver.userID
    WHERE 
        passengerOffer.userID = ?  -- Filter by the specific passenger's userID
    ORDER BY 
        ride.startTime DESC
    OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY;  -- MSSQL syntax to get the most recent ride (equivalent to LIMIT 1)
    """
    
    cursor.execute(query, (user_id,))
    ride = cursor.fetchone()  # Fetch the most recent ride
    conn.close()

    if ride:
        return {
            "Name of Passenger": ride[0],
            "Name of Driver": ride[1],
            "Driver Phone Number": ride[2],
            "Starting Location": ride[3],
            "Ending Location": ride[4],
            "Status of Ride": ride[5],
            "Start Time": ride[6],
            "End Time": ride[7]
        }
    return None  # No ride found


# Function to fetch the most recent ride for a specific driver using userID
def fetch_most_recent_driver_ride(user_id):
    conn = connect()  # Assuming connect() provides the correct database connection
    cursor = conn.cursor()
    
    query = """
    SELECT 
        passenger.name AS "Name of Passenger", 
        driver.name AS "Name of Driver", 
        passengerOffer.startLocation AS "Starting Location", 
        passengerOffer.endLocation AS "Ending Location", 
        ride.rideStatus AS "Status of Ride", 
        ride.startTime AS "Start Time", 
        ride.endTime AS "End Time"
    FROM 
        Ride ride
    JOIN 
        PassengerOffer passengerOffer ON ride.passengerOfferID = passengerOffer.offerID
    JOIN 
        DriverOffer driverOffer ON ride.driverOfferID = driverOffer.driverOfferID
    JOIN 
        Userr passenger ON passengerOffer.userID = passenger.userID
    JOIN 
        Driver driverDetails ON driverOffer.driverID = driverDetails.driverID
    JOIN 
        Userr driver ON driverDetails.userID = driver.userID
    WHERE 
        driver.userID = ?  -- Filter by the specific driver's userID
    ORDER BY 
        ride.startTime DESC
    OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY;  -- MSSQL syntax to get the most recent ride (equivalent to LIMIT 1)
    """
    
    cursor.execute(query, (user_id,))
    ride = cursor.fetchone()  # Fetch the most recent ride
    conn.close()

    if ride:
        return {
            "Name of Passenger": ride[0],
            "Name of Driver": ride[1],
            "Starting Location": ride[2],
            "Ending Location": ride[3],
            "Status of Ride": ride[4],
            "Start Time": ride[5],
            "End Time": ride[6]
        }
    return None  # No ride found


# Function to change the ride status to 'completed' based on rideID
def mark_ride_as_completed(ride_id):
    conn = connect()  # Establish the database connection
    cursor = conn.cursor()

    # Get the current time to set as the end time
    current_time = datetime.now()

    # SQL query to update the ride status and set the end time
    query = """
    UPDATE Ride
    SET rideStatus = 'completed',
        endTime = ?
    WHERE rideID = ? AND rideStatus != 'completed'
    """
    
    try:
        # Execute the update query
        cursor.execute(query, (current_time, ride_id))
        
        # Commit the changes to the database
        conn.commit()
        
        # Check if any rows were updated
        if cursor.rowcount > 0:
            print(f"Ride {ride_id} status updated to 'completed'.")
        else:
            print(f"Ride {ride_id} could not be updated or is already completed.")
    
    except Exception as e:
        print(f"Error updating ride status: {e}")
        conn.rollback()  # Rollback in case of error

    finally:
        cursor.close()
        conn.close()
        

# Function to change the most recent ride status to 'completed' based on user_id
def change_latest_ride_status_to_completed(user_id):
    conn = connect()  # Establish the database connection
    cursor = conn.cursor()

    # Get the current time for the endTime
    current_time = datetime.now()

    query = """
    UPDATE Ride
    SET rideStatus = 'completed',
        endTime = ?
    WHERE rideID = (
        SELECT TOP 1 ride.rideID
        FROM Ride ride
        JOIN DriverOffer driverOffer ON ride.driverOfferID = driverOffer.driverOfferID
        JOIN Driver driver ON driverOffer.driverID = driver.driverID
        WHERE driver.userID = ?
        ORDER BY ride.startTime DESC
    )
    AND rideStatus != 'completed'
    """

    try:
        # Execute the update query
        cursor.execute(query, (current_time, user_id))
        conn.commit()  # Commit the changes

        # Check if the update affected any rows
        if cursor.rowcount > 0:
            print(f"Ride status updated to 'completed' for user_id {user_id}.")
        else:
            print(f"No ongoing ride found for user_id {user_id}, or the ride is already completed.")

    except Exception as e:
        print(f"Error updating ride status: {e}")
        conn.rollback()  # Rollback in case of error

    finally:
        cursor.close()
        conn.close()
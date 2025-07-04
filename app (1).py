import os
import random
import requests
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from db import fetch_all_users, fetch_user_by_id, insert_user, fetch_notifications_for_user, fetch_all_drivers, validate_user, register_user,insert_passenger, insert_driver, insert_passenger_offer, get_passenger_offers, fetch_offers, insert_driver_offer, get_driver_id_by_user_id, get_accepted_offers_for_passenger,create_ride, complete_ride, get_recent_driver_offer, get_recent_passenger_offer, fetch_most_recent_passenger_ride, fetch_most_recent_driver_ride, change_latest_ride_status_to_completed, fetch_driver_by_id, get_user_details, get_passenger_details, update_passenger_profile, get_passengers, log_notification, get_user_notifications, get_drivers, get_driver_details
from flask_mail import Mail, Message



###################################################################################################
######################################### OOP CLASSES #############################################
###################################################################################################

class Offer:
    def __init__(self, user_id, start_location, end_location, available_seats, car_capacity, car_name, additional_note=None):
        self.user_id = user_id
        self.start_location = start_location
        self.end_location = end_location
        self.available_seats = available_seats
        self.car_capacity = car_capacity
        self.car_name = car_name
        self.additional_note = additional_note

    def create(self):
        if not all([self.start_location, self.end_location, self.available_seats, self.car_capacity, self.car_name]):
            return "Missing required fields", 400
        try:
            self.available_seats = int(self.available_seats)
            self.car_capacity = int(self.car_capacity)
        except ValueError:
            return "Invalid number for seats or capacity", 400
        # Insert into database logic here
        insert_passenger_offer(self.user_id, self.start_location, self.end_location, self.available_seats, self.car_capacity, self.car_name, self.additional_note)
        return jsonify({"success": True}), 200


class Ride:
    def __init__(self, passenger_offer_id, driver_offer_id):
        self.passenger_offer_id = passenger_offer_id
        self.driver_offer_id = driver_offer_id

    def start(self):
        success = create_ride(self.passenger_offer_id, self.driver_offer_id)
        if success:
            return jsonify({"success": True, "message": "Ride started successfully"})
        else:
            return jsonify({"success": False, "message": "Failed to start ride"}), 500

    def complete(self):
        result = change_latest_ride_status_to_completed(session['userID'])
        return jsonify(result)


class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def is_logged_in(self):
        return self.user_id is not None

    def get_offers(self):
        return get_passenger_offers()
    
    
class GoogleMapsAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def places_autocomplete(self, query):
        """Autocomplete suggestions for places."""
        if not query:
            return {"error": "Query parameter is required"}, 400

        base_url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
        params = {
            "input": query,
            "key": self.api_key,
            "types": "(cities)",  # Restrict results to cities (optional, modify as needed)
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK":
                predictions = [{"description": p["description"], "place_id": p["place_id"]} for p in data.get("predictions", [])]
                return predictions, 200
            else:
                return {"error": data.get("status")}, 400
        return {"error": "Failed to fetch autocomplete suggestions"}, 500

    def geocode(self, address):
        """Get latitude and longitude for a given address."""
        if not address:
            return {"error": "Address is required"}, 400
        
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": address,
            "key": self.api_key
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                location = data['results'][0]['geometry']['location']
                return {'latitude': location['lat'], 'longitude': location['lng']}, 200
            else:
                return {'error': data['status']}, 400
        else:
            return {'error': 'Failed to fetch coordinates'}, 500

    def get_distance(self, origin, destination):
        """Get distance and duration between two locations."""
        if not origin or not destination:
            return {'error': 'Origin and destination are required'}, 400
        
        base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": origin,
            "destinations": destination,
            "key": self.api_key,
            "mode": "driving"
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                element = data['rows'][0]['elements'][0]
                if element['status'] == 'OK':
                    return {
                        'distance': element['distance']['text'],
                        'duration': element['duration']['text']
                    }, 200
                else:
                    return {'error': element['status']}, 400
            else:
                return {'error': data['status']}, 400
        else:
            return {'error': 'Failed to fetch distance/duration'}, 500
    
    
    
    
# Load Google Maps API Key from environment variable
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_API_KEY") or "YOUR_GOOGLE_MAPS_API_KEY"

app = Flask(__name__, static_folder='static', template_folder='templates')

app.secret_key = 'your-secret-key'  # Replace 'your-secret-key' with a strong, random string


app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'waleedbinaamer2003@gmail.com'
app.config['MAIL_PASSWORD'] = 'ffir lilo llkb baur'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


mail = Mail(app)  # Updated OTP range for clarity
    
###################################################################################################
##################################        API TEMPLATE ROUTES          ############################
###################################################################################################

@app.route('/', methods=['GET'])
def homePage():
    return render_template('homePage.html')  # Serves your HTML page

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')  # Render the login page

@app.route('/driver', methods=['GET'])
def driver():
    return render_template('driver.html')  # Serves your HTML page


@app.route('/sch', methods=['GET'])
def sch():
    return render_template('sch.html')  # Serves your HTML page

@app.route('/notif', methods=['GET'])
def notif():
    return render_template('notif.html')  # Serves your HTML page

@app.route('/passengerDashboard', methods=['GET'])
def passengerDashboard():
    return render_template('passengerDash.html')  # Serves your HTML page

@app.route('/passengerDriverDetails.html', methods=['GET'])
def passengerDriverDetails():
    return render_template('passengerDriverDeet.html')  # Serves your HTML page

@app.route('/admin')
def admin_dashboard():
    return render_template('adminDashboard.html')

@app.route('/passengerprofile', methods=['GET'])
def passprofile():
    return render_template('passengerProfile.html')  # Render the login page

@app.route('/passnotif', methods=['GET'])
def passnotif():
    return render_template('passnotif.html')  # Render the login page

@app.route('/switchmode', methods=['GET'])
def switchmode():
    if(fetch_driver_by_id(session.get('userID'))):
        return driver()
    else:
        return render_template('driverRegister.html')
    
@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')  # Render the registration page

@app.route('/passengerDash')
def passenger_dash():
    u_name = session.get('name', 'Guest')  # Default to 'Guest' if not logged in
    return render_template('passengerDash.html', user_name=u_name)

@app.route('/driverRegistration', methods=['GET'])
def driver_details_page():
    return render_template('driverRegister.html')  # Serves the HTML page

@app.route('/verification', methods=["GET"])
def verification():
    return render_template("index.html")

@app.route('/verify', methods=['GET'])
def verify():
    return render_template('verify.html')

@app.route('/createoffer', methods=['GET'])
def createoffer():
    return render_template('createoffer.html')


@app.route('/offer_success')
def offer_success():
    return "Your offer has been successfully created!"


@app.route('/driver')
def driver_page():
    u_name = session.get('name', 'Guest')
    return render_template('driver.html', user_name=u_name)

@app.route('/profile', methods=['GET'])
def profile():
    user_id = session.get('userID')  # Get the user ID from query params
    user_data = get_user_details(user_id)
    driver_data = get_driver_details(user_id)
    if not user_data or not driver_data:
        return "User or passenger details not found.", 404
    return render_template(
        'profile.html',
        userID=user_id,
        name=user_data['name'],
        email=user_data['email'],
        phone=user_data['phoneNumber'],
        profilePicture=user_data['profilePicture'],
        rating=user_data['rating'],
        password=user_data['password'],
        vehicleID=driver_data['vehicleID'],
        licensePlate=driver_data['licensePlate'],
        make_model=driver_data['make_model'],
        availableSeats=driver_data['availableSeats']
    )


@app.route('/passenger-ride')
def passenger_ride():
    ride = fetch_most_recent_passenger_ride(session['userID'])
    if ride:
        return render_template('pRide.html', ride=ride)
    return "No rides found for this passenger."


@app.route('/driver-ride')
def driver_ride():
    ride = fetch_most_recent_driver_ride(session['userID'])
    if ride:
        return render_template('dRide.html', ride=ride)
    return "No rides found for this driver."
    

###################################################################################################
##################################        API FUNCTION ROUTES          ############################
###################################################################################################


google_maps_api = GoogleMapsAPI(GOOGLE_MAPS_API_KEY)

@app.route('/create_offer', methods=['POST'])
def create_offer():
    user_id = session.get('userID')
    if not user_id:
        return "User not logged in", 401

    offer_data = request.get_json()
    if not offer_data:
        return "No data provided", 400

    offer = Offer(
        user_id=user_id,
        start_location=offer_data.get('startLocation'),
        end_location=offer_data.get('endLocation'),
        available_seats=offer_data.get('availableSeats'),
        car_capacity=offer_data.get('carCapacity'),
        car_name=offer_data.get('carName'),
        additional_note=offer_data.get('additionalNote')
    )
    return offer.create()


@app.route('/api/passenger-offers', methods=['GET'])
def fetch_passenger_offers():
    user_id = session.get('userID')
    if not user_id:
        return jsonify({"success": False, "message": "User not logged in"}), 401

    user = User(user_id)
    offers = user.get_offers()
    return jsonify(offers)

@app.route('/get_offers', methods=['GET'])
def get_offers():
    try:
        offers = fetch_offers()
        offer_list = [
            {
                'offerID': offer[0],
                'startLocation': offer[1],
                'endLocation': offer[2],
                'availableSeats': offer[3],
                'carCapacity': offer[4],
                'carName': offer[5],
                'additionalNote': offer[6],
                'offerTimestamp': offer[7].strftime('%Y-%m-%d %H:%M:%S'),
            }
            for offer in offers
        ]
        return jsonify({'success': True, 'offers': offer_list})
    except Exception as e:
        print("Error fetching offers:", e)
        return jsonify({'success': False, 'message': 'Failed to fetch offers'}), 500


@app.route('/accept_offer', methods=['POST'])
def accept_offer():
    data = request.json
    offer_id = data.get('offerID')
    driver_id = get_driver_id_by_user_id(session.get('userID'))

    if not driver_id:
        return jsonify({'success': False, 'message': 'Driver not logged in'}), 401

    insert_driver_offer(offer_id, driver_id)
    return jsonify({'success': True})


@app.route('/get_accepted_offers', methods=['GET'])
def get_accepted_offers():
    user_id = session.get('userID')
    if not user_id:
        return jsonify({"success": False, "message": "User not logged in"}), 401

    try:
        offers = get_accepted_offers_for_passenger(user_id)
        return jsonify({"success": True, "offers": offers})
    except Exception as e:
        print(f"Error fetching accepted offers: {e}")
        return jsonify({"success": False, "message": "Error fetching accepted offers"}), 500


@app.route('/start_ride', methods=['POST'])
def start_ride():
    if 'userID' not in session:
        return jsonify({"success": False, "message": "User not logged in"}), 401

    data = request.json
    passenger_offer_id = get_recent_passenger_offer(session.get('userID'))
    driver_offer_id = get_recent_driver_offer(passenger_offer_id)

    if not passenger_offer_id or not driver_offer_id:
        return jsonify({"success": False, "message": "Invalid data provided"}), 400

    ride = Ride(passenger_offer_id, driver_offer_id)
    return ride.start()


@app.route('/complete_ride', methods=['POST'])
def complete_ride():
    data = request.get_json()
    ride = Ride(data.get('passengerOfferID'), data.get('driverOfferID'))
    return ride.complete()

@app.route('/passenger-profile', methods=['GET'])
def passenger_profile():
    user_id = session.get('userID')  # Get the user ID from query params
    user_data = get_user_details(user_id)
    passenger_data = get_passenger_details(user_id)
    if not user_data or not passenger_data:
        return "User or passenger details not found.", 404
    return render_template(
        'passengerProfile.html',
        userID=user_id,
        name=user_data['name'],
        email=user_data['email'],
        phone=user_data['phoneNumber'],
        profilePicture=user_data['profilePicture'],
        rating=user_data['rating'],
        password=user_data['password'],
        preferredPickupLocation=passenger_data['preferredPickupLocation'],
        preferredDropLocation=passenger_data['preferredDropLocation'],
        passengerID=passenger_data['passengerID']
    )

@app.route('/update_profile', methods=['POST'])
def update_profile():
    # Parse form data
    data = request.get_json()
    user_id = data.get("userID")
    phone = data.get("phone")
    pickup = data.get("pickup")
    drop = data.get("drop")
    password = data.get("pass")

    try:
        # Update the passenger profile
        update_passenger_profile(user_id, phone, pickup, drop, password)
        # Redirect back to the profile page after updating
        return jsonify({"message": "Profile updated successfully!"}), 200
    except Exception as e:
        return f"An error occurred while updating the profile: {e}", 500

@app.route('/admin/dashboard')
def dashboard_data():
    role = request.args.get('role', 'all')
    try:
        if role == 'driver':
            users = get_drivers()
            # Convert each user object to a dict with serializable values
            users_list = [
                {
                    'userID': user['userID'],
                    'name': user['name'],
                    'email': user['email'],
                    'phoneNumber': user['phoneNumber'],
                    'vehicleID': user['vehicleID'],
                    'licensePlate': user['licensePlate'],
                    'makeModel': user['makeModel'],
                    'capacity': user['capacity'],
                    'availableSeats': user['availableSeats'],
                    'rating': float(user['rating']) if user['rating'] else None
                } for user in users
            ]
        elif role == 'passenger':
            users = get_passengers()
            # Convert each user object to a dict with serializable values 
            users_list = [
                {
                    'userID': user['userID'],
                    'name': user['name'],
                    'email': user['email'],
                    'phoneNumber': user['phoneNumber'],
                    'preferredPickupLocation': user['preferredPickupLocation'],
                    'preferredDropLocation': user['preferredDropLocation'],
                    'rating': float(user['rating']) if user['rating'] else None
                } for user in users
            ]
        else:
            users_list = []
            
        return jsonify(users_list)
    except Exception as e:
        print(f"Error in dashboard_data: {str(e)}")
        return jsonify([]), 500

@app.route('/log_notification', methods=['POST'])
def log_notification_route():
    data = request.get_json()
    try:
        log_notification(
            data.get('userID'),
            data.get('message'),
            data.get('status', 'unread')
        )
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/get-notifications', methods=['GET'])
def get_notifications():
    user_id = session.get('userID')
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    try:
        notifications = get_user_notifications(user_id)
        return jsonify(notifications), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validate the user with the provided email and password
    user = validate_user(email, password)
    
    if user:

        # Store user ID or relevant data in the session
        session['userID'] = user[0]
        session['name'] = user[1]
        session['email'] = user[2]
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401


# Route to handle the registration form submission (POST request)
@app.route('/register', methods=['POST'])
def register():
    try:
        # Get the JSON data sent from the frontend
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        role = data.get('role')  # Include role if applicable

        # Validate that all required fields are provided
        if not all([name, email, phone, password, role]):
            return jsonify({"error": "All fields are required"}), 400

        # Store the registration data in the session temporarily
        session['registration_data'] = {
            'name': name,
            'email': email,
            'phone': phone,
            'password': password,
            'role': role
        }

        # Generate a 6-digit OTP
        otp = random.randint(100000, 999999)
        session['otp'] = otp  # Store OTP in session

        # Send OTP to the user's email
        msg = Message('OTP Verification', sender='your-email@example.com', recipients=[email])
        msg.body = f"Your OTP is {otp}"
        mail.send(msg)

        return jsonify({"message": "OTP sent to your email address"}), 200
    except Exception as e:
        print(f"Error during registration: {e}")
        return jsonify({"error": "An error occurred during registration"}), 500



# Route to fetch all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = fetch_all_users()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to fetch user by userID
@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = fetch_user_by_id(user_id)
        if user:
            return jsonify(user), 200
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to add a new user
@app.route('/user', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        
        user_id = data.get('userID')
        name = data.get('name')
        email = data.get('email')
        phone_number = data.get('phoneNumber')
        password = data.get('password')
        role = data.get('role')
        profile_picture = data.get('profilePicture', None)
        rating = data.get('rating', None)
        
        # Insert new user
        if insert_user(user_id, name, email, phone_number, password, role, profile_picture, rating):
            return jsonify({"message": "User added successfully!"}), 201
        return jsonify({"message": "Failed to add user"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


    
@app.route('/getDrivers', methods=['GET'])
def get_drivers_api():
    try:
        # Fetch all drivers using a helper function from db.py
        drivers = fetch_all_drivers()  # Ensure this function exists in db.py
        if drivers:
            return jsonify(drivers), 200
        return jsonify({"message": "No drivers found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/submitDriverDetails', methods=['POST'])
def submit_driver_details():
    try:
        data = request.get_json()
        car_make_model = data.get('carMakeModel')
        license_number = data.get('licenseNumber')
        number_plate = data.get('numberPlate')

        if not all([car_make_model, license_number, number_plate]):
            return jsonify({"success": False, "message": "All fields are required"}), 400

        # Example: Insert driver details into the database (replace with actual DB code)
        # insert_driver_details(car_make_model, license_number, number_plate)

        userid = session.get('userID')

        insert_driver(0, license_number, 0, 0, userid ,0, car_make_model, number_plate)

        return jsonify({"success": True, "message": "Driver details submitted successfully!"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500
    
# New route to save pickup location
@app.route('/save_pickup_location', methods=['POST'])
def save_pickup_location():
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if latitude and longitude:
            # Save location to the database or process further
            # Example: update the user's pickup location in the database
            # save_user_pickup_location(user_id, latitude, longitude)
            return jsonify({"message": "Pickup location saved successfully!", "latitude": latitude, "longitude": longitude}), 200
        else:
            return jsonify({"error": "Invalid location data"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Route to fetch places (autocomplete) suggestions
@app.route('/places', methods=['GET'])
def places_autocomplete():
    query = request.args.get('query')
    result, status = google_maps_api.places_autocomplete(query)
    return jsonify(result), status


# Route to get latitude and longitude for an address (geocode)
@app.route('/geocode', methods=['POST'])
def geocode():
    data = request.get_json()
    address = data.get('address')
    result, status = google_maps_api.geocode(address)
    return jsonify(result), status


# Route to get distance between two locations
@app.route('/distance', methods=['POST'])
def distance():
    data = request.get_json()
    origin = data.get('origin')
    destination = data.get('destination')
    result, status = google_maps_api.get_distance(origin, destination)
    return jsonify(result), status
    
@app.route('/logout')
def logout():
    response = jsonify({"message": "Logged out"})
    response.delete_cookie('session')  # Replace 'session' with the cookie name
    return response
    

@app.route('/validate', methods=["POST"])
def validate():
    user_otp = request.form.get('otp')
    otp = session.get('otp')
    otp_timestamp = session.get('otp_timestamp')

    # Verify the OTP
    if int(user_otp) == otp:
        # Retrieve registration data from session
        registration_data = session.get('registration_data')
        if not registration_data:
            return "<h3>Registration data not found. Please try registering again.</h3>"

        name = registration_data['name']
        email = registration_data['email']
        phone = registration_data['phone']
        password = registration_data['password']
        role = registration_data['role']

        try:
            # Add the user to the database
            userID = register_user(name, email, phone, password)

            insert_passenger(None, None, 5.0, userID)
            session['userID'] = userID
        
            if role == 'driver':
                # Redirect to driver details form
                return render_template('driverRegister.html')
            else:
                return redirect(url_for('passengerDashboard'))
        except Exception as e:
            print(f"Error during user registration: {e}")
            return "<h3>An error occurred during registration. Please try again.</h3>"
        finally:
            # Clean up session data
            session.pop('otp', None)
            session.pop('otp_timestamp', None)
            session.pop('registration_data', None)
    else:
        return "<h3>Invalid OTP. Please try again.</h3>"

if __name__ == '__main__':
    app.run(debug=True,port=5000)



**GoFAST – Ride Management Backend (Flask)**

GoFAST is a Flask-based backend application designed to handle the core functionalities of a ride-hailing or transport management system. It provides backend logic for managing drivers, passengers, rides, database models, and email notifications through a REST-style API.

This project focuses on backend architecture, API design, and scalable Python application development.

**Features**

Ride creation and completion system

Driver and passenger role handling

Database integration using structured models

Email notifications using a mailer service

REST-style API endpoints

Environment-based configuration using .env

Basic testing support

Tech Stack

Backend: Python, Flask

Database: SQL-based database (configured in db.py)

Email Service: SMTP (configured in mailer.py)

Environment Management: python-dotenv

**Project Structure
GoFAST/**
│
├── app.py           # Main Flask application
├── db.py            # Database connection and setup
├── models.py        # Database models
├── mailer.py        # Email notification logic
├── test.py          # Testing file
├── new.py           # Additional or experimental logic
├── .env             # Environment variables (not committed)
└── .gitattributes

**Installation and Setup
1. Clone the repository**
git clone https://github.com/USERNAME/GoFAST.git
cd GoFAST

**2. Create a virtual environment (recommended)**
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

**3. Install dependencies**
pip install flask requests python-dotenv


(Install additional libraries if required for your database or email service.)

**4. Environment Variables**

Create a .env file in the root directory:

FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
MAIL_USERNAME=your_email
MAIL_PASSWORD=your_email_password

**5. Run the application**
python app.py


**The server will start on:**

http://127.0.0.1:5000/

API Overview

The backend provides endpoints for:

Creating rides

Completing rides

Fetching driver ride offers

Fetching passenger ride requests

Endpoint logic is implemented inside app.py.

Testing

Run the test file using:

python test.py



**Author and Contributors**

Waleed Bin Aamer

Maria Nadeem

Dia Ejaz

Shamikh Naqvi

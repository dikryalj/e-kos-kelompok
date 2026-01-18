# e_kost

A Flask-based web application for managing kost (boarding house) rooms and bookings.

## Project Structure

```
e_kost/
│
├── venv/                     # virtual environment
│
├── app.py                    # main Flask application file
├── config.py                 # application and database configuration
├── requirements.txt          # list of required libraries
│
├── templates/                # HTML templates
│   ├── base.html             # main layout (navbar, footer)
│   ├── index.html            # home page
│   ├── rooms.html            # list of rooms
│   ├── booking.html          # booking form
│   └── admin/                # admin pages
│       ├── login.html
│       ├── dashboard.html
│       └── rooms.html
│
├── static/                   # static files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── uploads/              # room photos
│
├── models.py                 # database models (Room, Booking, Admin)
└── README.md
```

## Setup

1. Create virtual environment:

   ```
   python -m venv venv
   ```

2. Activate virtual environment:

   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

## Features

- Room listing and management
- Booking system
- Admin dashboard
- User authentication

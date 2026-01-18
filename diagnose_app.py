import os
from app import app, db, Room

def test_render():
    print("Testing rooms rendering...")
    with app.app_context():
        try:
            # Check database synchronization
            rooms_count = Room.query.count()
            print(f"Database sync check: Found {rooms_count} rooms.")
            
            # Check if any room has been found
            if rooms_count == 0:
                print("WARNING: No rooms found in database. Seed needed?")
            
            # Simulated render check
            from flask import render_template
            test_rooms = Room.query.limit(3).all()
            rendered = render_template('rooms.html', rooms=test_rooms)
            if 'Filter Pencarian' in rendered:
                print("SUCCESS: rooms.html rendered correctly with search filters.")
            else:
                print("FAILURE: rooms.html missing key components.")
                
            rendered_booking = render_template('booking.html')
            if 'Booking' in rendered_booking:
                print("SUCCESS: /booking rendered correctly.")
                
        except Exception as e:
            print(f"ERROR during rendering check: {str(e)}")

if __name__ == "__main__":
    test_render()

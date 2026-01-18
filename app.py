import os
from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, User, Room, Tenant, Payment, Booking
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
from functools import wraps
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(Config)

# Configure Uploads
UPLOAD_FOLDER = 'static/uploads/proofs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(os.path.join(app.root_path, UPLOAD_FOLDER), exist_ok=True)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# decorator for admin only access
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Akses ditolak. Anda bukan admin.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.cli.command("init-db")
def init_db():
    db.drop_all() 
    db.create_all()
    
    # Create Default Admin
    admin = User(username='admin', role='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Create Seed Rooms for Griya Kost Amalia
    facilities = "Wifi, Lemari, Kasur, Bantal, Ember Gayung, Tempat Jemur, Include Listrik"
    
    rooms_data = []
    # 6 KM Luar
    for i in range(1, 7):
        rooms_data.append({'room_number': f'Luar {i:02d}', 'price': 350000, 'facilities': facilities})
    # 6 KM Dalam
    for i in range(1, 7):
        rooms_data.append({'room_number': f'Dalam {i:02d}', 'price': 420000, 'facilities': facilities})
    
    for r in rooms_data:
        room = Room(
            room_number=r['room_number'],
            price=r['price'],
            facilities=r['facilities'],
            status='available'
        )
        db.session.add(room)
        
    db.session.commit()
    print("Database initialized with Griya Kost Amalia data.")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/rooms")
def rooms():
    # Filter Parameters
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    room_type = request.args.get('type')
    
    query = Room.query
    
    if min_price:
        query = query.filter(Room.price >= min_price)
    if max_price:
        query = query.filter(Room.price <= max_price)
    if room_type and room_type != 'Semua':
        if room_type == 'Kamar Mandi Dalam':
            query = query.filter(Room.price == 420000)
        elif room_type == 'Kamar Mandi Luar':
            query = query.filter(Room.price == 350000)
            
    rooms = query.all()
    return render_template('rooms.html', rooms=rooms)

@app.route("/booking", methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        try:
            new_booking = Booking(
                name=request.form['name'],
                email=request.form['email'],
                phone=request.form['phone'],
                occupation=request.form['occupation'],
                room_type=request.form.get('room', 'N/A'),
                checkin_date=datetime.strptime(request.form['checkin'], '%Y-%m-%d').date(),
                duration=int(request.form['duration']),
                notes=request.form.get('notes', '')
            )
            db.session.add(new_booking)
            db.session.commit()
            flash('Booking berhasil dikirim! Kami akan segera menghubungi Anda.', 'success')
            return redirect(url_for('booking'))
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
            return redirect(url_for('booking'))
            
    return render_template('booking.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_inbox'))
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            # Redirect to admin inbox if admin
            if user.role == 'admin':
                return redirect(url_for('admin_inbox'))
            return redirect(url_for('index'))
        flash('Username atau password salah.', 'error')
            
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# --- ADMIN ROUTES ---

@app.route("/admin/inbox")
@admin_required
def admin_inbox():
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return render_template('admin/inbox.html', bookings=bookings)

@app.route("/admin/booking/delete/<int:id>", methods=['POST'])
@admin_required
def delete_booking(id):
    booking = Booking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    flash('Permintaan booking berhasil dihapus.', 'success')
    return redirect(url_for('admin_inbox'))

if __name__ == "__main__":
    app.run(debug=True)

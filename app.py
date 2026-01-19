import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_from_directory
from config import Config
from models import db, User, Room, Tenant, Payment, Booking, OTP, Notification
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
from functools import wraps
from werkzeug.utils import secure_filename
from email_service import EmailService
import urllib.parse

app = Flask(__name__)
app.config.from_object(Config)

# Configure Uploads
UPLOAD_FOLDER = 'static/uploads/proofs'
PROFILE_UPLOAD_FOLDER = 'static/uploads/profiles'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROFILE_UPLOAD_FOLDER'] = PROFILE_UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
os.makedirs(os.path.join(app.root_path, UPLOAD_FOLDER), exist_ok=True)
os.makedirs(os.path.join(app.root_path, PROFILE_UPLOAD_FOLDER), exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

# Route to serve images from img folder
@app.route('/img/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(app.root_path, 'img'), filename)

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
@login_required
def booking():
    if request.method == 'POST':
        try:
            new_booking = Booking(
                user_id=current_user.id,
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
            
            # Send booking confirmation email
            booking_data = {
                'name': new_booking.name,
                'email': new_booking.email,
                'phone': new_booking.phone,
                'room_type': new_booking.room_type,
                'checkin_date': new_booking.checkin_date.strftime('%d %B %Y'),
                'duration': new_booking.duration
            }
            EmailService.send_booking_confirmation_email(new_booking.email, booking_data)
            
            # Create notification for user
            notification = Notification(
                title='Booking Berhasil!',
                message=f'Booking Anda untuk tipe kamar {new_booking.room_type} telah diterima. Kami akan segera menghubungi Anda.',
                notification_type='booking',
                is_global=False,
                user_id=current_user.id
            )
            db.session.add(notification)
            db.session.commit()
            
            # Store booking data in session for WhatsApp redirect
            session['last_booking'] = {
                'name': new_booking.name,
                'phone': new_booking.phone,
                'room_type': new_booking.room_type,
                'checkin_date': new_booking.checkin_date.strftime('%d %B %Y'),
                'duration': new_booking.duration
            }
            
            flash('Booking berhasil dikirim! Kami akan segera menghubungi Anda.', 'success')
            return redirect(url_for('booking_success'))
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
            return redirect(url_for('booking'))
            
    return render_template('booking.html')

@app.route("/booking/success")
@login_required
def booking_success():
    booking_data = session.get('last_booking')
    if not booking_data:
        return redirect(url_for('index'))
    return render_template('booking_success.html', booking=booking_data)

@app.route("/booking/whatsapp")
@login_required
def booking_whatsapp():
    booking_data = session.get('last_booking')
    if not booking_data:
        return redirect(url_for('index'))
    
    # Format WhatsApp message
    message = f"""Halo, saya ingin konfirmasi booking:

Nama: {booking_data['name']}
Tipe Kamar: {booking_data['room_type']}
Tanggal Check-in: {booking_data['checkin_date']}
Durasi: {booking_data['duration']} bulan

Mohon informasi lebih lanjut. Terima kasih!"""
    
    # WhatsApp number (admin/owner number) from config
    # Format: hanya angka, tanpa + atau spasi, contoh: 6281234567890
    whatsapp_number = app.config.get('WHATSAPP_NUMBER', '')
    
    # Bersihkan nomor dari karakter non-digit
    whatsapp_number = ''.join(filter(str.isdigit, whatsapp_number))
    
    # Validasi nomor WhatsApp
    if not whatsapp_number or len(whatsapp_number) < 10:
        flash('Nomor WhatsApp owner belum dikonfigurasi dengan benar.', 'error')
        return redirect(url_for('booking_success'))
    
    # Encode message for URL
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"
    
    return redirect(whatsapp_url)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            flash('Password tidak cocok!', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=username).first():
            flash('Username sudah digunakan!', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email sudah terdaftar!', 'error')
            return redirect(url_for('register'))
        
        # Store registration data in session
        session['registration_data'] = {
            'username': username,
            'email': email,
            'full_name': full_name,
            'phone': phone,
            'password': password
        }
        
        # Send OTP to email
        result = EmailService.send_otp_email(email)
        email_sent, otp_code = result
        
        if email_sent:
            if otp_code:
                # Dev mode - tampilkan OTP di flash message untuk testing
                flash(f'[DEV MODE] Kode OTP Anda: {otp_code}', 'info')
            flash('Kode OTP telah dikirim ke email Anda. Silakan cek inbox atau spam folder.', 'success')
            return redirect(url_for('verify_otp'))
        else:
            flash('Gagal mengirim email. Pastikan email Anda benar.', 'error')
            return redirect(url_for('register'))
            
    return render_template('register.html')

@app.route("/verify-otp", methods=['GET', 'POST'])
def verify_otp():
    if 'registration_data' not in session:
        flash('Silakan registrasi terlebih dahulu.', 'error')
        return redirect(url_for('register'))
    
    if request.method == 'POST':
        otp_code = request.form.get('otp_code')
        registration_data = session['registration_data']
        email = registration_data['email']
        
        # Verify OTP
        is_valid, message = EmailService.verify_otp(email, otp_code)
        
        if is_valid:
            # Create user account
            new_user = User(
                username=registration_data['username'],
                email=registration_data['email'],
                full_name=registration_data['full_name'],
                phone=registration_data['phone'],
                is_verified=True
            )
            new_user.set_password(registration_data['password'])
            db.session.add(new_user)
            db.session.commit()
            
            # Clear session
            session.pop('registration_data', None)
            
            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'error')
            return redirect(url_for('verify_otp'))
    
    return render_template('verify_otp.html')

@app.route("/resend-otp", methods=['POST'])
def resend_otp():
    if 'registration_data' not in session:
        return jsonify({'success': False, 'message': 'Session expired'}), 400
    
    email = session['registration_data']['email']
    
    result = EmailService.send_otp_email(email)
    email_sent, otp_code = result
    
    if email_sent:
        message = 'OTP baru telah dikirim!'
        if otp_code:
            message = f'[DEV MODE] Kode OTP Anda: {otp_code}. ' + message
        return jsonify({'success': True, 'message': message})
    else:
        return jsonify({'success': False, 'message': 'Gagal mengirim OTP'}), 500

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
            if not user.is_verified and user.role != 'admin':
                flash('Email Anda belum diverifikasi. Silakan cek email Anda.', 'error')
                return redirect(url_for('login'))
            
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

# --- USER PROFILE ROUTES ---

@app.route("/profile")
@login_required
def profile():
    # Get user notifications
    if current_user.role == 'admin':
        notifications = []
    else:
        # Get personal notifications and global notifications
        personal_notifications = Notification.query.filter_by(user_id=current_user.id, is_global=False).all()
        global_notifications = Notification.query.filter_by(is_global=True).all()
        notifications = personal_notifications + global_notifications
        notifications = sorted(notifications, key=lambda x: x.created_at, reverse=True)
    
    return render_template('profile.html', notifications=notifications)

@app.route("/profile/edit", methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name')
        current_user.phone = request.form.get('phone')
        
        # Update email if changed
        new_email = request.form.get('email')
        if new_email != current_user.email:
            if User.query.filter_by(email=new_email).first():
                flash('Email sudah digunakan oleh pengguna lain!', 'error')
                return redirect(url_for('edit_profile'))
            current_user.email = new_email
            current_user.is_verified = False
            # Send new OTP
            result = EmailService.send_otp_email(new_email)
            email_sent, otp_code = result
            if otp_code:
                flash(f'[DEV MODE] Kode OTP Anda: {otp_code}', 'info')
            flash('Email diubah. Silakan verifikasi email baru Anda.', 'warning')
        
        # Update password if provided
        new_password = request.form.get('new_password')
        if new_password:
            confirm_password = request.form.get('confirm_password')
            if new_password == confirm_password:
                current_user.set_password(new_password)
            else:
                flash('Konfirmasi password tidak cocok!', 'error')
                return redirect(url_for('edit_profile'))
        
        db.session.commit()
        flash('Profile berhasil diperbarui!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('edit_profile.html')

@app.route("/profile/upload-image", methods=['POST'])
@login_required
def upload_profile_image():
    if 'profile_image' not in request.files:
        flash('Tidak ada file yang dipilih!', 'error')
        return redirect(url_for('edit_profile'))
    
    file = request.files['profile_image']
    
    if file.filename == '':
        flash('Tidak ada file yang dipilih!', 'error')
        return redirect(url_for('edit_profile'))
    
    if file and allowed_file(file.filename):
        # Delete old profile image if exists
        if current_user.profile_image:
            old_image_path = os.path.join(app.root_path, current_user.profile_image.replace('/', os.sep))
            if os.path.exists(old_image_path):
                os.remove(old_image_path)
        
        # Save new profile image
        filename = secure_filename(file.filename)
        # Add timestamp to make filename unique
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{current_user.id}_{timestamp}_{filename}"
        
        # Use forward slash for URL compatibility (stored in database)
        file_path = f"{app.config['PROFILE_UPLOAD_FOLDER']}/{filename}"
        
        # Use OS-specific path for saving file
        save_path = os.path.join(app.root_path, app.config['PROFILE_UPLOAD_FOLDER'], filename)
        file.save(save_path)
        
        # Update user profile image path (using forward slash for URL)
        current_user.profile_image = file_path
        db.session.commit()
        
        flash('Foto profil berhasil diupload!', 'success')
    else:
        flash('Format file tidak diizinkan! Gunakan PNG, JPG, JPEG, GIF, atau WebP.', 'error')
    
    return redirect(url_for('edit_profile'))

@app.route("/profile/delete-image", methods=['POST'])
@login_required
def delete_profile_image():
    if current_user.profile_image:
        # Delete the file - convert forward slash to OS-specific path
        image_path = os.path.join(app.root_path, current_user.profile_image.replace('/', os.sep))
        if os.path.exists(image_path):
            os.remove(image_path)
        
        # Clear the database field
        current_user.profile_image = None
        db.session.commit()
        
        flash('Foto profil berhasil dihapus!', 'success')
    else:
        flash('Tidak ada foto profil untuk dihapus.', 'warning')
    
    return redirect(url_for('edit_profile'))

@app.route("/notifications")
@login_required
def notifications():
    if current_user.role == 'admin':
        all_notifications = Notification.query.order_by(Notification.created_at.desc()).all()
        return render_template('notifications.html', notifications=all_notifications)
    else:
        # Get personal and global notifications
        personal_notifications = Notification.query.filter_by(user_id=current_user.id, is_global=False).all()
        global_notifications = Notification.query.filter_by(is_global=True).all()
        all_notifications = personal_notifications + global_notifications
        all_notifications = sorted(all_notifications, key=lambda x: x.created_at, reverse=True)
        return render_template('notifications.html', notifications=all_notifications)

@app.route("/notifications/mark-read/<int:id>", methods=['POST'])
@login_required
def mark_notification_read(id):
    notification = Notification.query.get_or_404(id)
    notification.is_read = True
    db.session.commit()
    return jsonify({'success': True})

# --- ADMIN NOTIFICATION ROUTES ---

@app.route("/admin/notifications/create", methods=['GET', 'POST'])
@admin_required
def create_notification():
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        is_global = request.form.get('is_global') == 'on'
        send_email = request.form.get('send_email') == 'on'
        
        # Create notification
        notification = Notification(
            title=title,
            message=message,
            notification_type='announcement',
            is_global=is_global
        )
        db.session.add(notification)
        db.session.commit()
        
        # Send email to all users if requested
        if send_email:
            users = User.query.filter_by(role='tenant', is_verified=True).all()
            for user in users:
                if user.email:
                    EmailService.send_notification_email(user.email, title, message)
        
        flash('Notifikasi berhasil dibuat dan dikirim!', 'success')
        return redirect(url_for('admin_notifications'))
    
    return render_template('admin/create_notification.html')

@app.route("/admin/notifications")
@admin_required
def admin_notifications():
    notifications = Notification.query.order_by(Notification.created_at.desc()).all()
    return render_template('admin/notifications.html', notifications=notifications)

@app.route("/admin/notifications/delete/<int:id>", methods=['POST'])
@admin_required
def delete_notification(id):
    notification = Notification.query.get_or_404(id)
    db.session.delete(notification)
    db.session.commit()
    flash('Notifikasi berhasil dihapus.', 'success')
    return redirect(url_for('admin_notifications'))

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

# --- API ROUTES ---

@app.route("/api/unread-notifications-count")
@login_required
def unread_notifications_count():
    if current_user.role == 'admin':
        return jsonify({'count': 0})
    
    # Get personal and global unread notifications
    personal_unread = Notification.query.filter_by(
        user_id=current_user.id, 
        is_global=False, 
        is_read=False
    ).count()
    
    global_unread = Notification.query.filter_by(
        is_global=True, 
        is_read=False
    ).count()
    
    total_unread = personal_unread + global_unread
    return jsonify({'count': total_unread})

if __name__ == "__main__":
    app.run(debug=True)

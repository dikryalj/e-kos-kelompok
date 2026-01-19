import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kunci-rahasia-sangat-aman-sekali-12345'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///ekost.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # ============================================================
    # EMAIL CONFIGURATION (SMTP)
    # ============================================================
    # Untuk Gmail:
    # 1. Aktifkan 2-Step Verification di akun Google Anda
    # 2. Buat App Password di: https://myaccount.google.com/apppasswords
    # 3. Gunakan App Password tersebut (16 karakter) sebagai SENDER_PASSWORD
    # 
    # Contoh environment variable:
    # set SENDER_EMAIL=namaemail@gmail.com
    # set SENDER_PASSWORD=xxxx xxxx xxxx xxxx
    # ============================================================
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    SENDER_EMAIL = os.environ.get('SENDER_EMAIL')  # Contoh: namaemail@gmail.com
    SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')  # App Password 16 karakter
    
    # Development Mode - jika True, OTP ditampilkan di flash message
    # Set MAIL_DEV_MODE=false untuk mode production dengan email sungguhan
    MAIL_DEV_MODE = os.environ.get('MAIL_DEV_MODE', 'true').lower() == 'true'
    
    # ============================================================
    # WHATSAPP CONFIGURATION
    # ============================================================
    # Format nomor: Kode negara + nomor telepon, TANPA tanda + atau spasi
    # Contoh Indonesia: 6281234567890 (62 = kode negara, 81234567890 = nomor)
    # 
    # PENTING: Ganti dengan nomor WhatsApp owner yang valid!
    # Contoh environment variable:
    # set WHATSAPP_NUMBER=6281234567890
    # ============================================================
    WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '6281217929833')

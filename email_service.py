import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from models import db, OTP
from flask import current_app

class EmailService:
    
    @staticmethod
    def generate_otp():
        """Generate 6-digit OTP code"""
        return ''.join(random.choices(string.digits, k=6))
    
    @staticmethod
    def send_email(to_email, subject, html_content):
        """Send email using SMTP"""
        try:
            # Get email configuration from app config
            smtp_server = current_app.config.get('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = current_app.config.get('SMTP_PORT', 587)
            sender_email = current_app.config.get('SENDER_EMAIL')
            sender_password = current_app.config.get('SENDER_PASSWORD')
            dev_mode = current_app.config.get('MAIL_DEV_MODE', True)
            
            # Jika dalam mode development dan tidak ada konfigurasi SMTP
            if not sender_email or not sender_password:
                if dev_mode:
                    print(f"[DEV MODE] Email would be sent to: {to_email}")
                    print(f"[DEV MODE] Subject: {subject}")
                    return True  # Return True dalam dev mode agar registrasi bisa lanjut
                else:
                    print("Email configuration not found. Please set SENDER_EMAIL and SENDER_PASSWORD.")
                    return False
            
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = f"E-Kost Griya Amalia <{sender_email}>"
            message['To'] = to_email
            
            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)
            
            print(f"Email successfully sent to: {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            # Dalam dev mode, tetap return True agar tidak block flow
            dev_mode = current_app.config.get('MAIL_DEV_MODE', True)
            if dev_mode:
                print(f"[DEV MODE] Returning True despite error for testing purposes")
                return True
            return False
    
    @staticmethod
    def send_otp_email(email):
        """Send OTP verification email
        
        Returns:
            tuple: (success: bool, otp_code: str or None)
        """
        # Generate OTP
        otp_code = EmailService.generate_otp()
        
        # Save OTP to database
        expires_at = datetime.utcnow() + timedelta(minutes=10)  # OTP valid for 10 minutes
        otp = OTP(email=email, otp_code=otp_code, expires_at=expires_at)
        db.session.add(otp)
        db.session.commit()
        
        # Check if in dev mode
        dev_mode = current_app.config.get('MAIL_DEV_MODE', True)
        
        # Email HTML template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; color: #2c3e50; margin-bottom: 30px; }}
                .otp-box {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; font-size: 32px; font-weight: bold; letter-spacing: 8px; margin: 20px 0; }}
                .info {{ color: #666; margin: 20px 0; line-height: 1.6; }}
                .footer {{ text-align: center; color: #999; margin-top: 30px; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="header">Verifikasi Email Anda</h1>
                <p class="info">Terima kasih telah mendaftar di <strong>E-Kost Griya Kost Amalia</strong>.</p>
                <p class="info">Gunakan kode OTP berikut untuk memverifikasi email Anda:</p>
                <div class="otp-box">{otp_code}</div>
                <p class="info">Kode OTP ini akan kadaluarsa dalam <strong>10 menit</strong>.</p>
                <p class="info">Jika Anda tidak melakukan pendaftaran, abaikan email ini.</p>
                <div class="footer">
                    <p>&copy; 2026 Griya Kost Amalia. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Send email
        subject = "Kode OTP Verifikasi Email - E-Kost Griya Amalia"
        email_sent = EmailService.send_email(email, subject, html_content)
        
        # Return tuple dengan OTP code untuk ditampilkan di dev mode
        return (email_sent, otp_code if dev_mode else None)
    
    @staticmethod
    def send_notification_email(email, title, message):
        """Send notification email to user"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px 8px 0 0; margin: -30px -30px 20px -30px; }}
                .content {{ color: #333; line-height: 1.8; margin: 20px 0; }}
                .footer {{ text-align: center; color: #999; margin-top: 30px; font-size: 12px; border-top: 1px solid #eee; padding-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2 style="margin:0;">{title}</h2>
                </div>
                <div class="content">
                    <p>{message}</p>
                </div>
                <div class="footer">
                    <p>&copy; 2026 Griya Kost Amalia. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return EmailService.send_email(email, title, html_content)
    
    @staticmethod
    def send_booking_confirmation_email(email, booking_data):
        """Send booking confirmation email"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
                .booking-info {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .info-row {{ display: flex; margin: 10px 0; padding: 10px 0; border-bottom: 1px solid #eee; }}
                .info-label {{ font-weight: bold; color: #666; width: 150px; }}
                .info-value {{ color: #333; }}
                .footer {{ text-align: center; color: #999; margin-top: 30px; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Booking Berhasil!</h1>
                </div>
                <p>Halo <strong>{booking_data.get('name')}</strong>,</p>
                <p>Terima kasih telah melakukan booking di Griya Kost Amalia. Berikut adalah detail booking Anda:</p>
                <div class="booking-info">
                    <div class="info-row">
                        <span class="info-label">Nama:</span>
                        <span class="info-value">{booking_data.get('name')}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Email:</span>
                        <span class="info-value">{booking_data.get('email')}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Telepon:</span>
                        <span class="info-value">{booking_data.get('phone')}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Tipe Kamar:</span>
                        <span class="info-value">{booking_data.get('room_type')}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Tanggal Check-in:</span>
                        <span class="info-value">{booking_data.get('checkin_date')}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Durasi:</span>
                        <span class="info-value">{booking_data.get('duration')} bulan</span>
                    </div>
                </div>
                <p>Kami akan segera menghubungi Anda untuk konfirmasi lebih lanjut.</p>
                <div class="footer">
                    <p>&copy; 2026 Griya Kost Amalia. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        subject = "Konfirmasi Booking - Griya Kost Amalia"
        return EmailService.send_email(email, subject, html_content)
    
    @staticmethod
    def verify_otp(email, otp_code):
        """Verify OTP code"""
        otp = OTP.query.filter_by(email=email, otp_code=otp_code, is_used=False).order_by(OTP.created_at.desc()).first()
        
        if not otp:
            return False, "Kode OTP tidak valid."
        
        if otp.expires_at < datetime.utcnow():
            return False, "Kode OTP sudah kadaluarsa."
        
        # Mark OTP as used
        otp.is_used = True
        db.session.commit()
        
        return True, "Verifikasi berhasil!"

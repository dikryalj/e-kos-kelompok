# 🚀 Quick Start Guide - E-Kost System

## ⚡ Instalasi Cepat

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy dan edit .env
copy .env.example .env
# Edit .env dengan konfigurasi email & WhatsApp Anda

# 3. Initialize database
flask init-db

# 4. Jalankan aplikasi
python app.py
```

Aplikasi berjalan di: **http://localhost:5000**

---

## 🔑 Login Admin Default

- **URL**: http://localhost:5000/login
- **Username**: `admin`
- **Password**: `admin123`

---

## ✨ Fitur yang Sudah Ada

### Untuk User:
1. ✅ **Registrasi dengan OTP Email** - User harus verifikasi email sebelum bisa booking
2. ✅ **Booking Kamar** - User bisa booking setelah punya akun terverifikasi
3. ✅ **Profile Management** - Edit nama, email, telepon, password
4. ✅ **Notifikasi** - Lihat notifikasi booking & pengumuman dari admin
5. ✅ **WhatsApp Integration** - Hubungi admin via WhatsApp setelah booking

### Untuk Admin:
1. ✅ **Inbox Booking** - Lihat semua booking request
2. ✅ **Buat Notifikasi** - Kirim pengumuman ke semua user
3. ✅ **Email Broadcast** - Kirim notifikasi via email
4. ✅ **Kelola Notifikasi** - Dashboard & manage notifikasi

---

## 📝 Konfigurasi Email (Penting!)

Edit file `.env`:

```env
# Untuk Gmail
SENDER_EMAIL=email-anda@gmail.com
SENDER_PASSWORD=app-password-anda

# WhatsApp (format: kode negara + nomor, tanpa +/-)
WHATSAPP_NUMBER=6281234567890
```

**Cara dapat App Password Gmail:**
1. Buka: https://myaccount.google.com/security
2. Aktifkan **2-Step Verification**
3. Buat **App Password**: https://myaccount.google.com/apppasswords
4. Copy App Password ke `.env`

---

## 🎯 Alur User

```
1. Register → 2. Cek Email OTP → 3. Verifikasi → 4. Login → 5. Booking → 6. WhatsApp
```

**Navbar User:**
- Klik nama/avatar → **Profile** | **Pengaturan** | **Notifikasi**

---

## 👨‍💼 Alur Admin

```
1. Login → 2. Lihat Booking (Inbox) → 3. Buat Notifikasi → 4. Kirim ke User
```

**Menu Admin:**
- **Inbox** - Lihat booking
- **Kelola Notifikasi** - Buat & manage notifikasi
- **Profile Dropdown** - Profile & Pengaturan

---

## 🔧 Troubleshooting Cepat

| Masalah | Solusi |
|---------|--------|
| Email OTP tidak terkirim | Cek `.env`, gunakan App Password Gmail |
| Badge notifikasi tidak muncul | Refresh halaman (F5) |
| WhatsApp tidak membuka | Cek format nomor di `.env` (contoh: 6281234567890) |
| Database error | Jalankan `flask init-db` |

---

## 📁 File Penting yang Dibuat/Diupdate

```
templates/
├── base.html (UPDATED - navbar dengan dropdown)
├── edit_profile.html (NEW)
├── notifications.html (NEW)
└── admin/
    ├── create_notification.html (NEW)
    └── notifications.html (NEW)

static/js/
└── script.js (UPDATED - dropdown & API)

app.py (UPDATED - routes & API)
config.py (UPDATED - WhatsApp config)
.env.example (UPDATED - WhatsApp number)
```

---

## 🎨 Preview Fitur

### Navbar dengan Dropdown
```
┌─────────────────────────────────────┐
│  [Logo] Griya Kost Amalia           │
│                [Avatar ▼]  (Click!)  │
│                └── Profile           │
│                └── Pengaturan        │
│                └── Notifikasi [3]    │
│                └── Logout            │
└─────────────────────────────────────┘
```

### Halaman Notifikasi
```
📢 Pengumuman: Pembayaran Kost
   Admin mengirim pengumuman...
   [Tandai sudah dibaca]

📋 Booking Berhasil!
   Booking Anda telah diterima...
   [Sudah dibaca]
```

---

## 🚀 Demo Flow

### 1. User Flow
```bash
# Buka browser
http://localhost:5000

# Klik "Login" → "Daftar"
# Isi form registrasi
# Cek email untuk OTP
# Input OTP → Akun aktif
# Login → Booking → WhatsApp
```

### 2. Admin Flow
```bash
# Login sebagai admin
http://localhost:5000/login
Username: admin
Password: admin123

# Lihat booking di Inbox
# Klik "Kelola Notifikasi"
# Buat notifikasi baru
# Centang "Kirim ke Semua Pengguna"
# Centang "Kirim via Email"
# Kirim → User terima notifikasi!
```

---

## ✅ Checklist Implementasi

Semua fitur yang diminta sudah diimplementasikan:

- [x] User harus punya akun untuk booking
- [x] Registrasi dengan email verification OTP
- [x] Email harus real (terkoneksi langsung)
- [x] Navbar dengan dropdown Profile
- [x] Menu Pengaturan dengan CRUD profile
- [x] Menu Notifikasi untuk user
- [x] Admin bisa buat notifikasi
- [x] Notifikasi muncul di akun user
- [x] Notifikasi terkirim ke email user
- [x] WhatsApp integration setelah booking

---

## 📚 Dokumentasi Lengkap

Untuk panduan lebih detail, baca:
- **PANDUAN_LENGKAP.md** - Panduan lengkap user & admin
- **IMPLEMENTASI_FITUR.md** - Detail teknis implementasi

---

**Aplikasi siap digunakan!** 🎉

Jika ada pertanyaan atau error, cek file `PANDUAN_LENGKAP.md` untuk troubleshooting lengkap.

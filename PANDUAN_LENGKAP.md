# 🎉 E-Kost System - Panduan Lengkap

## 📋 Daftar Isi
1. [Fitur yang Diimplementasikan](#fitur-yang-diimplementasikan)
2. [Persiapan Awal](#persiapan-awal)
3. [Panduan Penggunaan User](#panduan-penggunaan-user)
4. [Panduan Penggunaan Admin](#panduan-penggunaan-admin)
5. [FAQ & Troubleshooting](#faq--troubleshooting)

---

## ✨ Fitur yang Diimplementasikan

### Fitur Utama yang Diminta:

#### ✅ 1. User Account dengan Email Verification OTP
- User harus memiliki akun untuk melakukan booking
- Registrasi dengan verifikasi email menggunakan OTP
- OTP dikirim langsung ke email user (real email)
- Akun hanya aktif setelah verifikasi OTP berhasil

#### ✅ 2. Navbar dengan Dropdown Profile
- Dropdown menu modern di navbar
- Menu Profile menampilkan:
  - **Profile** - Lihat informasi lengkap
  - **Pengaturan** - Edit profile (CRUD)
  - **Notifikasi** - Lihat semua notifikasi
- Badge counter menampilkan jumlah notifikasi belum dibaca

#### ✅ 3. CRUD Profile Management
- **Create**: Registrasi akun baru dengan verifikasi
- **Read**: Lihat informasi profile lengkap
- **Update**: Edit nama, email, telepon, password
- **Delete**: (Opsional - bisa ditambahkan jika diperlukan)

#### ✅ 4. Sistem Notifikasi User
- Notifikasi booking otomatis setelah user booking
- Notifikasi pengumuman dari admin
- Badge counter notifikasi belum dibaca
- Mark as read functionality
- Icon berbeda untuk tiap tipe notifikasi

#### ✅ 5. Admin Notification Management
- Form untuk membuat notifikasi baru
- Opsi kirim ke semua user (broadcast)
- Opsi kirim via email ke user
- Dashboard statistik notifikasi
- Hapus notifikasi

#### ✅ 6. WhatsApp Integration
- Tombol "Hubungi via WhatsApp" setelah booking
- Data booking otomatis ter-format di chat WhatsApp
- Nomor WhatsApp dapat dikonfigurasi via .env

#### ✅ 7. Email Notifications
- Email konfirmasi booking
- Email OTP verifikasi
- Email notifikasi dari admin
- Template email yang modern

---

## 🚀 Persiapan Awal

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Konfigurasi Email & WhatsApp

Copy file `.env.example` menjadi `.env`:
```bash
copy .env.example .env
```

Edit file `.env` dengan konfigurasi Anda:

```env
# Email Configuration
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password

# SMTP Configuration (default untuk Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# WhatsApp Configuration
# Format: kode negara + nomor (tanpa tanda +, -, atau spasi)
WHATSAPP_NUMBER=6281234567890
```

**Untuk Gmail:**
1. Buka https://myaccount.google.com/security
2. Aktifkan **2-Step Verification**
3. Buat **App Password** di https://myaccount.google.com/apppasswords
4. Gunakan App Password sebagai `SENDER_PASSWORD`

### 3. Initialize Database

```bash
flask init-db
```

Ini akan membuat:
- Admin default dengan username: `admin`, password: `admin123`
- 12 kamar kost (6 Luar, 6 Dalam)

### 4. Jalankan Aplikasi

```bash
python app.py
```

Aplikasi akan berjalan di: **http://localhost:5000**

---

## 👤 Panduan Penggunaan User

### Step 1: Registrasi Akun

1. Kunjungi `/register` atau klik tombol "Login" di navbar
2. Isi form registrasi:
   - Username
   - Email (harus email real/aktif)
   - Nama Lengkap
   - Nomor Telepon
   - Password
3. Klik "Daftar"
4. Cek email Anda untuk kode OTP (cek inbox dan spam folder)
5. Masukkan kode OTP di halaman verifikasi
6. Akun aktif! Login dengan username dan password

### Step 2: Melakukan Booking

1. Login ke akun Anda
2. Klik menu "Booking" di navbar
3. Isi form booking dengan lengkap
4. Klik "Kirim Booking"
5. Anda akan mendapat:
   - Notifikasi di akun
   - Email konfirmasi booking
6. Klik tombol "Hubungi via WhatsApp" untuk konfirmasi ke admin

### Step 3: Mengakses Profile & Notifikasi

#### Cara 1: Melalui Dropdown Navbar
1. Klik nama/avatar Anda di navbar (pojok kanan atas)
2. Pilih menu:
   - **Profile**: Lihat informasi lengkap
   - **Pengaturan**: Edit profile Anda
   - **Notifikasi**: Lihat semua notifikasi

#### Cara 2: Langsung ke URL
- Profile: `/profile`
- Edit Profile: `/profile/edit`
- Notifikasi: `/notifications`

### Step 4: Edit Profile

1. Akses menu **Pengaturan** dari dropdown
2. Edit informasi yang ingin diubah:
   - Nama Lengkap
   - Email (akan perlu verifikasi ulang)
   - Nomor Telepon
   - Password (opsional)
3. Klik "Simpan Perubahan"

### Step 5: Cek Notifikasi

1. Akses menu **Notifikasi** dari dropdown
2. Lihat semua notifikasi:
   - **Notifikasi Booking**: Konfirmasi booking Anda
   - **Pengumuman**: Pengumuman dari admin
3. Klik "Tandai sudah dibaca" untuk notifikasi yang belum dibaca
4. Badge di navbar akan update otomatis

---

## 👨‍💼 Panduan Penggunaan Admin

### Login Admin

- URL: `/login`
- Username: `admin`
- Password: `admin123`

### Melihat Booking Masuk

1. Setelah login, Anda otomatis ke halaman Inbox
2. Atau klik menu "Inbox" di navbar
3. Lihat semua booking request dari user
4. Hapus booking yang sudah diproses

### Membuat & Mengirim Notifikasi

#### Step 1: Akses Menu Notifikasi
1. Klik "Kelola Notifikasi" di navbar
2. Atau langsung ke `/admin/notifications`

#### Step 2: Buat Notifikasi Baru
1. Klik tombol "Buat Notifikasi Baru"
2. Isi form:
   - **Judul**: Judul notifikasi (contoh: "Pembayaran Kost Bulan Januari")
   - **Pesan**: Isi pesan notifikasi
3. Pilih opsi:
   - ☑️ **Kirim ke Semua Pengguna**: Notifikasi diterima semua user
   - ☑️ **Kirim via Email**: Notifikasi juga dikirim ke email user
4. Klik "Kirim Notifikasi"

#### Step 3: Hasil
- Notifikasi muncul di halaman profile user
- Jika opsi email dicentang, email otomatis terkirim ke semua user
- Badge notifikasi di navbar user akan update

### Mengelola Notifikasi

1. Di halaman "Kelola Notifikasi", Anda bisa:
   - Lihat statistik notifikasi
   - Lihat list semua notifikasi yang pernah dikirim
   - Hapus notifikasi yang tidak relevan lagi

---

## 🎨 Fitur UI/UX

### Navbar
- Modern gradient design
- Sticky navbar (tetap di atas saat scroll)
- Dropdown menu yang smooth
- Badge counter notifikasi real-time

### Profile Page
- Card-based design
- Avatar dengan initial nama
- Badge verified untuk user terverifikasi
- Notifikasi terbaru di sidebar

### Notifications Page
- Icon berbeda untuk tiap tipe notifikasi:
  - 📋 **Booking** - Biru
  - 📢 **Announcement** - Ungu
  - ℹ️ **System** - Abu-abu
- Badge "Baru" untuk notifikasi belum dibaca
- Mark as read dengan satu klik
- Empty state yang informatif

### Admin Dashboard
- Statistik notifikasi lengkap
- Table view yang responsive
- Confirmation dialog sebelum hapus
- Form dengan preview

---

## 🔐 Keamanan & Best Practices

1. **Password Hashing**: Semua password di-hash dengan werkzeug
2. **Email Verification**: OTP valid selama 10 menit
3. **Login Required**: Booking hanya bisa dilakukan setelah login
4. **Admin Protection**: Route admin hanya bisa diakses admin
5. **CSRF Protection**: Built-in Flask protection
6. **SQL Injection Protection**: SQLAlchemy ORM

---

## 🐛 FAQ & Troubleshooting

### Email OTP tidak terkirim?

**Solusi:**
1. Pastikan konfigurasi email di `.env` sudah benar
2. Untuk Gmail, gunakan App Password (bukan password biasa)
3. Cek folder spam di email
4. Pastikan email yang dimasukkan valid

### Notifikasi tidak muncul?

**Solusi:**
1. Refresh halaman (F5)
2. Logout dan login lagi
3. Pastikan JavaScript enabled di browser

### WhatsApp tidak membuka chat?

**Solusi:**
1. Pastikan nomor WhatsApp di `.env` sudah benar
2. Format nomor: kode negara + nomor (contoh: 6281234567890)
3. Pastikan WhatsApp terinstall atau WhatsApp Web aktif

### Badge notifikasi tidak update?

**Solusi:**
1. Refresh halaman
2. Clear browser cache
3. Pastikan API `/api/unread-notifications-count` berjalan

### Database error setelah update?

**Solusi:**
```bash
# Re-initialize database
flask init-db
```
**⚠️ WARNING**: Ini akan menghapus semua data!

---

## 📞 Support

Jika mengalami masalah:
1. Baca dokumentasi ini dengan teliti
2. Cek log error di console
3. Pastikan semua dependencies terinstall
4. Pastikan konfigurasi `.env` sudah benar

---

## 🎉 Selamat!

Semua fitur yang diminta sudah diimplementasikan:
- ✅ User account dengan OTP verification
- ✅ Navbar dropdown profile
- ✅ CRUD Profile
- ✅ Sistem notifikasi user
- ✅ Admin notification management
- ✅ Email notifications
- ✅ WhatsApp integration

**Aplikasi siap digunakan!** 🚀

---

**Last Updated**: 19 Januari 2026

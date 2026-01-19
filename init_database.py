#!/usr/bin/env python
"""
Script untuk initialize database E-Kost
Menghapus database lama dan membuat yang baru dengan struktur terbaru
"""

from app import app, db
from models import User, Room

def init_database():
    with app.app_context():
        print("Menghapus database lama...")
        db.drop_all()
        
        print("Membuat tabel baru...")
        db.create_all()
        
        print("Membuat admin default...")
        admin = User(username='admin', role='admin', is_verified=True)
        admin.set_password('admin123')
        db.session.add(admin)
        
        print("Membuat data kamar kost...")
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
        print("\n[SUCCESS] Database berhasil diinisialisasi!")
        print("\n[INFO] Informasi Login Admin:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n[INFO] 12 Kamar kost telah dibuat (6 Luar, 6 Dalam)")
        print("\nAplikasi siap digunakan! Jalankan dengan: python app.py")

if __name__ == '__main__':
    init_database()

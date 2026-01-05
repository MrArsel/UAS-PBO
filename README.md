# UAS-PBO
UAS PBO Sistem Peminjaman.id

I KOMANG GEDE AGUNG KRISNA YUDA KURNIAWAN [2401010030]
I KOMANG GEDE AGUNG KRISNA YUDA KURNIAWAN [2401010030]
I KOMANG GEDE AGUNG KRISNA YUDA KURNIAWAN [2401010030]

# Sistem Peminjaman Barang

Project ini dibuat sebagai tugas perkuliahan untuk membangun sistem peminjaman barang sederhana
menggunakan framework Django. Sistem ini bertujuan untuk membantu proses pencatatan barang,
peminjaman, dan penyimpanan agar lebih terstruktur dan mudah digunakan.

## Deskripsi Singkat
Aplikasi ini memungkinkan pengguna untuk mengelola data barang, melakukan peminjaman,
mengembalikan barang, serta melihat data penyimpanan. Sistem dibuat berbasis web
dengan tampilan sederhana dan mudah dipahami.

## Fitur Utama
- Login dan logout pengguna
- Manajemen data barang (tambah, edit, hapus)
- Peminjaman barang
- Pengembalian barang
- Penyimpanan barang
- Tampilan antarmuka sederhana

## Teknologi yang Digunakan
- Python
- Django
- SQLite
- HTML
- CSS

## Cara Menjalankan Aplikasi
1. Pastikan Python sudah terinstall (disarankan Python 3.9 atau lebih baru)
2. Extract folder project, lalu masuk ke direktori yang terdapat file `manage.py`
   
```bash
cd peminjaman_project
```

3. Buat dan aktifkan virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

4. Install dependency

```bash
pip install -r requirements.txt
```

5. Jalankan migrate database

```bash
python manage.py migrate
```

6. Jalankan server

```bash
python manage.py runserver
```

7. Buka browser dan akses:

```bash
http://127.0.0.1:8000/
```

## Struktur Folder
- peminjaman/ : aplikasi utama
- peminjaman_project/ : konfigurasi project
- templates/ : file tampilan HTML
- static/ : file CSS dan asset pendukung
- db.sqlite3 : database
- manage.py : file utama untuk menjalankan project

## Tujuan Pembuatan

Project ini dibuat untuk memenuhi tugas mata kuliah serta sebagai latihan
dalam memahami konsep dasar pengembangan web menggunakan Django.

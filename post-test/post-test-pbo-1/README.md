# 📌 Sistem Manajemen Toko Baju (OOP Python)

Program ini adalah simulasi sistem manajemen toko baju sederhana yang dibangun menggunakan konsep **Object-Oriented Programming (OOP)** di Python. Program mencakup pengelolaan produk, admin, pembeli, dan transaksi dalam satu sistem terintegrasi.

## 🎯 Tujuan Program
Mendemonstrasikan penerapan konsep-konsep OOP secara menyeluruh, meliputi:
- Class abstrak (Abstract Class) & Inheritance
- Encapsulation (Property, Getter, Setter, Private Attribute)
- Class Method & Static Method
- Class Attribute (atribut yang dimiliki bersama oleh seluruh objek)
- Validasi data pada setiap input

## 🗂️ Struktur Class

### 1. `Produk` (Abstract Class)
Class dasar/abstrak untuk semua jenis produk di toko.
- **Atribut instance:** `nama`, `brand`, `jenis`, `harga`, `stok`
- **Atribut class:** `nama_toko`, `total_produk`, `diskon_default`
- **Property:** `harga` dan `stok` memiliki getter/setter dengan validasi (tidak boleh negatif/tipe salah)
- **Method abstrak:** `info()` — wajib diimplementasikan oleh subclass
- **Method lain:** `ubahData()` untuk update data produk
- **Class Method:** `ubah_diskon_default()`, `get_total_produk()`
- **Static Method:** `format_rupiah()` — memformat angka jadi format Rupiah

**Subclass dari `Produk`:**
- `Baju`
- `Celana`
- `Aksesoris`

Masing-masing subclass mengimplementasikan method `info()` sesuai jenis produknya.

### 2. `Admin`
Mengelola data admin/pengelola toko.
- **Encapsulation:** `password` disimpan privat (`__password`), getter mengembalikan bentuk tersamar (`****`)
- **Setter:** validasi panjang password minimal 4 karakter
- **Method:** `login()` untuk autentikasi
- **Class Method:** `dari_dict()` — membuat objek Admin dari dictionary
- **Static Method:** `validasi_username()` — cek validitas format username

### 3. `Toko`
Mengelola operasi CRUD (Create, Read, Update, Delete) produk dalam toko.
- **Method:** `tambahProduk()`, `getAllProduk()`, `cariProduk()`, `updateProduk()`, `hapusProduk()`
- **Class Method:** `tambah_transaksi()` — menghitung total transaksi toko
- **Static Method:** `validasi_kategori()` — cek apakah kategori produk valid

### 4. `Pembeli`
Mengelola aktivitas belanja pembeli.
- **Encapsulation:** `__keranjang` (keranjang belanja) bersifat privat, diakses lewat property `keranjang`
- **Method:** `tambahKeranjang()`, `hapusKeranjang()`, `checkout()`
- **Class Method:** `ubah_diskon_member()` — mengatur diskon member
- **Static Method:** `hitung_diskon()` — menghitung nilai diskon

### 5. `Transaksi`
Mencatat detail transaksi hasil checkout pembeli.
- **Atribut:** `kode` (kode transaksi otomatis), `pembeli`, `total`
- **Method:** `hitungTotal()`, `cetakStruk()` — mencetak struk belanja
- **Class Method:** `atur_ppn()` — mengatur persentase PPN
- **Static Method:** `buat_kode_transaksi()` — membuat format kode transaksi (`TRX-0001`, dst.)

## ⚙️ Alur Program (Bagian `main`)
1. **Demo Admin** — membuat 2 admin, login (berhasil & gagal), uji ganti password valid/invalid, cek validasi username.
2. **Demo Toko & Produk** — membuat 2 toko, menambahkan produk (Baju, Celana, Aksesoris), menampilkan daftar produk, update & hapus produk, uji validasi harga/stok invalid.
3. **Demo Pembeli & Transaksi** — 2 pembeli berbelanja, menambahkan ke keranjang, uji validasi stok tidak cukup, proses checkout, cetak struk, ubah diskon member & PPN.
4. **Ringkasan Statistik** — menampilkan total admin, produk, pembeli, dan transaksi yang tercatat di sistem.

## ▶️ Cara Menjalankan
```bash
python 2509106014-BintangDhanaPermadi-PT-1.py
```
Program akan langsung menjalankan seluruh skenario demo di atas dan menampilkan hasilnya di terminal/console.

## ✅ Fitur Validasi
- Harga & stok produk tidak boleh negatif/salah tipe
- Password admin minimal 4 karakter
- Jumlah beli tidak boleh melebihi stok tersedia atau ≤ 0
- Diskon & PPN dibatasi pada rentang persentase yang wajar (0–100%, 0–50%, 0–30%)

## 📊 Konsep OOP yang Diterapkan
| Konsep | Contoh Penerapan |
|---|---|
| Abstraction | Class `Produk` bersifat abstrak dengan method `info()` |
| Inheritance | `Baju`, `Celana`, `Aksesoris` mewarisi `Produk` |
| Encapsulation | Atribut `__harga`, `__stok`, `__password`, `__keranjang` bersifat privat |
| Property (Getter/Setter) | `harga`, `stok`, `password`, `keranjang` |
| Class Method | `ubah_diskon_default()`, `dari_dict()`, `atur_ppn()`, dll |
| Static Method | `format_rupiah()`, `validasi_username()`, `hitung_diskon()`, dll |
| Class Attribute | `total_produk`, `total_admin`, `total_pembeli`, `total_transaksi` |
from abc import ABC, abstractmethod


class Produk(ABC):
    """
    Class abstrak yang menjadi cetakan dasar untuk semua jenis produk.
    """

    nama_toko = "Toko Baju Brand"
    total_produk = 0
    diskon_default = 10

    def __init__(self, nama, brand, jenis, harga, stok):
        self.nama = nama
        self.brand = brand
        self.jenis = jenis

        self.harga = harga
        self.stok = stok

        Produk.total_produk += 1

    @property
    def harga(self):
        return self.__harga

    @harga.setter
    def harga(self, harga_baru):
        if not isinstance(harga_baru, (int, float)) or harga_baru < 0:
            print(f"[GAGAL VALIDASI] Harga '{harga_baru}' tidak valid. Harga tidak boleh negatif.")
            if not hasattr(self, "_Produk__harga"):
                self.__harga = 0
        else:
            self.__harga = harga_baru

    @property
    def stok(self):
        return self.__stok

    @stok.setter
    def stok(self, stok_baru):
        if not isinstance(stok_baru, int) or stok_baru < 0:
            print(f"[GAGAL VALIDASI] Stok '{stok_baru}' tidak valid. Stok harus berupa angka non-negatif.")
            if not hasattr(self, "_Produk__stok"):
                self.__stok = 0
        else:
            self.__stok = stok_baru

    @abstractmethod
    def info(self):
        pass

    def ubahData(self, nama_baru=None, brand_baru=None, jenis_baru=None,
                harga_baru=None, stok_baru=None):
        if nama_baru:
            self.nama = nama_baru
        if brand_baru:
            self.brand = brand_baru
        if jenis_baru:
            self.jenis = jenis_baru
        if harga_baru is not None:
            self.harga = harga_baru
        if stok_baru is not None:
            self.stok = stok_baru
        print(f"[INFO] Data produk '{self.nama}' berhasil diperbarui.")

    @classmethod
    def ubah_diskon_default(cls, diskon_baru):
        if 0 <= diskon_baru <= 100:
            cls.diskon_default = diskon_baru
            print(f"[INFO] Diskon default toko diubah menjadi {diskon_baru}%.")
        else:
            print("[GAGAL VALIDASI] Nilai diskon harus di antara 0-100.")

    @classmethod
    def get_total_produk(cls):
        return cls.total_produk

    @staticmethod
    def format_rupiah(angka):
        return f"Rp{angka:,.0f}".replace(",", ".")


class Baju(Produk):
    def info(self):
        return (f"[BAJU] {self.nama} | Brand: {self.brand} | "
                f"Harga: {self.format_rupiah(self.harga)} | Stok: {self.stok}")


class Celana(Produk):
    def info(self):
        return (f"[CELANA] {self.nama} | Brand: {self.brand} | "
                f"Harga: {self.format_rupiah(self.harga)} | Stok: {self.stok}")


class Aksesoris(Produk):
    def info(self):
        return (f"[AKSESORIS] {self.nama} | Brand: {self.brand} | "
                f"Harga: {self.format_rupiah(self.harga)} | Stok: {self.stok}")


class Admin:
    total_admin = 0
    panjang_password_min = 4
    role_default = "admin"

    def __init__(self, username, password, role=None):
        self.username = username
        self.__password = None
        self.password = password
        self.role = role if role else Admin.role_default
        Admin.total_admin += 1

    @property
    def password(self):
        return "*" * len(self.__password) if self.__password else ""

    @password.setter
    def password(self, password_baru):
        if not password_baru or len(str(password_baru)) < Admin.panjang_password_min:
            print(f"[GAGAL VALIDASI] Password minimal {Admin.panjang_password_min} karakter.")
            if self.__password is None:
                self.__password = "0000"
        else:
            self.__password = str(password_baru)

    def login(self, username_input, password_input):
        if self.username == username_input and self.__password == password_input:
            print(f"[LOGIN BERHASIL] Selamat datang, {self.username} ({self.role})!")
            return True
        print(f"[LOGIN GAGAL] Username atau password untuk '{username_input}' salah.")
        return False

    @classmethod
    def dari_dict(cls, data):
        return cls(data["username"], data["password"], data.get("role"))

    @staticmethod
    def validasi_username(username):
        return bool(username) and " " not in username


class Toko:
    nama_instansi = "Toko Baju Brand"
    total_transaksi = 0
    kategori_tersedia = ["Baju", "Celana", "Aksesoris"]

    def __init__(self, nama_toko):
        self.nama_toko = nama_toko
        self.__daftar_produk = []

    def tambahProduk(self, produk):
        if not isinstance(produk, Produk):
            print("[GAGAL] Objek yang ditambahkan bukan Produk.")
            return
        self.__daftar_produk.append(produk)
        print(f"[INFO] Produk '{produk.nama}' berhasil ditambahkan ke {self.nama_toko}.")

    def getAllProduk(self):
        if not self.__daftar_produk:
            print(f"[INFO] Belum ada produk di {self.nama_toko}.")
            return
        print(f"\n=== DAFTAR PRODUK {self.nama_toko.upper()} ===")
        for p in self.__daftar_produk:
            print(p.info())

    def cariProduk(self, namaProduk):
        for p in self.__daftar_produk:
            if p.nama.lower() == namaProduk.lower():
                return p
        print(f"[INFO] Produk '{namaProduk}' tidak ditemukan di {self.nama_toko}.")
        return None

    def updateProduk(self, namaProduk, namaBaru=None, brandBaru=None,
                    jenisBaru=None, hargaBaru=None, stokBaru=None):
        produk = self.cariProduk(namaProduk)
        if produk:
            produk.ubahData(namaBaru, brandBaru, jenisBaru, hargaBaru, stokBaru)
        return produk

    def hapusProduk(self, namaProduk):
        produk = self.cariProduk(namaProduk)
        if produk:
            self.__daftar_produk.remove(produk)
            print(f"[INFO] Produk '{namaProduk}' berhasil dihapus dari {self.nama_toko}.")
            return True
        return False

    @classmethod
    def tambah_transaksi(cls):
        cls.total_transaksi += 1

    @staticmethod
    def validasi_kategori(jenis):
        return jenis in Toko.kategori_tersedia


class Pembeli:
    total_pembeli = 0
    diskon_member = 5
    level_default = "Reguler"

    def __init__(self, nama):
        self.nama = nama
        self.__keranjang = []
        Pembeli.total_pembeli += 1

    @property
    def keranjang(self):
        return list(self.__keranjang)

    def tambahKeranjang(self, produk, jumlah=1):
        if not isinstance(produk, Produk):
            print("[GAGAL] Item bukan produk yang valid.")
            return
        if jumlah <= 0:
            print("[GAGAL VALIDASI] Jumlah pembelian harus lebih dari 0.")
            return
        if jumlah > produk.stok:
            print(f"[GAGAL VALIDASI] Stok '{produk.nama}' tidak mencukupi (sisa {produk.stok}).")
            return
        self.__keranjang.append((produk, jumlah))
        print(f"[INFO] {produk.nama} x{jumlah} ditambahkan ke keranjang {self.nama}.")

    def hapusKeranjang(self, namaProduk):
        for item in self.__keranjang:
            if item[0].nama.lower() == namaProduk.lower():
                self.__keranjang.remove(item)
                print(f"[INFO] '{namaProduk}' dihapus dari keranjang {self.nama}.")
                return
        print(f"[INFO] '{namaProduk}' tidak ada di keranjang.")

    def checkout(self):
        if not self.__keranjang:
            print(f"[INFO] Keranjang {self.nama} kosong, checkout dibatalkan.")
            return None
        transaksi = Transaksi(self, self.__keranjang)
        for produk, jumlah in self.__keranjang:
            produk.stok -= jumlah
        self.__keranjang = []
        Toko.tambah_transaksi()
        return transaksi

    @classmethod
    def ubah_diskon_member(cls, persen_baru):
        if 0 <= persen_baru <= 50:
            cls.diskon_member = persen_baru
            print(f"[INFO] Diskon member diubah menjadi {persen_baru}%.")
        else:
            print("[GAGAL VALIDASI] Diskon member harus antara 0-50%.")

    @staticmethod
    def hitung_diskon(total, persen):
        return total * persen / 100


class Transaksi:
    kode_counter = 0
    ppn_persen = 0
    status_default = "Lunas"

    def __init__(self, pembeli, daftar_item):
        Transaksi.kode_counter += 1
        self.kode = Transaksi.buat_kode_transaksi(Transaksi.kode_counter)
        self.pembeli = pembeli.nama
        self.__daftar_item = list(daftar_item)
        self.__total = self.hitungTotal()

    @property
    def total(self):
        return self.__total

    def hitungTotal(self):
        total = sum(produk.harga * jumlah for produk, jumlah in self.__daftar_item)
        diskon = Pembeli.hitung_diskon(total, Pembeli.diskon_member)
        self.__total = total - diskon
        return self.__total

    def cetakStruk(self):
        print("\n" + "=" * 40)
        print(f"STRUK BELANJA - {Toko.nama_instansi}")
        print(f"Kode Transaksi : {self.kode}")
        print(f"Pembeli        : {self.pembeli}")
        print("-" * 40)
        for produk, jumlah in self.__daftar_item:
            subtotal = produk.harga * jumlah
            print(f"{produk.nama} x{jumlah} = {Produk.format_rupiah(subtotal)}")
        print("-" * 40)
        print(f"Diskon member ({Pembeli.diskon_member}%) diterapkan")
        print(f"Total Bayar    : {Produk.format_rupiah(self.__total)}")
        print("Terima kasih telah berbelanja!")
        print("=" * 40 + "\n")

    @classmethod
    def atur_ppn(cls, persen_baru):
        if 0 <= persen_baru <= 30:
            cls.ppn_persen = persen_baru
            print(f"[INFO] PPN diatur ke {persen_baru}%.")
        else:
            print("[GAGAL VALIDASI] PPN harus di antara 0-30%.")

    @staticmethod
    def buat_kode_transaksi(counter):
        return f"TRX-{counter:04d}"


if __name__ == "__main__":

    print("\n" + "="*50)
    print(" DEMO PEMBUKTIAN KETENTUAN POSTTEST PBO ".center(50, "="))
    print("="*50 + "\n")

    print(">>> 1. DEMO CLASS ADMIN (Minimal 2 Objek & Method) <<<")
    admin1 = Admin("admin_utama", "rahasia123", "Super Admin")
    admin2 = Admin.dari_dict({"username": "admin_kasir", "password": "password456", "role": "Kasir"})

    admin1.login("admin_utama", "rahasia123")
    admin2.login("admin_kasir", "salah_pass")

    print(f"Password admin1 (Property Getter): {admin1.password}")
    print("[UJI SETTER VALID] Mengubah password admin1 ke 'baru2026'...")
    admin1.password = "baru2026"
    print(f"Password admin1 setelah diubah: {admin1.password}")

    print("[UJI SETTER INVALID] Mengubah password admin1 ke '123' (kurang dari 4 karakter)...")
    admin1.password = "123"

    is_valid = Admin.validasi_username("admin_kasir")
    print(f"Hasil Static Method Admin.validasi_username('admin_kasir'): {is_valid}\n")


    print(">>> 2. DEMO CLASS TOKO & PRODUK (Minimal 2 Objek Per Class & CRUD) <<<")
    toko1 = Toko("Toko Baju Brand - Balikpapan")
    toko2 = Toko("Toko Baju Brand - Samarinda")

    baju1 = Baju("Kaos Lacoste", "Lacoste", "Baju", 250000, 10)
    baju2 = Baju("Jaket H&M", "H&M", "Baju", 550000, 5)

    celana1 = Celana("Celana Rucas", "Rucas", "Celana", 400000, 8)
    celana2 = Celana("Jeans Levi's", "Levi's", "Celana", 750000, 12)

    aksesoris1 = Aksesoris("Topi Nike", "Nike", "Aksesoris", 150000, 20)
    aksesoris2 = Aksesoris("Kacamata Rayban", "Rayban", "Aksesoris", 300000, 15)

    toko1.tambahProduk(baju1)
    toko1.tambahProduk(baju2)
    toko1.tambahProduk(celana1)
    toko1.tambahProduk(aksesoris1)

    toko2.tambahProduk(celana2)
    toko2.tambahProduk(aksesoris2)

    toko1.getAllProduk()

    print("\n[UJI SETTER VALID] Mengubah harga Kaos Lacoste menjadi 270000...")
    baju1.harga = 270000  # Valid
    print(f"Harga baru Kaos Lacoste: {Produk.format_rupiah(baju1.harga)}")

    print("[UJI SETTER INVALID] Mengubah stok Kaos Lacoste menjadi -10...")
    baju1.stok = -10

    toko1.updateProduk("Jaket H&M", hargaBaru=500000, stokBaru=10)
    toko1.hapusProduk("Celana Rucas")

    Produk.ubah_diskon_default(15)
    print(f"Total produk dibuat (Class Method): {Produk.get_total_produk()}")
    print(f"Validasi Kategori 'Baju' (Static Method): {Toko.validasi_kategori('Baju')}\n")

    print(">>> 3. DEMO CLASS PEMBELI & TRANSAKSI (Minimal 2 Objek Per Class) <<<")
    pembeli1 = Pembeli("Udin")
    pembeli2 = Pembeli("Sari")

    print("\n--- Udin Belanja ---")
    pembeli1.tambahKeranjang(baju1, 2)
    pembeli1.tambahKeranjang(aksesoris1, 1)

    print("\n--- Sari Belanja ---")
    pembeli2.tambahKeranjang(aksesoris2, 1)
    pembeli2.tambahKeranjang(celana2, 1)

    print("\n[UJI VALIDASI] Udin mencoba membeli Jaket H&M sebanyak 100 pcs...")
    pembeli1.tambahKeranjang(baju2, 100)

    trx1 = pembeli1.checkout()
    trx2 = pembeli2.checkout()

    if trx1:
        trx1.cetakStruk()
    if trx2:
        trx2.cetakStruk()

    Pembeli.ubah_diskon_member(10)
    Transaksi.atur_ppn(11)

    total_dummy = Pembeli.hitung_diskon(100000, Pembeli.diskon_member)
    print(f"Perhitungan Diskon Dummy (Static Method): {total_dummy}")
    print(f"Format Kode Transaksi (Static Method): {Transaksi.buat_kode_transaksi(99)}")

    print("\n" + "="*50)
    print("SUMMARY STATISTIK SISTEM:")
    print(f"- Total Admin Terdaftar    : {Admin.total_admin}")
    print(f"- Total Produk Terdaftar   : {Produk.total_produk}")
    print(f"- Total Pembeli Terdaftar  : {Pembeli.total_pembeli}")
    print(f"- Total Transaksi Berhasil : {Toko.total_transaksi}")
    print("="*50)
    print("\n########## SELURUH PENGUJIAN SELESAI ##########\n")
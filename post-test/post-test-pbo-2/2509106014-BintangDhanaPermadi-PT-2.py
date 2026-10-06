import gc
import weakref
from abc import ABC, abstractmethod


class Produk(ABC):
    """
    Superclass (Parent Class) untuk semua jenis produk.

    Tingkat akses:
    - Protected (_harga, _stok)  : boleh diakses/dimanipulasi langsung oleh subclass
    - Private   (__harga_modal)  : rahasia toko, HANYA bisa diakses oleh Produk
    """

    nama_toko = "Toko Baju Brand"
    total_produk = 0
    diskon_default = 10

    def __init__(self, nama, brand, jenis, harga, stok, harga_modal=0):
        self.nama = nama
        self.brand = brand
        self.jenis = jenis

        self.harga = harga
        self.stok = stok
        self.__harga_modal = harga_modal

        Produk.total_produk += 1

    @property
    def harga(self):
        return self._harga

    @harga.setter
    def harga(self, harga_baru):
        if not isinstance(harga_baru, (int, float)) or harga_baru < 0:
            print(f"[GAGAL VALIDASI] Harga '{harga_baru}' tidak valid. Harga tidak boleh negatif.")
            if not hasattr(self, "_harga"):
                self._harga = 0
        else:
            self._harga = harga_baru

    @property
    def stok(self):
        return self._stok

    @stok.setter
    def stok(self, stok_baru):
        if not isinstance(stok_baru, int) or stok_baru < 0:
            print(f"[GAGAL VALIDASI] Stok '{stok_baru}' tidak valid. Stok harus berupa angka non-negatif.")
            if not hasattr(self, "_stok"):
                self._stok = 0
        else:
            self._stok = stok_baru

    def hitung_keuntungan(self):
        """Keuntungan per unit. Harga modal bersifat rahasia (private)."""
        return self._harga - self.__harga_modal

    @abstractmethod
    def info(self):
        """Info dasar produk. Subclass wajib override dan boleh memanggil super().info()."""
        return (f"{self.nama} | Brand: {self.brand} | "
                f"Harga: {self.format_rupiah(self._harga)} | Stok: {self._stok}")

    def hitung_harga_akhir(self):
        """Harga jual akhir. Di superclass = harga normal (tanpa diskon)."""
        return self._harga

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
    """Subclass Produk. Atribut unik: ukuran, bahan."""

    def __init__(self, nama, brand, harga, stok, harga_modal, ukuran, bahan):
        super().__init__(nama, brand, "Baju", harga, stok, harga_modal)
        self.ukuran = ukuran
        self.bahan = bahan

    def hitung_harga_akhir(self):
        potongan = self._harga * Produk.diskon_default / 100
        return self._harga - potongan

    def info(self):
        return (f"[BAJU] {super().info()} | Ukuran: {self.ukuran} | Bahan: {self.bahan} | "
                f"Harga Akhir (diskon {Produk.diskon_default}%): "
                f"{self.format_rupiah(self.hitung_harga_akhir())}")


class Celana(Produk):
    """Subclass Produk. Atribut unik: ukuran_pinggang, model_potongan."""

    def __init__(self, nama, brand, harga, stok, harga_modal, ukuran_pinggang, model_potongan):
        super().__init__(nama, brand, "Celana", harga, stok, harga_modal)
        self.ukuran_pinggang = ukuran_pinggang
        self.model_potongan = model_potongan

    def perlu_restock(self):
        """Method khusus Celana: memakai atribut protected _stok milik superclass."""
        return self._stok < 5

    def info(self):
        status = "PERLU RESTOCK" if self.perlu_restock() else "Stok aman"
        return (f"[CELANA] {super().info()} | Pinggang: {self.ukuran_pinggang} | "
                f"Potongan: {self.model_potongan} | {status}")


class Aksesoris(Produk):
    """Subclass Produk. Atribut unik: material, garansi_bulan."""

    biaya_kemasan_hadiah = 5000

    def __init__(self, nama, brand, harga, stok, harga_modal, material, garansi_bulan=0):
        super().__init__(nama, brand, "Aksesoris", harga, stok, harga_modal)
        self.material = material
        self.garansi_bulan = garansi_bulan

    def hitung_harga_akhir(self):
        return self._harga + Aksesoris.biaya_kemasan_hadiah

    def info(self):
        return (f"[AKSESORIS] {super().info()} | Material: {self.material} | "
                f"Garansi: {self.garansi_bulan} bulan")


class Admin:
    total_admin = 0
    panjang_password_min = 4
    role_default = "admin"

    def __init__(self, username, password, role=None):
        self.username = username
        self.__password = None
        self.password = password
        self.role = role if role else Admin.role_default
        self._login_status = False
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
            self._login_status = True
            print(f"[LOGIN BERHASIL] Selamat datang, {self.username} ({self.role})!")
            return True
        print(f"[LOGIN GAGAL] Username atau password untuk '{username_input}' salah.")
        return False

    def tambah_produk_ke_toko(self, toko, produk):
        if not self._login_status:
            print(f"[AKSES DITOLAK] {self.username} harus login dulu.")
            return False
        print(f"[ADMIN {self.username}] Mengelola {toko.nama_toko}...")
        toko.tambahProduk(produk)
        return True

    def hapus_produk_dari_toko(self, toko, nama_produk):
        if not self._login_status:
            print(f"[AKSES DITOLAK] {self.username} harus login dulu.")
            return False
        print(f"[ADMIN {self.username}] Mengelola {toko.nama_toko}...")
        return toko.hapusProduk(nama_produk)

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

    def belanja_di(self, toko, namaProduk, jumlah=1):
        print(f"[INFO] {self.nama} mencari '{namaProduk}' di {toko.nama_toko}...")
        produk = toko.cariProduk(namaProduk)
        if produk:
            self.tambahKeranjang(produk, jumlah)

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


class ItemTransaksi:
    """
    Tidak punya arti tanpa Transaksi. Objek ini dibuat di dalam Transaksi
    dan ikut musnah bersama Transaksi (komposisi).
    """

    def __init__(self, nama_produk, harga_satuan, jumlah):
        self.nama_produk = nama_produk
        self.harga_satuan = harga_satuan
        self.jumlah = jumlah

    @property
    def subtotal(self):
        return self.harga_satuan * self.jumlah

    def __str__(self):
        return (f"{self.nama_produk} x{self.jumlah} @ "
                f"{Produk.format_rupiah(self.harga_satuan)} = {Produk.format_rupiah(self.subtotal)}")


class Transaksi:
    kode_counter = 0
    ppn_persen = 0
    status_default = "Lunas"

    def __init__(self, pembeli, daftar_item):
        Transaksi.kode_counter += 1
        self.kode = Transaksi.buat_kode_transaksi(Transaksi.kode_counter)
        self.pembeli = pembeli.nama
        self.__daftar_item = [
            ItemTransaksi(produk.nama, produk.hitung_harga_akhir(), jumlah)
            for produk, jumlah in daftar_item
        ]
        self.__total = self.hitungTotal()

    @property
    def total(self):
        return self.__total

    @property
    def daftar_item(self):
        return tuple(self.__daftar_item)

    def hitungTotal(self):
        total = sum(item.subtotal for item in self.__daftar_item)
        diskon = Pembeli.hitung_diskon(total, Pembeli.diskon_member)
        self.__total = total - diskon
        return self.__total

    def cetakStruk(self):
        print("\n" + "=" * 40)
        print(f"STRUK BELANJA - {Toko.nama_instansi}")
        print(f"Kode Transaksi : {self.kode}")
        print(f"Pembeli        : {self.pembeli}")
        print("-" * 40)
        for item in self.__daftar_item:
            print(item)
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

    print("\n" + "=" * 60)
    print(" DEMO POSTTEST 2 PBO: RELASI UML & INHERITANCE ".center(60, "="))
    print("=" * 60 + "\n")

    # ------------------------------------------------------------
    print(">>> 1. CLASS ADMIN (lanjutan Posttest 1) <<<")
    admin1 = Admin("admin_utama", "rahasia123", "Super Admin")
    admin2 = Admin.dari_dict({"username": "admin_kasir", "password": "password456", "role": "Kasir"})
    admin2.login("admin_kasir", "salah_pass")
    print(f"Password admin1 (Property Getter): {admin1.password}")
    admin1.password = "123"
    print(f"Validasi username 'admin_kasir': {Admin.validasi_username('admin_kasir')}\n")

    print(">>> 2. INHERITANCE: Superclass Produk -> Baju, Celana, Aksesoris <<<")
    baju1 = Baju("Kaos Lacoste", "Lacoste", 250000, 10, 150000, "L", "Katun")
    baju2 = Baju("Jaket H&M", "H&M", 550000, 5, 350000, "XL", "Fleece")
    celana1 = Celana("Celana Rucas", "Rucas", 400000, 8, 250000, 32, "Slim Fit")
    celana2 = Celana("Jeans Levi's", "Levi's", 750000, 3, 500000, 30, "Regular")
    aksesoris1 = Aksesoris("Topi Nike", "Nike", 150000, 20, 80000, "Polyester", 3)
    aksesoris2 = Aksesoris("Kacamata Rayban", "Rayban", 300000, 15, 180000, "Plastik Polarized", 12)

    print("\n[POLYMORPHISM + METHOD OVERRIDING] info() tiap subclass berbeda:")
    for p in (baju1, baju2, celana1, celana2, aksesoris1, aksesoris2):
        print(" ", p.info())

    print("\n[METHOD OVERRIDING] hitung_harga_akhir() berbeda per subclass:")
    print(f"  Baju      : {Produk.format_rupiah(baju1._harga)} -> {Produk.format_rupiah(baju1.hitung_harga_akhir())} (diskon default)")
    print(f"  Celana    : {Produk.format_rupiah(celana1._harga)} -> {Produk.format_rupiah(celana1.hitung_harga_akhir())} (versi superclass)")
    print(f"  Aksesoris : {Produk.format_rupiah(aksesoris1._harga)} -> {Produk.format_rupiah(aksesoris1.hitung_harga_akhir())} (+ biaya kemasan)")

    print("\n[ATRIBUT PROTECTED] subclass memakai _stok milik superclass:")
    print(f"  {celana2.nama} perlu restock? {celana2.perlu_restock()} (stok = {celana2.stok})")

    print("\n[ATRIBUT PRIVATE] __harga_modal hanya bisa dipakai di dalam Produk:")
    try:
        print(baju1.__harga_modal)
    except AttributeError as e:
        print(f"  Akses langsung gagal -> AttributeError: {e}")
    print(f"  Lewat method superclass hitung_keuntungan(): {Produk.format_rupiah(baju1.hitung_keuntungan())} per unit")

    print("\n[CEK RELASI PEWARISAN]")
    print(f"  isinstance(baju1, Produk)   : {isinstance(baju1, Produk)}")
    print(f"  isinstance(baju1, Celana)   : {isinstance(baju1, Celana)}")
    print(f"  issubclass(Aksesoris, Produk): {issubclass(Aksesoris, Produk)}")
    print(f"  MRO Baju: {[k.__name__ for k in Baju.mro()]}")

    print("\n[UJI SETTER VALID] Mengubah harga Kaos Lacoste menjadi 270000...")
    baju1.harga = 270000
    print(f"  Harga baru: {Produk.format_rupiah(baju1.harga)}")
    print("[UJI SETTER INVALID] Mengubah stok Kaos Lacoste menjadi -10...")
    baju1.stok = -10
    Produk.ubah_diskon_default(15)
    print(f"  Total produk dibuat (Class Method): {Produk.get_total_produk()}")
    print(f"  Validasi kategori 'Baju' (Static Method): {Toko.validasi_kategori('Baju')}\n")

    print(">>> 3. AGREGASI: Toko 'memiliki' Produk <<<")
    toko1 = Toko("Toko Baju Brand - Balikpapan")
    toko2 = Toko("Toko Baju Brand - Samarinda")

    toko1.tambahProduk(baju1)
    toko1.tambahProduk(baju2)
    toko1.tambahProduk(celana1)
    toko1.tambahProduk(aksesoris1)
    toko2.tambahProduk(celana2)
    toko2.tambahProduk(aksesoris2)
    toko1.getAllProduk()

    print("\n[UPDATE & DELETE (CRUD)]")
    toko1.updateProduk("Jaket H&M", hargaBaru=500000, stokBaru=10)
    toko1.hapusProduk("Celana Rucas")
    print(f"  Produk dihapus dari toko, objeknya tetap ada: {celana1.info()}")

    print("\n[BUKTI AGREGASI] Toko Bontang dibuat, diisi produk, lalu dihapus (del):")
    toko_sementara = Toko("Toko Baju Brand - Bontang")
    toko_sementara.tambahProduk(baju2)
    del toko_sementara
    print(f"  Objek Toko sudah dihapus, tetapi Produk tetap utuh:\n  {baju2.info()}\n")

    print(">>> 4. ASOSIASI: Admin & Pembeli 'menggunakan' Toko <<<")
    print("[Admin belum login mencoba menambah produk]")
    baju3 = Baju("Kemeja Uniqlo", "Uniqlo", 350000, 7, 200000, "M", "Linen")
    admin2.tambah_produk_ke_toko(toko1, baju3)

    print("\n[Admin sudah login menambah produk]")
    admin1.login("admin_utama", "rahasia123")
    admin1.tambah_produk_ke_toko(toko1, baju3)
    admin1.hapus_produk_dari_toko(toko2, "Kacamata Rayban")
    toko2.tambahProduk(aksesoris2)

    print("\n[Pembeli memakai Toko lewat parameter method]")
    pembeli1 = Pembeli("Udin")
    pembeli2 = Pembeli("Sari")

    pembeli1.belanja_di(toko1, "Kaos Lacoste", 2)
    pembeli1.belanja_di(toko1, "Topi Nike", 1)
    pembeli1.belanja_di(toko1, "Jaket H&M", 100)
    pembeli1.belanja_di(toko1, "Celana Tidak Ada", 1)
    pembeli2.belanja_di(toko2, "Kacamata Rayban", 1)
    pembeli2.belanja_di(toko2, "Jeans Levi's", 1)
    print(f"  Pembeli tidak menyimpan Toko sebagai atribut: {'toko' in vars(pembeli1)}\n")

    print(">>> 5. KOMPOSISI: Transaksi 'terdiri dari' ItemTransaksi <<<")
    trx1 = pembeli1.checkout()
    trx2 = pembeli2.checkout()
    if trx1:
        trx1.cetakStruk()
    if trx2:
        trx2.cetakStruk()

    print("[BUKTI KOMPOSISI] ItemTransaksi ikut musnah bersama Transaksi:")
    ref_item = weakref.ref(trx2.daftar_item[0])
    print(f"  Item sebelum Transaksi dihapus : {ref_item()}")
    del trx2
    gc.collect()
    print(f"  Item setelah Transaksi dihapus : {ref_item()}  (None = ikut musnah)")

    Pembeli.ubah_diskon_member(10)
    Transaksi.atur_ppn(11)
    print(f"  Diskon dummy (Static Method): {Pembeli.hitung_diskon(100000, Pembeli.diskon_member)}")
    print(f"  Kode transaksi (Static Method): {Transaksi.buat_kode_transaksi(99)}")

    print("\n" + "=" * 60)
    print("SUMMARY STATISTIK SISTEM:")
    print(f"- Total Admin Terdaftar    : {Admin.total_admin}")
    print(f"- Total Produk Terdaftar   : {Produk.total_produk}")
    print(f"- Total Pembeli Terdaftar  : {Pembeli.total_pembeli}")
    print(f"- Total Transaksi Berhasil : {Toko.total_transaksi}")
    print("=" * 60)
    print("\n########## SELURUH PENGUJIAN SELESAI ##########\n")
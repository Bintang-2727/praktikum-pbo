# class MesinATM:

#     def __init__(self, id_atm, lokasi, saldo_kas):
#         self.id_atm = id_atm
#         self.lokasi = lokasi
#         self.saldo_kas = saldo_kas

#     def proses_penarikan(self, nama_nasabah, jumlah):
#         if jumlah <= self.saldo_kas:
#             self.saldo_kas -= jumlah
#             print(
#                 f" [ATM {self.id_atm}] Penarikan Rp{jumlah:,} oleh {nama_nasabah} berhasil."
#             )
#             print(f" Sisa kas di ATM {self.lokasi}: Rp{self.saldo_kas:,}")
#         else:
#             print(f" [ATM {self.id_atm}] Saldo kas mesin tidak mencukupi.")


# class Nasabah:

#     def __init__(self, nama, nomor_rekening):
#         self.nama = nama
#         self.nomor_rekening = nomor_rekening
#         # Tidak ada self.atm = ...
#         # Nasabah tidak memiliki mesin ATM secara permanen.

#     def tarik_tunai(self, atm, jumlah):
#         """Asosiasi: MesinATM diterima sebagai parameter dan dipakai sementara."""
#         print(
#             f" {self.nama} memasukkan kartu ke ATM unit {atm.id_atm} ({atm.lokasi})..."
#         )
#         atm.proses_penarikan(self.nama, jumlah)


# # Kedua objek dibuat secara independen
# atm_pusat = MesinATM("ATM-01", "Kantor Cabang Sudirman", 50000000)
# budi = Nasabah("Budi Santoso", "101-220-334")
# siti = Nasabah("Siti Rahma", "101-445-889")

# # Asosiasi berjalan saat method dipanggil
# budi.tarik_tunai(atm_pusat, 500000)

# # Mesin ATM yang sama bisa digunakan oleh nasabah lain
# siti.tarik_tunai(atm_pusat, 1000000)


class Shop:

    def __init__(self, name):
        self.name = name

    def proses_pembelian(self, hero, item):
        if hero.gold >= item.harga:
            hero.gold -= item.harga
            print(
                f"[{self.name}] {hero.name} berhasil membeli {item.nama}. Sisa gold: {hero.gold}"
            )
            return True
        print(
            f"[{self.name}] Gold {hero.name} tidak cukup untuk membeli {item.nama}!"
        )
        return False


class Item:

    def __init__(self, nama, harga, bonus_attack=0, bonus_armor=0):
        self.nama = nama
        self.harga = harga
        self.bonus_attack = bonus_attack
        self.bonus_armor = bonus_armor

    def __str__(self):
        return f"Item {self.nama} | +{self.bonus_attack} attack | +{self.bonus_armor} armor"


class Hero:
    jumlahHero = 0
    MAKS_SLOT = 4

    def __init__(self, name, health, mana, armor, attack, gold, list_skill):
        self.name = name
        self.health = health
        self.mana = mana
        self.armor = armor
        self.attack = attack
        self.gold = gold
        self.list_skill = list_skill
        self.item = []
        Hero.jumlahHero += 1

    def beli_item(self, shop, item):
        if len(self.item) >= self.MAKS_SLOT:
            print(f"Inventory {self.name} dah penuh brok!")
            return
        if shop.proses_pembelian(self, item):
            self.item.append(item)

    def ambil_item(self, item):
        if len(self.item) < Hero.MAKS_SLOT:
            self.item.append(item)
            print(f"+ {self.name} mengambil {item.name}")


brodi = Hero("Brodi", 3000, 1000, 10, 100, 100, ["tembak", "loncat"])
shop = Shop("Toko Item Mobile")
bod = Item("BOD", 3100, bonus_attack=160)
winter = Item("Winter Truncheon", 2140, bonus_attack=15, bonus_armor=45)

brodi.beli_item(shop, bod)

brodi.gold = 3000
brodi.beli_item(shop, winter)
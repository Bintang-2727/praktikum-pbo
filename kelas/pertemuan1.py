# class Hero:

#     def __init__(self, name, health, attack_power):
#         self.name = name
#         self.health = health
#         self.attack_power = attack_power
#         self.is_alive = True
#         print(f"{self.name} has entered the game with {self.health} health and {self.attack_power} attack power.")

# roger = Hero("Roger", 100, 20)
# print(roger.name)
# sniper = Hero("Sniper", 80, 25)


# class Tim:
#     nama_liga = "MPL Indonesia"

#     def __init__(self, nama, ceo):
#         self.nama = nama
#         self.ceo = ceo

# rrq = Tim("RRQ Hoshi", "Pak AP")
# evos = Tim("Evos Legends", "Hartman Harris")
# alter_ego = Tim("Alter Ego", "Koh Delwyn")

# print(f"{rrq.nama} (CEO: {rrq.ceo}) - Liga: {Tim.nama_liga}\n")
# print(f"{evos.nama} (CEO: {evos.ceo}) - Liga: {Tim.nama_liga}\n")
# print(f"{alter_ego.nama} (CEO: {alter_ego.ceo}) - Liga: {Tim.nama_liga}\n")

# rrq.ceo = "Pak AP Manullang"
# print(f"{rrq.nama} (CEO: {rrq.ceo}) - Liga: {Tim.nama_liga}\n")

# Tim.nama_liga = "MPL Indonesia Season 15"
# print(f"{rrq.nama} (CEO: {rrq.ceo}) - Liga: {Tim.nama_liga}\n")
# print(f"{evos.nama} (CEO: {evos.ceo}) - Liga: {Tim.nama_liga}\n")
# print(f"{alter_ego.nama} (CEO: {alter_ego.ceo}) - Liga: {Tim.nama_liga}\n")


class Pertandingan:
    musim_liga = "MPL Indonesia Season 14"

def __init__(self, tim_a, tim_b):
    self.tim_a = tim_a
    self.tim_b = tim_b
    self.skor_a = 0
    self.skor_b = 0
    self.selesai = False

def tambah_skor(self, tim, poin=1):
    if tim == self.tim_a:
        self.skor_a += poin
    elif tim == self.tim_b:
        self.skor_b += poin
    else:
        print(f"{tim} tidak terdaftar di pertandingan ini!")

def selesaikan(self):
    self.selesai = True

def tampilkan_hasil(self):
    status = "Selesai" if self.selesai else "Berlangsung"
    print(f"{self.tim_a} {self.skor_a} - {self.skor_b} {self.tim_b} "
        f"({status}, {Pertandingan.musim_liga})")
@classmethod
def dari_dict(cls, data):
    return cls(data["tim_a"], data["tim_b"])

@classmethod
def ganti_musim(cls, musim_baru):
    cls.musim_liga = musim_baru

@staticmethod
def validasi_nama_tim(nama_tim):
    tim_terdaftar = ["RRQ", "Evos Legends", "Alter Ego", "ONIC"]
    return nama_tim in tim_terdaftar



@staticmethod
def tentukan_pemenang(tim_a, skor_a, tim_b, skor_b):
    if skor_a > skor_b:
        return tim_a
    elif skor_b > skor_a:
        return tim_b
    return "Seri"


print(Pertandingan.validasi_nama_tim("RRQ"))
print(Pertandingan.validasi_nama_tim("Team Baru"))

final = Pertandingan("RRQ", "Evos Legends")
final.tambah_skor("RRQ", 2)
final.tambah_skor("Evos Legends", 1)
final.selesaikan()
final.tampilkan_hasil()

data_laga = {"tim_a": "ONIC", "tim_b": "Alter Ego"}
laga2 = Pertandingan.dari_dict(data_laga)
laga2.tambah_skor("ONIC", 2)
laga2.tampilkan_hasil()

Pertandingan.ganti_musim("MPL Indonesia Season 15")
final.tampilkan_hasil()
laga2.tampilkan_hasil()
pemenang = Pertandingan.tentukan_pemenang("RRQ",
final.skor_a, "Evos Legends", final.skor_b)
print(f"Pemenang: {pemenang}")
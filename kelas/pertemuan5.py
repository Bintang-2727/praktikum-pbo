from abc import ABC, abstractmethod

class Hero(ABC):
    def __init__(self, name, attack,health, armor):
        self.name = name
        self.attack = attack
        self.health = health
        self.armor = armor

    @abstractmethod
    def ultimate(self, target):
        pass

    def hitung_damage(self, target):
        return max(self.attack - target.armor, 0)

    def serang(self, target):
        damage = self.hitung_damage(target)
        target.health -= damage
        print(f'{self.name} menyerang {target.name,} damage {damage}')

    def __add__(self, Healing):
        return self.health + Healing

    def __sub__(self, burn):
        darah = self.health
        for i in range(10):
            darah = darah - burn
            print('Darah:', darah)
        self.health = darah
        print(self.health)

class Mage(Hero):
    def hitung_damage(self, target):
        return self.attack #armor nyo tembusss

    def ultimate(self, target):
        return (self.attack * 88) - target.health

class Warrior(Hero):
    def hitung_damage(self, target):
        return super().hitung_damage(target) + 10 #bonus 10

    def ultimate(self, target):
        return (self.attack * 77) - target.health

class Minion():
    def __init__(self,name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

sora = Warrior('Sora', 60, 100, 30)
eudora = Mage('Eudora', 100, 60, 5)
minion = Minion('Minion', 100, 30)

eudora.serang(sora)
sora.serang(eudora)
eudora.serang(minion)       

print(sora.ultimate(eudora))

print(eudora + 120)

# print(eudora - 1)
print(isinstance(eudora, Hero))
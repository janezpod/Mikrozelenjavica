import os
import json
import hashlib
from base64 import b64encode, b64decode, encode
from datetime import datetime

def zakrij_geslo(geslo):    
    s = os.urandom(32)
    sol = b64encode(s).decode('UTF-8')
    k = hashlib.pbkdf2_hmac('sha256', geslo.encode('UTF-8'), s, 100000)
    kljuc = b64encode(k).decode('UTF-8')
    z_geslo = {'geslo': {'sol': sol, 'kljuc': kljuc}}
    return z_geslo

class Stanje:
    def __init__(self):
        self.uporavniki = []
        self.administratorji = []
        self.narocila = []
        self.zelenjavica = [
        {'zaporedno_stevilo': 0, "vrsta":  "Brokoli", "cena": 2.5, 'cas_vzgoje': 7},
        {'zaporedno_stevilo': 1, "vrsta":  "Gorčica", "cena": 2.5, 'cas_vzgoje': 7 },
        {'zaporedno_stevilo': 2, "vrsta":  "Grah", "cena": 2.5, 'cas_vzgoje': 15},
        {'zaporedno_stevilo': 3, "vrsta":  "Kreša", "cena": 2.5, 'cas_vzgoje': 7},
        {'zaporedno_stevilo': 4, "vrsta":  "Ohrovt", "cena": 2.5, 'cas_vzgoje': 10},
        {'zaporedno_stevilo': 5, "vrsta":  "Rdeče zelje", "cena": 2.5, 'cas_vzgoje': 10},
        {'zaporedno_stevilo': 6, "vrsta":  "Redkvica", "cena": 2.5, 'cas_vzgoje': 7},
        {'zaporedno_stevilo': 7, "vrsta":  "Sončnica", "cena": 2.5, 'cas_vzgoje': 7},
        {'zaporedno_stevilo': 8, "vrsta":  "Zelje", "cena": 2.5, 'cas_vzgoje': 9}
        ]   
    
    def ustvari_zelenjavico(self, vrsta, cena, cas_vzgoje):
        nova_zelenjavica = {'zaporedno_stevilo': len(stanje.zelenjavica) + 1, 'vrsta': vrsta, 'cena': cena, 'cas_vzgoje': cas_vzgoje}
        return stanje.zelenjavica.append(nova_zelenjavica)

    def aktiviraj_zelenjavico(self, zaporedno_stevilo):
        pass

stanje = Stanje()

class Narocilo:
    def __init__(self, narocnik, stevilka=1, narocil='', naroceno=[], stanje='', sporocilo='', datum_narocila=datetime.now()):
        self.narocnik = narocnik
        self.stevilka = stevilka
        if narocil:
            self. narocil = narocil
        else:
            self.narocil = narocnik
        self.naroceno = naroceno
        self.stanje = stanje
        self.sporocilo = sporocilo
        self.datum_narocila = datum_narocila

    def v_slovar(self):
        datum_narocila = self.datum_narocila.isoformat()
        return {
            'številka naročila': self.stevilka,
            'naročnik': self.narocnik,
            'naročil': self.narocil,
            'stanje': self.stanje,
            'datum naročila': datum_narocila,        
            'naročeno': [{'zaporedna številka': zel['zaporedno_stevilo'], 'vrsta': zel['vrsta'], 'število': zel['stevilo'], 'cena': zel['cena']} \
                for zel in self.naroceno if zel['stevilo']],
            'sporočilo': self.sporocilo
        }       

    def shrani_v_datoteko(self):
        datoteka = 'narocila/narocila.json'
        narocila = []
        if os.path.exists(datoteka):
            with open(datoteka, 'r', encoding='UTF-8') as dat:
                narocila = json.load(dat)
            stevilka_narocila = len(narocila)
            self.stevilka = int(narocila[stevilka_narocila - 1]['številka naročila']) + 1
        slovar = self.v_slovar()
        narocila.append(slovar)
        with open(datoteka, 'w', encoding='UTF-8') as dat:
            json.dump(narocila, dat, ensure_ascii=False, indent=4) 


class Uporabnik:
    def __init__(self, u_ime, u_geslo, ime=None, pravice='uporabnik'):
        self.u_ime = u_ime
        self.u_geslo = u_geslo
        self.ime = ime
        self.pravice = pravice

    def v_slovar(self):
        return {
            'u_ime': self.u_ime,
            'u_geslo': self.u_geslo,
            'pravice': self.pravice
        }

    def shrani_v_datoteko(self):
        datoteka = 'uporabniki/' + self.u_ime + '.json'
        with open(datoteka, 'w', encoding='UTF-8') as dat:
            slovar = self.v_slovar()
            json.dump(slovar, dat, ensure_ascii=False, indent=4)
    
    def spremeni_geslo(self, n_geslo):
        datoteka = 'uporabniki/' + self.u_ime + '.json'
        os.remove(datoteka)
        return Uporabnik(self.u_ime, n_geslo).shrani_v_datoteko()
    
    def prijava(self):
        datoteka = 'uporabniki/' + self.u_ime + '.json'
        if os.path.isfile(datoteka) == False:
            napaka = 'Uporabnik ne obstaja. Prijava ni uspela.'
            return False
        else:
            if self.preveri_geslo() == True:
                return True
            else:
                napaka = 'Vnesli ste napačno geslo. Prijava ni uspela.'
                return False                

    def preveri_geslo(self):
        datoteka = 'uporabniki/' + self.u_ime + '.json'
        with open(datoteka, 'r', encoding='UTF-8') as dat:
            slovar = json.load(dat)
        sol = slovar['u_geslo']['geslo']['sol']
        s = b64decode(sol.encode('UTF-8'))
        z_geslo = hashlib.pbkdf2_hmac('sha256', self.u_geslo.encode('UTF-8'), s, 100000)
        if b64encode(z_geslo).decode('UTF-8') == slovar['u_geslo']['geslo']['kljuc']:
            return True
        else:
            return False

class Administrator(Uporabnik):
    pass
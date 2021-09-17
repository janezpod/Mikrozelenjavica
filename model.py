import os
import json
import hashlib
from base64 import b64encode, b64decode



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
            {'zaporedno_stevilo': 1, 'vrsta': 'Test', 'cena': 3.5, 'faza': [3,4]}
        ]
    
    def ustvari_zelenjavico(self, vrsta, cena, faza):
        nova_zelenjavica = {'zaporedno_stevilo': len(Stanje.zelenjavica) + 1, 'vrsta': vrsta, 'cena': cena, 'faza': faza}
        return Stanje.zelenjavica.append(nova_zelenjavica)

    def ustvari_narocilo(self, narocilo):
        pass
    
    def spremeni_narocilo(self, narocilo):
        pass

    def potrdi_narocilo(self, narocilo):
        pass

    def zakljuci_naroiclo(self, narocilo):
        pass

class Narocilo:
    def __init__(self, narocnik, datum_narocila, datum_dostave, artikli):
        self.narocnik = narocnik
        self.datum_narocila = datum_narocila
        self.datum_dostave = datum_dostave
        self.artikli = artikli


class Uporabnik:
    def __init__(self, u_ime, u_geslo, ime=None):
        self.u_ime = u_ime
        self.u_geslo = u_geslo
        self.ime = ime

    def v_slovar(self):
        return {
            'u_ime': self.u_ime,
            'u_geslo': self.u_geslo
        }

    def shrani_v_datoteko(self):
        datoteka = 'uporabniki/' + self.u_ime + '.json'
        with open(datoteka, 'w+', encoding='UTF-8') as dat:
            slovar = self.v_slovar()
            json.dump(slovar, dat, ensure_ascii=False, indent=4)
    
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
import os
import json
import hashlib
from base64 import b64encode



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
            {'zap_stevilo': 1, 'vrsta': 'Test', 'cena': 3.5, 'faza': (3,4)}
        ]

    def ustvari_narocilo(self, narocilo):
        pass
    
    def spremeni_narocilo(self, narocilo):
        pass

    def potrdi_narocilo(self, narocilo):
        pass

    def zakljuci_naroiclo(self, narocilo):
        pass

class Narocilo:
    pass

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

class Administrator(Uporabnik):
    pass

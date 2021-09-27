import os
import bottle
from datetime import date
from model import Stanje, Narocilo, Uporabnik, zakrij_geslo, stanje

SIFRA = os.urandom(4)

@bottle.get('/')
def osnovna_zaslon():
    u_ime = bottle.request.get_cookie('uporabnisko_ime', secret=SIFRA)
    if u_ime: 
        narocila = Uporabnik(u_ime).zberi_narocila()
        return bottle.template('osnovni_zaslon.html', u_ime=u_ime, narocila=narocila)
    else:
        return bottle.template('zacetna_stran.html')

@bottle.get('/registracija')
def registracija_get():
    sporocila = []
    return bottle.template('registracija.html', sporocila=sporocila, polja={'uporabnisko_ime': None}, u_ime='')

@bottle.post('/registracija')
def registracija_post():
    sporocila = []
    u_ime = bottle.request.forms.getunicode('u_ime').lower()
    u_geslo = bottle.request.forms.getunicode('u_geslo')
    p_geslo = bottle.request.forms.getunicode('p_geslo')
    if u_geslo != p_geslo:
        sporocila = {'geslo': 'Vpisani gesli se razlikujeta. Poizkusite znova.'}
        return bottle.template('registracija.html', sporocila=sporocila)
    elif len(u_geslo) < 6:
        sporocila = {'geslo': 'Geslo mora biti dolgo vsaj šest znakov! Izberite drugo geslo.'}
        return bottle.template('registracija.html', sporocila=sporocila)
    if os.path.exists('uporabniki/' + u_ime + '.json'):
        sporocila = {'u_ime': 'Uporabnisko ime ' + u_ime + ' že obstaja.'}
        return bottle.template('registracija.html', sporocila=sporocila)
    else:
        z_geslo = zakrij_geslo(u_geslo)
        Uporabnik(u_ime, z_geslo).shrani_v_datoteko()
        bottle.response.set_cookie('uporabnisko_ime', u_ime, path='/', secret=SIFRA)
        bottle.redirect('/')

@bottle.get('/prijava')
def prijava_get():
    sporocila = []
    return bottle.template('prijava.html', sporocila = sporocila)

@bottle.post('/prijava')
def prijava_post():
    sporocila = []
    u_ime = bottle.request.forms.getunicode('u_ime').lower()
    u_geslo = bottle.request.forms.getunicode('u_geslo')
    if Uporabnik(u_ime, u_geslo).prijava():
        bottle.response.set_cookie('uporabnisko_ime', u_ime, path='/', secret=SIFRA)
        bottle.redirect('/')
    else:
        sporocila = {'geslo': 'Prijava ni uspela. Poizkusite znova.'}
        return bottle.template('prijava.html', sporocila = sporocila)

@bottle.get('/novo_narocilo')
def novo_narocilo_get():
    u_ime = bottle.request.get_cookie('uporabnisko_ime', secret=SIFRA)
    if not u_ime:
        bottle.redirect('/')
    else:
        zelenjavice = stanje.zelenjavica
        return bottle.template('novo_narocilo.html', u_ime=u_ime, zelenjavice=zelenjavice, naroceno=[], korak ='priprava narocila')

@bottle.post('/novo_narocilo')
def narocilo_post():
    u_ime = bottle.request.get_cookie('uporabnisko_ime', secret=SIFRA)
    if not u_ime:
        bottle.redirect('/')
    else:
        zelenjavice = stanje.zelenjavica
        zelenjavice_narocene =[]
        potrdi = False
        for zelenjava in zelenjavice:
            zelenjavica_narocena = {}
            zaporedno_s = str(zelenjava['zaporedno_stevilo'])
            stevilo_narocenih = int(bottle.request.forms.getunicode(zaporedno_s))
            if stevilo_narocenih > 0:
                potrdi = True
            zelenjavica_narocena['zaporedno_stevilo'] = zaporedno_s
            zelenjavica_narocena['vrsta'] = zelenjava['vrsta']
            zelenjavica_narocena['cena'] = zelenjava['cena']
            zelenjavica_narocena['stevilo'] = stevilo_narocenih
            zelenjavice_narocene.append(zelenjavica_narocena)
        if not potrdi:
            bottle.redirect('/novo_narocilo')
        else:
            korak = bottle.request.forms.getunicode('korak')
            if korak == 'potrditev narocila':
                return bottle.template('novo_narocilo.html', u_ime=u_ime, zelenjavice=zelenjavice, naroceno=zelenjavice_narocene, korak = 'potrditev narocila')
            elif korak == 'shrani narocilo':
                sporocilo = str(bottle.request.forms.getunicode('sporocilo'))
                narocilo = Narocilo(narocnik=u_ime, stanje='naroceno', naroceno=zelenjavice_narocene, sporocilo=sporocilo)
                narocilo.shrani_v_datoteko()
                return bottle.template('potrdi_narocilo.html', u_ime=u_ime, zelenjavice=zelenjavice, naroceno=zelenjavice_narocene, korak = 'shrani porocilo')
            else:
                pass

@bottle.get('/spremeni_podatke')
def spremeni_podatke_get():
    sporocila = []
    u_ime = bottle.request.get_cookie('uporabnisko_ime', secret=SIFRA)
    if not u_ime:
        bottle.redirect('/')
    else:
        return bottle.template('spremeni_podatke.html', u_ime=u_ime, sporocila=sporocila)

@bottle.post('/spremeni_podatke')
def spremeni_podatke_post():
    u_ime = bottle.request.get_cookie('uporabnisko_ime', secret=SIFRA)
    if not u_ime:
        bottle.redirect('/')
    else:
        s_geslo = bottle.request.forms.getunicode('s_geslo')
        n_geslo = bottle.request.forms.getunicode('n_geslo')
        p_geslo = bottle.request.forms.getunicode('p_geslo')
        if n_geslo != p_geslo or Uporabnik(u_ime, s_geslo).preveri_geslo() == False:
            sporocila = {'geslo': 'Poizkusite znova.'}
            return bottle.template('spremeni_podatke.html', sporocila=sporocila)
        elif len(n_geslo) < 6:
            sporocila = {'geslo': 'Novo geslo naj bo dolgo vsaj šest znakov.'}
            return bottle.template('spremeni_podatke.html', sporocila=sporocila)
        else:
            z_geslo = zakrij_geslo(n_geslo)
            Uporabnik(u_ime, s_geslo).spremeni_geslo(z_geslo)
            sporocila = {'uspesno': 'Ušpesno ste spremenili geslo.'}
            return bottle.template('spremeni_podatke.html', sporocila=sporocila)

@bottle.get('/ponudba')
def ponudba_get():
    u_ime = bottle.request.get_cookie('uporabnisko_ime', secret=SIFRA)
    slika = 'B_V3.jpg'
    return bottle.template('ponudba.html', u_ime=u_ime, picture=slika)

@bottle.get('/images/<picture>')
def images(picture):
    return bottle.static_file(picture, 'images')

@bottle.get('/odjava')
def odjava_get():
    bottle.response.delete_cookie('uporabnisko_ime', path='/', secret=SIFRA)
    bottle.redirect('/')



bottle.run(debug=True, reloader=True)
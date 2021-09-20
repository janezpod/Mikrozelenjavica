import os
import bottle
from datetime import date
from model import Stanje, Narocilo, Uporabnik, zakrij_geslo

SIFRA = os.urandom(4)
stanje = Stanje()

@bottle.get('/')
def osnovna_zaslon():
    u_ime = bottle.request.get_cookie('uporabnisko_ime', secret=SIFRA)
    if u_ime:
        return bottle.template('osnovni_zaslon.html', u_ime=u_ime)
    else:
        return bottle.template('zacetna_stran.html')

@bottle.get('/registracija')
def registracija_get():
    napake = []
    return bottle.template("registracija.html", napake=napake, polja={"uporabnisko_ime": None}, u_ime='')

@bottle.post('/registracija')
def registracija_post():
    napake = []
    u_ime = bottle.request.forms.getunicode('u_ime').lower()
    u_geslo = bottle.request.forms.getunicode('u_geslo')
    p_geslo = bottle.request.forms.getunicode('p_geslo')
    if u_geslo != p_geslo:
        napake = {'geslo': 'Vpisani gesli se razlikujeta. Poizkusite znova.'}
        return bottle.template('registracija.html', napake=napake)
    elif len(u_geslo) < 6:
        napake = {'geslo': 'Geslo mora biti dolgo vsaj šest znakov! Izberite drugo geslo.'}
        return bottle.template('registracija.html', napake=napake)
    if os.path.exists('uporabniki/' + u_ime + '.json'):
        napake = {'u_ime': 'Uporabnisko ime ' + u_ime + ' že obstaja.'}
        return bottle.template('registracija.html', napake=napake)
    else:
        z_geslo = zakrij_geslo(u_geslo)
        Uporabnik(u_ime, z_geslo).shrani_v_datoteko()
        bottle.response.set_cookie('uporabnisko_ime', u_ime, path='/', secret=SIFRA)
        bottle.redirect("/")

@bottle.get('/prijava')
def prijava_get():
    return bottle.template('prijava.html')

@bottle.post('/prijava')
def prijava_post():
    u_ime = bottle.request.forms.getunicode('u_ime').lower()
    u_geslo = bottle.request.forms.getunicode('u_geslo')
    if Uporabnik(u_ime, u_geslo).prijava() == True:
        bottle.response.set_cookie('uporabnisko_ime', u_ime, path='/', secret=SIFRA)
        bottle.redirect('/')
    else:
        bottle.redirect('/prijava')

@bottle.get('/odjava')
def odjava_get():
    bottle.response.delete_cookie('uporabnisko_ime', path='/', secret=SIFRA)
    bottle.redirect('/')

@bottle.get('/novo_narocilo')
def novo_narocilo_get():
    u_ime = bottle.request.get_cookie('uporabnisko_ime', secret=SIFRA)
    if not u_ime:
        bottle.redirect('/')
    else:
        zelenjavice = stanje.zelenjavica
        return bottle.template('novo_narocilo.html', u_ime=u_ime, zelenjavice=zelenjavice, naroceno=[], korak ='priprava naročila')

@bottle.get('/spremeni_podatke')
def spremeni_podatke_get():
    napake = []
    u_ime = bottle.request.get_cookie('uporabnisko_ime', secret=SIFRA)
    if not u_ime:
        bottle.redirect('/')
    else:
        return bottle.template('spremeni_podatke.html', u_ime=u_ime, napake=napake)

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
            napake = {'geslo': 'Poizkusite znova.'}
            return bottle.template('spremeni_podatke.html', napake=napake)
        elif len(n_geslo) < 6:
            napake = {'geslo': 'Novo geslo naj bo dolgo vsaj šest znakov.'}
            return bottle.template('spremeni_podatke.html', napake=napake)
        else:
            z_geslo = zakrij_geslo(n_geslo)
            Uporabnik(u_ime, s_geslo).spremeni_geslo(z_geslo)
            napake = {'geslo': 'Ušpesno ste spremenili geslo.'}
            return bottle.template('spremeni_podatke.html', napake=napake)




bottle.run(debug=True, reloader=True)
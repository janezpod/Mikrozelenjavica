import os
import bottle
from datetime import date
from model import Stanje, Narocilo, Uporabnik, zakrij_geslo

SIFRA = os.urandom(4)

@bottle.get('/')
def osnovna_zaslon():
    return bottle.template('osnovni_zaslon.html')

@bottle.get('/registracija')
def registracija_get():
    return bottle.template('registracija.html')

@bottle.get('/prijava')
def prijava_get():
    return bottle.template('prijava.html')

@bottle.post('/registracija')
def registracija_post():
    u_ime = bottle.request.forms.getunicode('u_ime').lower()
    u_geslo = bottle.request.forms.getunicode('u_geslo')
    if os.path.exists('uporabniki/' + u_ime + '.json'):
        napake = {u_ime: 'Uporabnisko ime že obstaja.'}
        return bottle.template('registracija.html', napake = napake)
    else:
        z_geslo = zakrij_geslo(u_geslo)
        Uporabnik(u_ime, z_geslo).shrani_v_datoteko()
        bottle.response.set_cookie("u_ime", u_ime, path="/", secret=SIFRA)
        bottle.redirect("/")

@bottle.post('/prijava')
def prijava_post():
    u_ime = bottle.request.forms.getunicode('u_ime').lower()
    u_geslo = bottle.request.forms.getunicode('u_geslo')
    if Uporabnik(u_ime, u_geslo).prijava() == True:
        return bottle.template('osnovni_zaslon.html')
    else:
        return bottle.template('prijava.html')

bottle.run(debug=True, reloader=True)
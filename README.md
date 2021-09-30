# Zelenjavica

## O projektu

Program je bil prvotno namenjen moji mami kot dodatek k že obstoječi [spletni strani](https://zelenjavica.si/), 
ki bi ji olajšal poslovanje z naročili. V trenutni obliki nima dovolj funkcionalosti za praktično uporabo.
Upam, da bom program v prihodnje izpopolnil.

Program omogoča registracijo računa, prijavo z računom, spremeniti geslo računa, ustvariti naročilo 
in pregeld nad naročili uporabnika. Predhodno je ustvarjen uporabnik `admin`, 
z geslom `spremenigeslo`, ki ima pregled nad naročili vseh uporabnikov.

## Navodila za zagon

Za zagon programa je potreben programski jezik [Python](https://www.python.org/).
Potrebno je namestiti tudi knjižnico [Bottle](http://bottlepy.org/).
To je najlažje storiti preko ukazne vrste z ukazom `pip install bottle`.
Če nimate nameščenega `pip`-a. lahko knjižnico še vedno prenesete preko preko navedene spletne strani.

Po tem odprite program in poženite datoteko `spletni_vmesnik.py` ter odprite [naslov](http://127.0.0.1:8080/).
from flask import render_template, request
from collections import OrderedDict
from tryktrak import app
import pickle, random

class Gra:
    def __init__(self, typ_gry):
        self.typ_gry = typ_gry
        if typ_gry == 'komputer':
            self.gracz1 = 'bordo'
            self.komputer = 'bialy'
        else:
            self.gracz1 = 'bordo'
            self.gracz2 = 'bialy'
        self.kolejka = 'gracz1'
        if self.kolejka == 'gracz1':
            self.aktywny_kolor = 'bordo'
        else:
            self.aktywny_kolor = 'bialy'
        self.plansza = OrderedDict()
        for x in range(24):
            numer = x+1
            klucz = 'pole_'+str(numer)
            self.plansza[klucz] = []
        self.plansza['pole_1'] = ['bordo', 'bordo']
        self.plansza['pole_6'] = ['bialy', 'bialy', 'bialy', 'bialy', 'bialy']
        self.plansza['pole_8'] = ['bialy', 'bialy', 'bialy']
        self.plansza['pole_12'] = ['bordo', 'bordo', 'bordo', 'bordo', 'bordo']
        self.plansza['pole_13'] = ['bialy', 'bialy', 'bialy', 'bialy', 'bialy']
        self.plansza['pole_17'] = ['bordo', 'bordo', 'bordo']
        self.plansza['pole_19'] = ['bordo', 'bordo', 'bordo', 'bordo', 'bordo']
        self.plansza['pole_24'] = ['bialy', 'bialy']

    def rzut_kostka(self):
        rzuty = []
        rzuty.append(random.randint(1, 6))
        rzuty.append(random.randint(1, 6))
        if rzuty[0] == rzuty[1]:
            rzuty.append(rzuty[0])
            rzuty.append(rzuty[0])
        self.rzuty = rzuty
        self.aktywne_rzuty = self.rzuty
        return self.rzuty, self.aktywne_rzuty

    def koniec_kolejki(self):
        if self.typ_gry == 'komputer':
            if self.kolejka == 'gracz1':
                self.kolejka = 'komputer'
            else:
                self.kolejka = 'gracz1'
        else:
            if self.kolejka == 'gracz1':
                self.kolejka = 'gracz2'
            else:
                self.kolejka = 'gracz1'
        if self.aktywny_kolor == 'bordo':
            self.aktywny_kolor = 'bialy'
        else:
            self.aktywny_kolor = 'bordo'
        self.rzut_kostka()

    def znajdz_mozliwe_ruchy(self):
        mozliwe_ruchy = []
        if len(self.aktywne_rzuty) == 1:
            mozliwe_ruchy.append(self.aktywne_rzuty[0])
        elif len(self.aktywne_rzuty) == 2:
            mozliwe_ruchy.append(self.aktywne_rzuty[0])
            mozliwe_ruchy.append(self.aktywne_rzuty[1])
            mozliwe_ruchy.append(self.aktywne_rzuty[0] + self.aktywne_rzuty[1])
        elif len(self.aktywne_rzuty) > 2:
            licznik = 1
            for x in self.aktywne_rzuty:
                mozliwe_ruchy.append(x * licznik)
        return mozliwe_ruchy

    def ruch(self, skad, dokad):
        skad_pole = 'pole_' + str(request.values['pionek'])
        dokad_pole = 'pole_' + str(request.values['pole'])
        mozliwe_ruchy = self.znajdz_mozliwe_ruchy()
        if self.aktywny_kolor == 'bordo':
            wartosc_ruchu = int(dokad)-int(skad)
            if wartosc_ruchu in mozliwe_ruchy:
                if 'bordo' in self.plansza[skad_pole]:
                    self.plansza[dokad_pole].append('bordo')
                    self.plansza[skad_pole].pop()
                elif 'bialy' in self.plansza[skad_pole]:
                    return 'To nie twój kolor pionków!'
                else:
                    return 'Na wybranym polu nie ma żadnego pionka!'
            else:
                return 'Nie możesz przesunąć pionka o taką liczbę oczek'
        else:
            if self.aktywny_kolor == 'bialy':
                wartosc_ruchu = int(skad)-int(dokad)
                if wartosc_ruchu in mozliwe_ruchy:
                    if 'bialy' in self.plansza[skad_pole]:
                        self.plansza[dokad_pole].append('bialy')
                        self.plansza[skad_pole].pop()
                    elif 'bordo' in self.plansza[skad_pole]:
                        return 'To nie twój kolor pionków!'
                    else:
                        return 'Na wybranym polu nie ma żadnego pionka!'
                else:
                    return 'Nie możesz przesunąć pionka o taką liczbę oczek'
        if wartosc_ruchu in self.aktywne_rzuty:
            self.aktywne_rzuty.remove(wartosc_ruchu)
        else:
            if len(self.aktywne_rzuty) == 2:
                self.aktywne_rzuty = []
            else:
                x = wartosc_ruchu/self.aktywne_rzuty[0]
                del self.aktywne_rzuty[-x:]
        if len(self.aktywne_rzuty) == 0:
            self.koniec_kolejki()
        self.znajdz_mozliwe_ruchy()



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/gra')
def gra():
    gra = Gra(request.values['typ_gry'])
    gra.rzut_kostka()
    rzuty = gra.rzuty
    with open('zapis.pickle', 'wb') as handle:
        pickle.dump(gra, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return render_template('gra.html', rzuty=rzuty, ruchy = gra.znajdz_mozliwe_ruchy(), aktywne_rzuty = gra.aktywne_rzuty,
                           typ_gry=gra.typ_gry, stan_gry = gra.plansza, kolejka=gra.kolejka)


@app.route('/ruch')
def ruch():
    with open('zapis.pickle', 'rb') as handle:
        gra = pickle.load(handle)

    skad = request.values['pionek']
    dokad = request.values['pole']
    komunikat = gra.ruch(skad, dokad)
    rzuty = gra.rzuty

    with open('zapis.pickle', 'wb') as handle:
        pickle.dump(gra, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return render_template('ruch.html', rzuty=rzuty, aktywne_rzuty = gra.aktywne_rzuty, ruchy = gra.znajdz_mozliwe_ruchy(), typ_gry=gra.typ_gry, stan_gry=gra.plansza,
                           komunikat=komunikat, kolejka=gra.kolejka)
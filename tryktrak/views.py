from flask import render_template, request, redirect, url_for
from collections import OrderedDict
from tryktrak import app
import pickle, random

class Gra:
    def __init__(self, typ_gry):
        self.typ_gry = typ_gry
        self.gracz1 = ''
        if typ_gry == 'komputer':
            self.gracz2 = 'Komputer'
        else:
            self.gracz2 = ''
        self.kolejka = self.gracz1
        if self.kolejka == self.gracz1:
            self.aktywny_kolor = 'bordo'
        else:
            self.aktywny_kolor = 'bialy'
        self.plansza = OrderedDict()
        for x in range(24):
            numer = x+1
            klucz = 'pole_'+str(numer)
            self.plansza[klucz] = []
        self.plansza['zbite'] = []
        self.plansza['pole_1'] = ['bordo', 'bordo']
        self.plansza['pole_6'] = ['bialy', 'bialy', 'bialy', 'bialy', 'bialy']
        self.plansza['pole_8'] = ['bialy', 'bialy', 'bialy']
        self.plansza['pole_12'] = ['bordo', 'bordo', 'bordo', 'bordo', 'bordo']
        self.plansza['pole_13'] = ['bialy', 'bialy', 'bialy', 'bialy', 'bialy']
        self.plansza['pole_17'] = ['bordo', 'bordo', 'bordo']
        self.plansza['pole_19'] = ['bordo', 'bordo', 'bordo', 'bordo', 'bordo']
        self.plansza['pole_24'] = ['bialy', 'bialy']

    def rzut_kostka(self):
        """Wykonuje rzut dwoma kostkami kostkami"""
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
        """Zmienia aktywnego gracza i aktywny kolor pod koniec kolejki"""
        if self.typ_gry == 'komputer':
            if self.kolejka == self.gracz1:
                self.kolejka = self.gracz2
            else:
                self.kolejka = self.gracz1
        else:
            if self.kolejka == self.gracz1:
                self.kolejka = self.gracz2
            else:
                self.kolejka = self.gracz1
        if self.aktywny_kolor == 'bordo':
            self.aktywny_kolor = 'bialy'
        else:
            self.aktywny_kolor = 'bordo'
        self.rzut_kostka()

    def znajdz_pozostale_ruchy(self):
        """Na podstawie wyrzuconych kostek zwraca wartości ruchu możliwe do wykonania"""
        pozostale_ruchy = []
        if len(self.aktywne_rzuty) == 1:
            pozostale_ruchy.append(self.aktywne_rzuty[0])
        elif len(self.aktywne_rzuty) == 2:
            pozostale_ruchy.append(self.aktywne_rzuty[0])
            pozostale_ruchy.append(self.aktywne_rzuty[1])
            pozostale_ruchy.append(self.aktywne_rzuty[0] + self.aktywne_rzuty[1])
        elif len(self.aktywne_rzuty) > 2:
            licznik = 1
            for x in self.aktywne_rzuty:
                pozostale_ruchy.append(x * licznik)
                licznik += 1
        return pozostale_ruchy

    def znajdz_mozliwe_ruchy(self):
        """Znajduje ruchy możliwe do wykonania przy aktualnie wyrzuconych kostkach"""
        pozostale_ruchy = self.znajdz_pozostale_ruchy()
        numer_pola = 1
        mozliwe_ruchy = dict()
        if self.aktywny_kolor == 'bialy':
            mozliwe_ruchy[0] = []
            if 'bialy' in self.plansza['zbite']:
                for ruch in pozostale_ruchy:
                    if 0 < 25-ruch < 25:
                        dokad = 25-ruch
                        pole_dokad = 'pole_' + str(dokad)
                        if 'bialy' in self.plansza[pole_dokad] or not self.plansza[pole_dokad] or len(self.plansza[pole_dokad]) == 1:
                            mozliwe_ruchy[0].append(ruch)
            else:
                for pole, wartosc in self.plansza.items():
                    if 'bialy' in wartosc:
                        mozliwe_ruchy[numer_pola] = []
                        for ruch in pozostale_ruchy:
                            if numer_pola - ruch > 0 and numer_pola - ruch < 25:
                                dokad = numer_pola - ruch
                                pole_dokad = 'pole_'+str(dokad)
                                if 'bialy' in self.plansza[pole_dokad] or not self.plansza[pole_dokad] or len(self.plansza[pole_dokad]) == 1:
                                    mozliwe_ruchy[numer_pola].append(dokad)
                    numer_pola += 1
        elif self.aktywny_kolor == 'bordo':
            if 'bordo' in self.plansza['zbite']:
                mozliwe_ruchy[0] = []
                for ruch in pozostale_ruchy:
                    if 0 < ruch < 25:
                        pole_dokad = 'pole_' + str(ruch)
                        if 'bordo' in self.plansza[pole_dokad] or not self.plansza[pole_dokad] or len(self.plansza[pole_dokad]) == 1:
                            mozliwe_ruchy[0].append(ruch)
            else:
                for pole, wartosc in self.plansza.items():
                    if 'bordo' in wartosc:
                        mozliwe_ruchy[numer_pola] = []
                        for ruch in pozostale_ruchy:
                            if numer_pola + ruch > 0 and numer_pola + ruch < 25:
                                dokad = numer_pola + ruch
                                pole_dokad = 'pole_'+str(dokad)
                                if 'bordo' in self.plansza[pole_dokad] or not self.plansza[pole_dokad] or len(self.plansza[pole_dokad]) == 1:
                                    mozliwe_ruchy[numer_pola].append(dokad)
                    numer_pola += 1
        return mozliwe_ruchy


    def ruch(self, skad, dokad):
        """Wykonuje ruch na podstawie przekazanych wartości pól"""

        if int(skad) == 0:
            skad_pole = 'zbite'
        else:
            skad_pole = 'pole_' + str(skad)
        dokad_pole = 'pole_' + str(dokad)
        pozostale_ruchy = self.znajdz_pozostale_ruchy()

        if self.aktywny_kolor == 'bordo':
            wartosc_ruchu = int(dokad) - int(skad)
            if 'bordo' in self.plansza['zbite']:
                if int(skad) != 0:
                    return "Najpierw musisz ściągnąć zbite pionki"
                else:
                    if int(dokad) in pozostale_ruchy:
                        if 'bialy' in self.plansza[dokad_pole]:
                            if len(self.plansza[dokad_pole]) == 1:
                                self.zbij_pionek(dokad_pole)
                            else:
                                return "Nie możesz przejść na pole, na którym znajdują się pionki przeciwnika"
                        self.plansza[dokad_pole].append('bordo')
                        self.plansza['zbite'].remove('bordo')
                        self.usun_wykorzystany_ruch(wartosc_ruchu)
                        return
                    else:
                        return "Nie możesz przejść na pole, na którym znajdują się pionki przeciwnika"
            if wartosc_ruchu in pozostale_ruchy:
                if 'bordo' in self.plansza[skad_pole]:
                    if 'bialy' in self.plansza[dokad_pole]:
                        if len(self.plansza[dokad_pole]) == 1:
                            self.zbij_pionek(dokad_pole)
                        else:
                            return "Nie możesz przejść na pole, na którym znajdują się pionki przeciwnika"
                    self.plansza[dokad_pole].append('bordo')
                    self.plansza[skad_pole].pop()
                    self.usun_wykorzystany_ruch(wartosc_ruchu)
                elif 'bialy' in self.plansza[skad_pole]:
                    return 'To nie twój kolor pionków!'
                else:
                    return 'Na wybranym polu nie ma żadnego pionka!'
            else:
                return 'Nie możesz przesunąć pionka o taką liczbę oczek'
        else:
            if self.aktywny_kolor == 'bialy':
                if 'bialy' in self.plansza['zbite']:
                    if int(skad) != 0:
                        return "Najpierw musisz ściągnąć zbite pionki"
                    else:
                        if 25-int(dokad) in pozostale_ruchy:
                            if 'bordo' in self.plansza[dokad_pole]:
                                if len(self.plansza[dokad_pole]) == 1:
                                    self.zbij_pionek(dokad_pole)
                                else:
                                    return "Nie możesz przejść na pole, na którym znajdują się pionki przeciwnika"
                            wartosc_ruchu = 25-int(dokad)
                            self.plansza[dokad_pole].append('bialy')
                            self.plansza['zbite'].remove('bialy')
                            self.usun_wykorzystany_ruch(wartosc_ruchu)
                            return
                        else:
                            return "Nie możesz przesunąć pionka o tyle oczek"
                wartosc_ruchu = int(skad)-int(dokad)
                if wartosc_ruchu in pozostale_ruchy:
                    if 'bialy' in self.plansza[skad_pole]:
                        if 'bordo' in self.plansza[dokad_pole]:
                            if len(self.plansza[dokad_pole]) == 1:
                                self.zbij_pionek(dokad_pole)
                            else:
                                return "Nie możesz przejść na pole, na którym znajdują się pionki przeciwnika"
                        self.plansza[dokad_pole].append('bialy')
                        self.plansza[skad_pole].pop()
                        self.usun_wykorzystany_ruch(wartosc_ruchu)
                    elif 'bordo' in self.plansza[skad_pole]:
                        return 'To nie twój kolor pionków!'
                    else:
                        return 'Na wybranym polu nie ma żadnego pionka!'
                else:
                    return 'Nie możesz przesunąć pionka o taką liczbę oczek'

    def ruch_komputera(self):
        mozliwe_ruchy = self.znajdz_mozliwe_ruchy()
        numer_pola = 1
        ewentualne_ruchy = dict()
        if 1 in mozliwe_ruchy or 2 in mozliwe_ruchy or 3 in mozliwe_ruchy or 4 in mozliwe_ruchy or 5 in mozliwe_ruchy or 6 in mozliwe_ruchy:
            for pionek, ruchy in mozliwe_ruchy:
                if pionek == 1 or pionek == 2 or pionek == 3 or pionek == 4 or pionek == 5 or pionek == 6:
                    for ruch in ruchy:
                        dokad = pionek-ruch
                        dokad_pole = 'pole_'+str(dokad)
                        skad_pole = 'pole_'+str(pionek)
                        if len(self.plansza[skad_pole]) != 2 and 'bialy' in self.plansza[dokad_pole] or len(self.plansza[dokad_pole] == 1) :
                            self.plansza[dokad_pole].append('bialy')
                            self.plansza[skad_pole].pop()
                            return
                        else:
                            ewentualne_ruchy[skad_pole] = dokad_pole
        else:
            for pole, wartosc in self.plansza:
                if 'bialy' in wartosc and len(self.plansza[pole]) == 1:
                    if numer_pola in mozliwe_ruchy:
                        ruchy = mozliwe_ruchy[numer_pola]
                        for ruch in ruchy:
                            dokad = numer_pola - ruch
                            dokad_pole = 'pole_' + str(dokad)
                            skad_pole = 'pole_' + str(numer_pola)


    def ruch_komp(self):
        mozliwe_ruchy = self.znajdz_mozliwe_ruchy()
        for pionek, ruchy in mozliwe_ruchy.items():
            if ruchy:
                dokad_pole = 'pole_' + str(ruchy[0])
                skad_pole = 'pole_' + str(pionek)
                self.plansza[dokad_pole].append('bialy')
                self.plansza[skad_pole].pop()
                wartosc_ruchu = ruchy[0]-pionek
                self.usun_wykorzystany_ruch(wartosc_ruchu)
                return "Komputer wykonał ruch z pola %d na pole %d" % (pionek, ruchy[0])

    def wywolaj_ruch(self):
        komunikaty = []
        while self.kolejka == 'Komputer':
            komunikaty.append(self.ruch_komp())
        return komunikaty



    def usun_wykorzystany_ruch(self, wartosc_ruchu):
        """Usuwa wykorzystane wartości ruchu z aktywnych rzutów"""
        if wartosc_ruchu in self.aktywne_rzuty:
            self.aktywne_rzuty.remove(wartosc_ruchu)
        else:
            if len(self.aktywne_rzuty) == 2:
                self.aktywne_rzuty = []
            else:
                x = int(wartosc_ruchu / self.aktywne_rzuty[0])
                del self.aktywne_rzuty[-x:]
        if len(self.aktywne_rzuty) == 0:
            self.koniec_kolejki()
        self.znajdz_pozostale_ruchy()

    def zbij_pionek(self, pole):
        """Zbija pionek z pola przekazanego w zmiennej"""
        if self.aktywny_kolor == 'bordo':
            pionek = 'bialy'
        else:
            pionek = 'bordo'
        self.plansza['zbite'].append(pionek)
        self.plansza[pole].pop()
        





@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/wybierzgraczy')
def wybierzgraczy():
    gra = Gra(request.values['typ_gry'])

    with open('zapis.pickle', 'wb') as handle:
        pickle.dump(gra, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return render_template('wybierzgraczy.html', typ_gry = gra.typ_gry)

@app.route('/gra')
def gra():
    with open('zapis.pickle', 'rb') as handle:
        gra = pickle.load(handle)

    gra.gracz1 = request.values['gracz1']
    gra.kolejka = gra.gracz1
    if gra.typ_gry == 'gracze':
        gra.gracz2 = request.values['gracz2']
    gra.rzut_kostka()
    rzuty = gra.rzuty
    with open('zapis.pickle', 'wb') as handle:
        pickle.dump(gra, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return render_template('gra.html', rzuty=rzuty, ruchy = gra.znajdz_pozostale_ruchy(), aktywne_rzuty = gra.aktywne_rzuty,
                           typ_gry=gra.typ_gry, stan_gry = gra.plansza, kolejka=gra.kolejka)


@app.route('/ruch')
def ruch():
    with open('zapis.pickle', 'rb') as handle:
        gra = pickle.load(handle)

    if gra.typ_gry == 'komputer' and gra.kolejka == 'Komputer':
        komunikaty = gra.wywolaj_ruch()
    else:
        skad = request.values['pionek']
        dokad = request.values['pole']
        komunikaty = gra.ruch(skad, dokad)

    rzuty = gra.rzuty
    zbite = gra.plansza['zbite']

    with open('zapis.pickle', 'wb') as handle:
        pickle.dump(gra, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return render_template('ruch.html', rzuty=rzuty, aktywne_rzuty = gra.aktywne_rzuty, ruchy = gra.znajdz_pozostale_ruchy(),
                           typ_gry=gra.typ_gry, stan_gry=gra.plansza, komunikaty=komunikaty, kolejka=gra.kolejka, zbite=zbite,
                           mozliwe_ruchy = gra.znajdz_mozliwe_ruchy())
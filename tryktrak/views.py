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
        self.plansza['pole_x'] = []
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
        numer_pola_dom = 1
        sciaganie = 1
        mozliwe_ruchy = dict()
        if self.aktywny_kolor == 'bialy':
            if 'bialy' in self.plansza['zbite']:
                ruchy = []
                for ruch in pozostale_ruchy:
                    if 0 < 25-ruch < 25:
                        dokad = 25-ruch
                        pole_dokad = 'pole_' + str(dokad)
                        if 'bialy' in self.plansza[pole_dokad] or not self.plansza[pole_dokad] or len(self.plansza[pole_dokad]) == 1:
                            ruchy.append(ruch)
                if ruchy:
                    mozliwe_ruchy[0] = ruchy
            else:
                for pole, wartosc in self.plansza.items():
                    if numer_pola_dom > 7 and 'bialy' in wartosc:
                        sciaganie = 0
                    numer_pola_dom += 1
                for pole, wartosc in self.plansza.items():
                    ruchy = []
                    if 'bialy' in wartosc:
                        for ruch in pozostale_ruchy:
                            if numer_pola - ruch > 0 and numer_pola - ruch < 25:
                                dokad = numer_pola - ruch
                                pole_dokad = 'pole_'+str(dokad)
                                if 'bialy' in self.plansza[pole_dokad] or not self.plansza[pole_dokad] or len(self.plansza[pole_dokad]) == 1:
                                    ruchy.append(dokad)
                            if sciaganie and numer_pola - ruch == 0:
                                ruchy.append('x')
                    if ruchy:
                        mozliwe_ruchy[numer_pola] = ruchy
                    numer_pola += 1
        elif self.aktywny_kolor == 'bordo':
            if 'bordo' in self.plansza['zbite']:
                ruchy = []
                for ruch in pozostale_ruchy:
                    if 0 < ruch < 25:
                        pole_dokad = 'pole_' + str(ruch)
                        if 'bordo' in self.plansza[pole_dokad] or not self.plansza[pole_dokad] or len(self.plansza[pole_dokad]) == 1:
                            ruchy.append(ruch)
                if ruchy:
                    mozliwe_ruchy[0] = ruchy
            else:
                for pole, wartosc in self.plansza.items():
                    if numer_pola_dom < 19 and 'bordo' in wartosc:
                        sciaganie = 0
                    numer_pola_dom += 1
                for pole, wartosc in self.plansza.items():
                    ruchy = []
                    if 'bordo' in wartosc:
                        for ruch in pozostale_ruchy:
                            if numer_pola + ruch > 0 and numer_pola + ruch < 25:
                                dokad = numer_pola + ruch
                                pole_dokad = 'pole_'+str(dokad)
                                if 'bordo' in self.plansza[pole_dokad] or not self.plansza[pole_dokad] or len(self.plansza[pole_dokad]) == 1:
                                    ruchy.append(dokad)
                            if sciaganie and numer_pola + ruch == 25:
                                    ruchy.append('x')
                    if ruchy:
                        mozliwe_ruchy[numer_pola] = ruchy
                    numer_pola += 1
        return mozliwe_ruchy


    def ruch(self, skad, dokad):
        """Wykonuje ruch na podstawie przekazanych wartości pól"""
        mozliwe_ruchy = self.znajdz_mozliwe_ruchy()
        sciaganie = 1
        wygrana = 1
        numer_pola_dom = 1
        if not mozliwe_ruchy:
            self.koniec_kolejki()
            return "Użytkownik nie miał żadnych możliwych ruchów. Następna kolejka."
        else:
            if int(skad) == 0:
                skad_pole = 'zbite'
            else:
                skad_pole = 'pole_' + str(skad)
            dokad_pole = 'pole_' + str(dokad)
            pozostale_ruchy = self.znajdz_pozostale_ruchy()

            if self.aktywny_kolor == 'bordo':
                for pole, wartosc in self.plansza.items():
                    if 'bordo' in wartosc:
                        wygrana = 0
                    if numer_pola_dom < 19 and 'bordo' in wartosc:
                        sciaganie = 0
                    numer_pola_dom += 1
                if wygrana:
                    return "Wygrał bordowy!"
                if sciaganie and dokad == 'x' and 'bordo' in self.plansza[skad_pole] and 25-int(skad) in pozostale_ruchy:
                    self.plansza[skad_pole].pop()
                    self.usun_wykorzystany_ruch(25-int(skad))
                    return
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
                            for pole, wartosc in self.plansza.items():
                                if 'bialy' in wartosc:
                                    wygrana = 0
                                if numer_pola_dom > 6 and 'bialy' in wartosc:
                                    sciaganie = 0
                                numer_pola_dom += 1
                            if wygrana:
                                return "Wygrał biały!"
                            if sciaganie and dokad == 'x' and 'bialy' in self.plansza[skad_pole] and int(skad) in pozostale_ruchy:
                                self.plansza[skad_pole].pop()
                                self.usun_wykorzystany_ruch(int(skad))
                                return
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

    def wykonaj_ruch_komputera(self, skad_pole, dokad_pole, wartosc_ruchu):
        if dokad_pole == 'x' or dokad_pole == 'pole_x':
            self.plansza[skad_pole].pop()
            self.usun_wykorzystany_ruch(wartosc_ruchu)
        else:
            self.plansza[dokad_pole].append('bialy')
            self.plansza[skad_pole].pop()
            self.usun_wykorzystany_ruch(wartosc_ruchu)

    def ruch_komputera(self):
        mozliwe_ruchy = self.znajdz_mozliwe_ruchy()
        if not mozliwe_ruchy:
            self.koniec_kolejki()
            return "Użytkownik nie miał żadnych możliwych ruchów. Następna kolejka."
        else:
            numer_pola = 1
            ewentualne_ruchy = dict()
            if 0 in mozliwe_ruchy:
                for ruch in mozliwe_ruchy[0]:
                    dokad_pole = 'pole_' + str(25 - ruch)
                    if 'bialy' in self.plansza[dokad_pole] or len(self.plansza[dokad_pole]) == 1:
                        if 'bordo' in self.plansza[dokad_pole] and len(self.plansza[dokad_pole]) == 1:
                            self.zbij_pionek(dokad_pole)
                        self.wykonaj_ruch_komputera('zbite', dokad_pole, ruch)
                        return "Komputer ściągnął zbity pionek na pole %d" % (ruch)
                    else:
                        ewentualne_ruchy[0] = 25-ruch
                    if ewentualne_ruchy:
                        dokad_pole = 'pole_' + str(ewentualne_ruchy[0])
                        skad_pole = 'zbite'
                        if 'bordo' in self.plansza[dokad_pole] and len(self.plansza[dokad_pole]) == 1:
                            self.zbij_pionek(dokad_pole)
                        self.wykonaj_ruch_komputera(skad_pole, dokad_pole, ruch)
                        return "Komputer ściągnął zbity pionek na pole %d" % (ruch)
            if 24 in mozliwe_ruchy or 23 in mozliwe_ruchy or 22 in mozliwe_ruchy or 21 in mozliwe_ruchy or 20 in mozliwe_ruchy or 19 in mozliwe_ruchy:
                for pionek, ruchy in mozliwe_ruchy.items():
                    if pionek == 24 or pionek == 23 or pionek == 22 or pionek == 21 or pionek == 20 or pionek == 19:
                        for ruch in ruchy:
                            dokad_pole = 'pole_'+str(ruch)
                            skad_pole = 'pole_'+str(pionek)
                            if len(self.plansza[skad_pole]) != 2 and 'bialy' in self.plansza[dokad_pole] or len(self.plansza[dokad_pole]) == 1:
                                if 'bordo' in self.plansza[dokad_pole] and len(self.plansza[dokad_pole]) == 1:
                                    self.zbij_pionek(dokad_pole)
                                wartosc_ruchu = pionek - ruch
                                self.wykonaj_ruch_komputera(skad_pole, dokad_pole, wartosc_ruchu)
                                return "Pierwszy Komputer wykonał ruch z pola %d na pole %d" % (pionek, ruch)
                            else:
                                ewentualne_ruchy[pionek] = ruch
                        if ewentualne_ruchy:
                            for pionek, ruch in ewentualne_ruchy.items():
                                if ruchy:
                                    dokad_pole = 'pole_' + str(ruch)
                                    skad_pole = 'pole_' + str(pionek)
                                    if 'bordo' in self.plansza[dokad_pole] and len(self.plansza[dokad_pole]) == 1:
                                        self.zbij_pionek(dokad_pole)
                                    wartosc_ruchu = pionek - ruch
                                    self.wykonaj_ruch_komputera(skad_pole, dokad_pole, wartosc_ruchu)
                                    return "Komputer wykonał ruch z pola %d na pole %d" % (pionek, ruch)
            for pole, wartosc in self.plansza.items():
                if 'bialy' in wartosc and len(self.plansza[pole]) == 1:
                    if numer_pola in mozliwe_ruchy:
                        ruchy = mozliwe_ruchy[numer_pola]
                        for ruch in ruchy:
                            dokad_pole = 'pole_' + str(ruch)
                            if 'bialy' in self.plansza[dokad_pole] or 'bordo' in self.plansza[dokad_pole] and len(self.plansza[dokad_pole]) == 1:
                                skad_pole = 'pole_' + str(numer_pola)
                                if 'bordo' in self.plansza[dokad_pole] and len(self.plansza[dokad_pole]) == 1:
                                    self.zbij_pionek(dokad_pole)
                                wartosc_ruchu = numer_pola - ruch
                                self.wykonaj_ruch_komputera(skad_pole, dokad_pole, wartosc_ruchu)
                                return
            for pionek, ruchy in mozliwe_ruchy.items():
                if ruchy:
                    dokad_pole = 'pole_' + str(ruchy[0])
                    skad_pole = 'pole_' + str(pionek)
                    if 'bordo' in self.plansza[dokad_pole] and len(self.plansza[dokad_pole]) == 1:
                        self.zbij_pionek(dokad_pole)
                    wartosc_ruchu = pionek-ruchy[0]
                    self.wykonaj_ruch_komputera(skad_pole, dokad_pole, wartosc_ruchu)
                    return "Komputer wykonał ruch z pola %d na pole %d" % (pionek, ruchy[0])


        def ruch_komp(self):
            mozliwe_ruchy = self.znajdz_mozliwe_ruchy()
            for pionek, ruchy in mozliwe_ruchy.items():
                if ruchy:
                    dokad_pole = 'pole_' + str(ruchy[0])
                    skad_pole = 'pole_' + str(pionek)
                    self.plansza[dokad_pole].append('bialy')
                    self.plansza[skad_pole].pop()
                    wartosc_ruchu = pionek-ruchy[0]
                    self.usun_wykorzystany_ruch(wartosc_ruchu)
                    return "Komputer wykonał ruch z pola %d na pole %d" % (pionek, ruchy[0])


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
        komunikaty = gra.ruch_komputera()
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
from flask import render_template, request
from collections import OrderedDict
from tryktrak import app
import pickle, random

def rzut_kostka():
    ruchy = []
    ruchy.append(random.randint(1,6))
    ruchy.append(random.randint(1,6))
    if ruchy[0] == ruchy[1]:
        ruchy.append(ruchy[0])
        ruchy.append(ruchy[0])
    return ruchy

class Plansza:
    def __init__(self, typ_gry):
        self.typ_gry = typ_gry
        self.stan = OrderedDict()
        for x in range(24):
            numer = x+1
            klucz = 'pole_'+str(numer)
            self.stan[klucz] = []
        self.stan['pole_1'] = ['bordo', 'bordo']
        self.stan['pole_6'] = ['bialy', 'bialy', 'bialy', 'bialy', 'bialy']
        self.stan['pole_8'] = ['bialy', 'bialy', 'bialy']
        self.stan['pole_12'] = ['bordo', 'bordo', 'bordo', 'bordo', 'bordo']
        self.stan['pole_13'] = ['bialy', 'bialy', 'bialy', 'bialy', 'bialy']
        self.stan['pole_17'] = ['bordo', 'bordo', 'bordo']
        self.stan['pole_19'] = ['bordo', 'bordo', 'bordo', 'bordo', 'bordo']
        self.stan['pole_24'] = ['bialy', 'bialy']

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/gra')
def gra():
    plansza = Plansza(request.values['typ_gry'])

    with open('zapis.pickle', 'wb') as handle:
        pickle.dump(plansza, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return render_template('gra.html', ruchy = rzut_kostka(), typ_gry=plansza.typ_gry,  stan_gry = plansza.stan)


@app.route('/ruch')
def ruch():
    with open('zapis.pickle', 'rb') as handle:
        plansza = pickle.load(handle)

    skad = 'pole_'+str(request.values['pionek'])
    dokad = 'pole_'+str(request.values['pole'])
    if 'bordo' in plansza.stan[skad]:
        plansza.stan[dokad].append('bordo')
    elif 'bialy' in plansza.stan[skad]:
        plansza.stan[dokad].append('bialy')
    plansza.stan[skad].pop()

    with open('zapis.pickle', 'wb') as handle:
        pickle.dump(plansza, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return render_template('ruch.html', ruchy = rzut_kostka(), typ_gry=plansza.typ_gry, stan_gry=plansza.stan)
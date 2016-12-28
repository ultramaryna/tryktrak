from flask import render_template, request
from collections import OrderedDict
from tryktrak import app
import random

def rzut_kostka():
    ruchy = []
    ruchy.append(random.randint(1,6))
    ruchy.append(random.randint(1,6))
    if ruchy[0] == ruchy[1]:
        ruchy.append(ruchy[0])
        ruchy.append(ruchy[0])
    return ruchy

def sciezki_kostek(ruchy):
    kostki = []
    pierwsza_kostka = '../static/' + str(ruchy[0]) + '.png'
    druga_kostka = '../static/' + str(ruchy[1]) + '.png'
    kostki.append(pierwsza_kostka)
    kostki.append(druga_kostka)
    return kostki

class Plansza:
    def __init__(self):
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
    plansza = Plansza()
    return render_template('gra.html', ruchy = rzut_kostka(), typ_gry=request.values['typ_gry'],  stan_gry = plansza.stan)

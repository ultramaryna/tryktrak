from flask import render_template, request
from collections import OrderedDict
from tryktrak import app
import random

def rzut_kostka():
    rzuty = []
    rzuty.append(random.randint(1,6))
    rzuty.append(random.randint(1,6))
    if rzuty[0] == rzuty[1]:
        rzuty.append(rzuty[0])
        rzuty.append(rzuty[0])
    return rzuty

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
    return render_template('gra.html', typ_gry=request.values['typ_gry'], rzuty = rzut_kostka(), stan_gry = plansza.stan)

from flask import render_template, request
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

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/gra')
def gra():
    return render_template('gra.html', typ_gry=request.values['typ_gry'], rzuty = rzut_kostka())

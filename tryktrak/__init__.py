from flask import Flask
 
app = Flask(__name__) 
from tryktrak import views
from tryktrak import plansza
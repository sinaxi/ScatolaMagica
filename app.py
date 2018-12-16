#!/usr/bin/env python
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import requests
import pymysql
import random
from datetime import date, timedelta
#from bs4 import BeautifulSoup
import string
import pandas as pd


app = Flask(__name__)

class Database:
    def __init__(self):
        host = "77.104.184.16"
        user = "bootep_mainuser"
        password = "bootep@123"
        db = "bootep_stories"

        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def list_info(self):
        self.cur.execute("SELECT id, title, story, publishdate, author FROM bootep_stories.stories;")
        result = self.cur.fetchall()

        return result

ask = Ask(app, '/')

def get_story():
    return "This is just a demo..Database yet to be linked with the application...If you hear this then things are working fine as of now"

@app.route('/')
def homepage():
    return 'Welcome to the Bootep Application'

@ask.launch
def start_skill():
    message = 'Ciao... Benvenuto nella Scatola Magica ...vuoi ascoltare una fiaba?'
    return question(message)

@ask.intent("YesIntent")
def yes_Intent():
    message = 'Dimmi se vuoi sentire la fiaba di oggi ...oppure pronuncia la parola TITOLO seguita dal titolo della fiaba che vuoi ascoltare'
    return question(message)

@ask.intent("DateIntent")
def date_Intent(date):
    message = 'Ecco la fiaba per te....'
    story_found = False
    db = Database()
    res = db.list_info()
    story = 'Spiacente non ho trovato nessuna fiaba'
    for entry in res:
        tstr = str(entry['publishdate'])
        tstr = tstr[:10] 
        if tstr == str(date):
            story_found = True
            story = entry['story']
    endtext = "....Dimmi se vuoi sentire la fiaba di oggi ...oppure pronuncia la parola TITOLO seguita dal titolo della fiaba che vuoi ascoltare"
    if story_found:
        message = message + story + endtext
    else:
        message = story + endtext
    return question(message)

@ask.intent("NumberIntent")
def number_Intent(number):
    message = 'Ecco la fiaba per te....'
    story_found = False
    db = Database()
    res = db.list_info()
    dat = date.today() - timedelta(days = int(number))
    story = 'Spiacente non ho trovato nessuna fiaba'
    for entry in res:
        tstr = str(entry['publishdate'])
        tstr = tstr[:10] 
        if tstr == str(dat):
            story_found = True
            story = entry['story']
    endtext = ".....Dimmi se vuoi sentire la fiaba di oggi ...oppure pronuncia la parola TITOLO seguita dal titolo della fiaba che vuoi ascoltare"
    if story_found:
        message = message + story + endtext
    else:
        message = story + endtext
    return question(message)

@ask.intent("SearchIntent")
def search_Intent(keyword):
    message = 'Ecco la fiaba per te....'
    story_found = False
    db = Database()
    res = db.list_info()
    story = 'Spiacente non ho trovato nessuna fiaba'
    tstr = ""
    for entry in res:
        tstr = entry['title']
        tx = str(keyword)
        if  tx == "3 porcellini":
            tx = "tre porcellini"
        if tstr.lower() == tx:
            story_found = True
            story = entry['story']
    endtext = "......Dimmi se vuoi sentire la fiaba di oggi ...oppure pronuncia la parola TITOLO seguita dal titolo della fiaba che vuoi ascoltare"
    if story_found:
        message = message + story + endtext
    else:
        message = story + endtext
    return question(message)

@ask.intent("RandomIntent")
def random_Intent():
    message = 'Ecco la fiaba per te....'
    db = Database()
    res = db.list_info()
    y = len(res)
    x = random.randint(0,y-1)
    story = res[x]['story']
    endtext = "....Dimmi se vuoi sentire la fiaba di oggi ...oppure pronuncia la parola TITOLO seguita dal titolo della fiaba che vuoi ascoltare"
    message = message + story + endtext
    return question(message)


@ask.intent("NoIntent")
def no_Intent():
    message = 'Bene, sarà per la prossima volta'
    return statement(message)

@ask.intent("AMAZON.CancelIntent")
def cancel_Intent():
    message = 'A presto!'
    return statement(message)

@ask.intent("AMAZON.StopIntent")
def stop_Intent():
    message = 'A presto!'
    return statement(message)

@ask.intent("AMAZON.HelpIntent")
def help_Intent():
    message = 'Pronuncia la parola Si pe ascoltare una fiaba, dopo prununcia il titolo...'
    return question(message)

if __name__ == '__main__':
    app.run(debug = True)

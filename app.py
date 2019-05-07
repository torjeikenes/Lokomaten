from flask import Flask, render_template, request, make_response, redirect
from forms import LokForm
import sys
import csv
import datetime
import operator
import os


path = '/home/lokomaten/mysite/troops/'
#path = '/home/torje/github/lokomat/troops/'

def pastWeeks(d, uke):
    weeks = {}
    for i in range(1, uke):
        ukas = ukasLok(d,i)
        #lok = max(ukas.items(), key=operator.itemgetter(1))[0]
        try:
            lok = max(ukas, key=lambda k: ukas[k])
            weeks[i] = lok
        except ValueError:
            print("No submissions", file=sys.stdout)
    return weeks

def findNavn(d,navn):
    streker = []
    for i in d:
        if i['navn'] == navn:
            streker.append(i)
    return streker

def ukasLok(d, week):
    ukas = {}
    for i in d:
        uke = int(datetime.datetime.strptime(i['dato'], '%Y-%m-%d').strftime("%V"))
        if uke == week:
            if i['navn'] in ukas:
                ukas[i['navn']] += int(i['antall'])
            else:
                ukas[i['navn']] = int(i['antall'])
    return ukas


def ukasStreker(d, week):
    streker = []
    for i in d:
        uke = int(datetime.datetime.strptime(i['dato'], '%Y-%m-%d').strftime("%V"))
        if uke == week:
            streker.append(i)
    return streker


def readFile(file):
    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
        return data

def findTotal(d):
    total = {}
    for i in d:
        # print(i['navn'], file=sys.stdout)
        if i['navn'] in total:
            total[i['navn']] += int(i['antall'])
        else:
            total[i['navn']] = int(i['antall'])
    return total


def writeToFile(tropp, navn,antall,forkl,dato):
    with open(path+tropp+'.csv', mode='a') as lok_file:
        fieldnames = ['navn', 'antall', 'forklaring', 'dato']
        lok_writer = csv.DictWriter(lok_file, fieldnames=fieldnames)
        row = {'navn': navn, 'antall': antall,'forklaring': forkl,'dato': dato}
        #row = {'navn': 'torge', 'antall': 2,'forklaring': 'sgsdsdfsdf','dato': '2019-03-04'}
        lok_writer.writerow(row)
    lok_file.close()

def findTroops():
    troops = []
    for file in os.listdir(path):
        troops.append(os.path.splitext(file)[0])
    # print(troops, file=sys.stdout)
    return troops



def lokTropp():
    troops = {}
    for file in os.listdir(path):
        troop = os.path.splitext(file)[0]
        data=readFile(path+file)
        troops[troop] = 0
        for i in data:
            troops[troop] += int(i['antall'])
    # print(troops, file=sys.stdout)
    return troops

def topLok():
    total = {}
    for file in os.listdir(path):
        troop = os.path.splitext(file)[0]
        data=readFile(path+file)
        total.update(findTotal(data))
    return total

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hemmelig'


@app.route('/')
def index():
    tropp = lokTropp()
    stropp = sorted(tropp.items(), reverse=True, key=operator.itemgetter(1))
    troops = findTroops()
    lok =  topLok()
    sl = sorted(lok.items(), reverse=True, key=operator.itemgetter(1))
    return render_template('start.html', lok=sl, troops=troops, tropp=stropp)

@app.route('/<tropp>')
def tropp(tropp):
    data = readFile(path+tropp+'.csv')
    total = findTotal(data)
    stotal = sorted(total.items(), reverse=True, key=operator.itemgetter(1))
    thisWeek = int(datetime.datetime.now().strftime("%V"))
    ukas = ukasLok(data, thisWeek)
    sukas = sorted(ukas.items(), reverse=True, key=operator.itemgetter(1))
    past = pastWeeks(data, thisWeek)
    return render_template('index.html', r=reversed(data), data=data,
                           total=stotal, ukas=sukas, past=past, tropp=tropp)

@app.route('/<tropp>/<navn>')
def navn(tropp,navn):
    data = readFile(path+tropp+'.csv')
    streker = findNavn(data, navn)
    totalt = findTotal(streker)[navn]
    return render_template('navn.html', navn=navn, streker=reversed(streker), totalt=totalt)

@app.route('/<tropp>/uke/<ukeNr>')
def uke(tropp, ukeNr):
    data = readFile(path+tropp+'.csv')
    ukas = ukasLok(data, int(ukeNr))
    streker = reversed(ukasStreker(data, int(ukeNr)))
    return render_template('uke.html',ukas=ukas, ukeNr=ukeNr, streker=streker)

@app.route('/<tropp>/submit', methods=['GET', 'POST'])
def submit(tropp):
    form = LokForm()
    #if form.validate_on_submit():
    if request.method == 'POST':
        navn = form.navn.data
        forklaring = form.forklaring.data
        lokstreker = form.lokstreker.data
        dato = form.dato.data
        writeToFile(tropp,navn,lokstreker,forklaring,dato)
        return redirect('/'+tropp)

    return render_template('submit.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)

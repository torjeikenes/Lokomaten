from flask import Flask, render_template, request, make_response, redirect
from forms import LokForm
import sys
import csv
import datetime
import operator

svarfil = '/home/lokomaten/mysite/svar.csv'

def pastWeeks(d, uke):
    weeks = {}
    for i in range(5, uke):
        ukas = ukasLok(d,i)
        #lok = max(ukas.items(), key=operator.itemgetter(1))[0]
        lok = max(ukas, key=lambda k: ukas[k])
        weeks[i] = lok

    return weeks

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
        if i['navn'] in total:
            total[i['navn']] += int(i['antall'])
        else:
            total[i['navn']] = int(i['antall'])
    return total


def writeToFile(navn,antall,forkl,dato):
    with open(svarfil, mode='a') as lok_file:
        fieldnames = ['navn', 'antall', 'forklaring', 'dato']
        lok_writer = csv.DictWriter(lok_file, fieldnames=fieldnames)
        row = {'navn': navn, 'antall': antall,'forklaring': forkl,'dato': dato}
        #row = {'navn': 'torge', 'antall': 2,'forklaring': 'sgsdsdfsdf','dato': '2019-03-04'}
        lok_writer.writerow(row)
    lok_file.close()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hemmelig'

@app.route('/')
def index():
    data = readFile(svarfil)
    total = findTotal(data)
    thisWeek = int(datetime.datetime.now().strftime("%V"))
    ukas = ukasLok(data, thisWeek)
    past = pastWeeks(data, thisWeek)
    return render_template('index.html', r=reversed(data), data=data, total=total, ukas=ukas, past=past)

@app.route('/uke/<ukeNr>')
def uke(ukeNr):
    data = readFile(svarfil)
    ukas = ukasLok(data, int(ukeNr))
    streker = reversed(ukasStreker(data, int(ukeNr)))
    return render_template('uke.html',ukas=ukas, ukeNr=ukeNr, streker=streker)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = LokForm()
    #if form.validate_on_submit():
    if request.method == 'POST':
        navn = form.navn.data
        forklaring = form.forklaring.data
        lokstreker = form.lokstreker.data
        dato = form.dato.data
        writeToFile(navn,lokstreker,forklaring,dato)
        return redirect('/')

    return render_template('submit.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)

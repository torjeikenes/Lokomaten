

from flask import Flask, render_template, request, make_response, redirect
from forms import LokForm
import sys
import csv


def writeToFile(navn,antall,forkl,dato):
    with open('svar.csv', mode='a') as lok_file:
        lok_writer = csv.writer(lok_file, delimiter=',')
        row = [navn, antall, forkl, dato]
        lok_writer.writerow(row)
    lok_file.close()




app = Flask(__name__)
app.config['SECRET_KEY'] = 'hemmelig'


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

        print(navn, file=sys.stdout)
        print(lokstreker, file=sys.stdout)
        print(dato, file=sys.stdout)
        print(forklaring, file=sys.stdout)
    return render_template('submit.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)

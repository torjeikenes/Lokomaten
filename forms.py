from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import RadioField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
import datetime

class LokForm(FlaskForm):
    navn = StringField('Navn', validators=[DataRequired()])
    lokstreker = RadioField('Løkstreker',
                            choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('10','Superløk (10)'),('20','Megaløk (20)')],
                            default='1',
                            validators=[DataRequired()])
    forklaring = StringField('Forklaring',
                             validators=[DataRequired()])
    dato = DateField('Dato',
                     format='%Y-%m-%d',
                     default=datetime.datetime.today,
                     validators=[DataRequired()])

    submit = SubmitField('Send inn')

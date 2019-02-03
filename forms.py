from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import RadioField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

class LokForm(FlaskForm):
    navn = StringField('Navn', validators=[DataRequired()])
    lokstreker = RadioField('Løkstreker', choices=[('1','1'),('2','2'),('3','3')], validators=[DataRequired()])
    forklaring = StringField('Forklaring', validators=[DataRequired()])
    dato = DateField('Dato', format='%Y-%m-%d', validators=[DataRequired()])

    submit = SubmitField('Send inn')

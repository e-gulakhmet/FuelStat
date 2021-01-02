from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import DateField, SelectMultipleField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired
from datetime import date


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember")
    submit = SubmitField('Sign In')


class NavigationForm(FlaskForm):
    start_date = DateField("Start Date", default=date(1000, 1, 1))
    end_date = DateField("End Date", default=date(9000, 12, 31))
    names = SelectMultipleField("Stations Names")
    allow = SubmitField("Allow")
    

class TableRowForm(FlaskForm):
    id = IntegerField("Id")
    date = DateField("Date")
    odometer = IntegerField("Odometer")
    fuel_station = SelectField("Station")
    gallon_count = FloatField("Gallons")
    allow = SubmitField("Allow")

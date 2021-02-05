from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import DateField, SelectMultipleField, IntegerField, FloatField, SelectField
from datetime import date


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    remember = BooleanField("Remember")
    submit = SubmitField('Sign In')


class NavigationTransForm(FlaskForm):
    start_date = DateField("Start Date", default=date(1000, 1, 1))
    end_date = DateField("End Date", default=date(9000, 12, 31))
    start_odometer = IntegerField("Start Odometer", default=1)                             
    end_odometer = IntegerField("End Odometer", default=1000000)
    names = SelectMultipleField("Stations Names")
    trans_allow = SubmitField("Allow")


class NavigationFuelForm(FlaskForm):
    start_price = IntegerField("Start Price", default=0)
    end_price = IntegerField("End Price", default=1000)
    fuel_allow = SubmitField("Allow")


class TransTableRowForm(FlaskForm):
    id = IntegerField("id")
    date = DateField("Date")
    odometer = IntegerField("Odometer")
    fuel_station = SelectField("Station", validate_choice=False)
    gallon_count = FloatField("Gallons")
    save_trans = SubmitField("Save")
    delete_trans = SubmitField("Delete")


class TransTableNewRowForm(FlaskForm):
    date = DateField("Date")
    odometer = IntegerField("Odometer")
    fuel_station = SelectField("Station", validate_choice=False)
    gallon_count = FloatField("Gallons")
    add_trans = SubmitField("Add")


class FuelTableRowForm(FlaskForm):
    id = IntegerField("id")
    name = StringField("Name")
    price = StringField("Price")
    save_fuel = SubmitField("Save")
    delete_fuel = SubmitField("Delete")


class FuelTableNewRowForm(FlaskForm):
    name = StringField("Name")
    price = StringField("Price")
    add_fuel = SubmitField("Add")


class ReportForm(FlaskForm):
    start_date = DateField("Start Date", default=date(1000, 1, 1), format='%Y-%m-%d')
    end_date = DateField("End Date", default=date(9000, 12, 31), format='%Y-%m-%d')
    start_odometer = IntegerField("Start Odometer", default=1)                            
    end_odometer = IntegerField("End Odometer", default=1000000)
    names = SelectMultipleField("Stations Names")
    show_table = BooleanField("Show Table", default=True)
    show_statistic = BooleanField("Show Statistic", default=True)
    get_report = SubmitField("Get Report")
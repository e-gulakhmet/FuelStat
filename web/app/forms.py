from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import DateField, SelectMultipleField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, ValidationError, Length, InputRequired
from datetime import date
import sqlite3


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

    # def validate_start_date(form, field):
    #     if field.data > form.end_date.data:
    #         raise ValidationError("Start date must be less than end date")

    # def validate_end_date(form, field):
    #     if field.data < form.start_date.data:
    #         raise ValidationError("End date must be greater than start date")

    # def validate_start_odometer(form, field):
    #     if field.data < form.end_odometer.data:
    #         raise ValidationError("Start odometer must be less than end odometer")
    
    # def validate_end_odometer(form, field):
    #     if field.data > form.start_odometer.data:
    #         raise ValidationError("End odometer must be greater than start odometer")


class NavigationFuelForm(FlaskForm):
    start_price = IntegerField("Start Price", default=0)
    end_price = IntegerField("End Price", default=1000)
    fuel_allow = SubmitField("Allow")


class TransTableRowForm(FlaskForm):
    id = IntegerField("id")
    date = DateField("Date", format='%Y-%m-%d')
    odometer = IntegerField("Odometer")
    fuel_station = SelectField("Station")
    gallon_count = FloatField("Gallons")
    save_trans = SubmitField("Save")
    delete_trans = SubmitField("Delete")


class TransTableNewRowForm(FlaskForm):
    date = DateField("Date")
    odometer = IntegerField("Odometer")
    fuel_station = SelectField("Station")
    gallon_count = FloatField("Gallons")
    add_trans = SubmitField("Add")
    
    # def validate_odometer(form, field):
    #     db = sqlite3.connect("../data/database.db")
    #     min_value = list(db.execute("SELECT MAX(odometer) FROM trans WHERE dtime <= '" + str(form.date.data) + "'"))[0][0]
    #     max_value = list(db.execute("SELECT MIN(odometer) FROM trans WHERE dtime >= '" + str(form.date.data) + "'"))[0][0]
    #     print(min_value)
    #     print(max_value)
    #     if field.data < int(min_value):
    #         raise ValidationError("Odometer must be greater than " + str(min_value))
    #     if field.data > int(max_value):
    #         raise ValidationError("Odometer must be less than " + str(max_value))


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

    # def validate_start_date(form, field):
    #     if field.data < form.start_date.data:
    #         raise ValidationError("Start date must be less than end date")

    # def validate_end_date(form, field):
    #     if field.data < form.start_date.data:
    #         raise ValidationError("End date must be greater than start date")
    
    # def validate_start_odometer(form, field):
    #     if field.data < form.end_odometer.data:
    #         raise ValidationError("Start odometer must be less than end odometer")
    
    # def validate_end_odometer(form, field):
    #     if field.data > form.start_odometer.data:
    #         raise ValidationError("End odometer must be greater than start odometer")
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import DateField, SelectMultipleField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, ValidationError
from datetime import date
import sqlite3


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("FUCK")])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember")
    submit = SubmitField('Sign In')


class NavigationTransForm(FlaskForm):
    start_date = DateField("Start Date", default=date(1000, 1, 1),
                           validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField("End Date", default=date(9000, 12, 31),
                         validators=[DataRequired()], format='%Y-%m-%d')
    names = SelectMultipleField("Stations Names",
                                validators=[DataRequired()])
    allow = SubmitField("Allow")

    def validate_start_date(form, field):
        if field.data < form.start_date.data:
            raise ValidationError("Start date must be less than end date")

    def validate_end_date(form, field):
        if field.data < form.start_date.data:
            raise ValidationError("End date must be greater than start date")


class NavigationFuelForm(FlaskForm):
    names = SelectMultipleField("Stations Names",
                                validators=[DataRequired()])
    start_price = IntegerField("Start Price", default=0, 
                               validators=[DataRequired()])
    end_price = IntegerField("Start Price", default=1000, 
                             validators=[DataRequired()])
    allow = SubmitField("Allow")


class TableRowForm(FlaskForm):
    id = IntegerField("Id")
    date = DateField("Date", validators=[DataRequired()], format='%Y-%m-%d')
    odometer = IntegerField("Odometer", validators=[DataRequired()])
    fuel_station = SelectField("Station", validators=[DataRequired()])
    gallon_count = FloatField("Gallons", validators=[DataRequired()])
    save = SubmitField("Save")
    delete = SubmitField("Delete")


class TableNewRowForm(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    odometer = IntegerField("Odometer", validators=[DataRequired()])
    fuel_station = SelectField("Station", validators=[DataRequired()])
    gallon_count = FloatField("Gallons", validators=[DataRequired()])
    add = SubmitField("Add")
    
    def validate_odometer(form, field):
        db = sqlite3.connect("../data/database.db")
        min_value = list(db.execute("SELECT MAX(odometer) FROM trans WHERE dtime <= '" + str(form.date.data) + "'"))[0][0]
        max_value = list(db.execute("SELECT MIN(odometer) FROM trans WHERE dtime >= '" + str(form.date.data) + "'"))[0][0]
        if field.data < min_value:
            raise ValidationError("Odometer must be greater than " + str(min_value))
        if field.data > max_value:
            raise ValidationError("Odometer must be less than " + str(max_value))


class WorkTableForm(FlaskForm):
    table_name = StringField("name", default="trans")
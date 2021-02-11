from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import DateField, SelectMultipleField, IntegerField, FloatField, SelectField, FileField
from wtforms.validators import DataRequired, ValidationError, Regexp
from datetime import date
import re
import logging

from app.database import DataBase


logger = logging.getLogger("FORMS")

db = DataBase(__file__.replace("web/app/forms.py", "data/database.db"))


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember")
    submit = SubmitField('Sign In')


class NavigationTransForm(FlaskForm):
    start_date_trans_navigation = DateField("Start Date", default=date(1000, 1, 1),
                           validators=[DataRequired()], format='%Y-%m-%d')
    end_date_trans_navigation = DateField("End Date", default=date(9000, 12, 31),
                         validators=[DataRequired()], format='%Y-%m-%d')
    start_odometer_trans_navigation = IntegerField("Start Odometer", default=1,
                                  validators=[DataRequired()])                             
    end_odometer_trans_navigation = IntegerField("End Odometer", default=1000000,
                                validators=[DataRequired()])
    names_trans_navigation = SelectMultipleField("Stations Names",
                                validators=[DataRequired()])
    allow_trans_navigation = SubmitField("Allow")

    def validate_start_date(form, field):
        if field.data > form.end_date.data:
            logger.warning("Start date more than end date, Navigation")
            raise ValidationError()
    
    def validate_end_date(form, field):
        if field.data < form.start_date.data:
            logger.warning("End date less than start date, Navigation")
            raise ValidationError()
    
    def validate_start_odometer(form, field):
        if field.data > form.end_odometer.data:
            logger.warning("Start odometer more than end odometer, Navigation")
            raise ValidationError()
    
    def validate_end_odometer(form, field):
        if field.data < form.start_odometer.data:
            logger.warning("End odometer less than start odometer, Navigation")
            raise ValidationError()


class NavigationFuelForm(FlaskForm):
    start_price_fuel_navigation = IntegerField("Start Price", default=0,
                               validators=[DataRequired()]) 
    end_price_fuel_navigation = IntegerField("End Price", default=1000,
                             validators=[DataRequired()])
    allow_fuel_navigation = SubmitField("Allow")

    def validate_start_price(form, field):
        if field.data > form.end_price.data:
            logger.warning("Start price more than end price, Navigation")
            raise ValidationError()
    
    def validate_end_price(form, field):
        if field.data < form.start_price.data:
            logger.warning("End price less than start price, Navigation")


class TransTableRowForm(FlaskForm):
    id_trans_row = IntegerField("id")
    date_trans_row = DateField("Date", validators=[DataRequired()])
    odometer_trans_row = IntegerField("Odometer", validators=[DataRequired()])
    fuel_station_trans_row = SelectField("Station", validate_choice=False)
    gallon_count_trans_row = FloatField("Gallons", validators=[DataRequired()])
    save_trans_row = SubmitField("Save")
    delete_trans_row = SubmitField("Delete")


class TransTableNewRowForm(FlaskForm):
    date_trans_new_row = DateField("Date", validators=[DataRequired()])
    odometer_trans_new_row = IntegerField("Odometer", validators=[DataRequired()])
    fuel_station_trans_new_row = SelectField("Station", validate_choice=False)
    gallon_count_trans_new_row = FloatField("Gallons")
    add_trans_new_row = SubmitField("Add")


class FuelTableRowForm(FlaskForm):
    id_fuel_row = IntegerField("id")
    name_fuel_row = StringField("Name", validators=[DataRequired()])
    price_fuel_row = StringField("Price", validators=[DataRequired()])
    save_fuel_row = SubmitField("Save")
    delete_fuel_row = SubmitField("Delete")


class FuelTableNewRowForm(FlaskForm):
    name_fuel_new_row = StringField("Name", validators=[DataRequired()])
    price_fuel_new_row = StringField("Price", validators=[DataRequired()])
    add_fuel_new_row = SubmitField("Add")


class ReportForm(FlaskForm):
    start_date_report = DateField("Start Date", default=date(1000, 1, 1),
                           format='%Y-%m-%d',
                           validators=[DataRequired(),
                                       Regexp("^\d{4}-\d{2}-\d{2}")])
    end_date_report = DateField("End Date", default=date(9000, 12, 31),
                         format='%Y-%m-%d',
                         validators=[DataRequired(),
                                     Regexp("^\d{4}-\d{2}-\d{2}")])
    start_odometer_report = IntegerField("Start Odometer", default=1,
                                  validators=[DataRequired(),
                                              Regexp("^\d*$")])                            
    end_odometer_report = IntegerField("End Odometer", default=1000000,
                                validators=[DataRequired(),
                                            Regexp("^\d*$")])
    names_report = SelectMultipleField("Stations Names")
    show_table_report = BooleanField("Show Table", default=True)
    show_statistic_report = BooleanField("Show Statistic", default=True)
    get_report = SubmitField("Get Report")

    def validate_start_date(form, field):
        print(form.validate())
        if field.data > form.end_date.data:
            logger.warning("Start date more than end date, Report")
            raise ValidationError()


    def validate_end_date(form, field):
        if field.data < form.start_date.data:
            logger.warning("End date less than start date, Report")
            raise ValidationError()

    
    def validate_start_odometer(form, field):
        if field.data > form.end_odometer.data:
            logger.warning("Start odometer more than end odometer, Report")
            raise ValidationError()
    
    def validate_end_odometer(form, field):
        if field.data < form.start_odometer.data:
            logger.warning("End odometer less than start odometer, Report")
            raise ValidationError()



class UploadTransForm(FlaskForm):
    file_trans = FileField('Upload File')
    method_trans = SelectField("Upload Method",
                               choices=[(0, "Add"),
                                        (1, "Replace")])
    upload_trans = SubmitField("Upload")

    def validate_file_trans(form, field):
        if field.data and re.search("^.*.csv$", str(field.data.filename)) is None:
            logger.warning("Invalid file extension: " + field.data.filename)
            raise ValueError("Invalid file extension")



class UploadFuelForm(FlaskForm):
    file_fuel = FileField('Upload File')
    method_fuel = SelectField("Upload Method",
                              choices=[(0, "Add"),
                                       (1, "Replace")])
    upload_fuel = SubmitField("Upload")

    def validate_file_fuel(form, field):
        if field.data and re.search("^.*.csv$", str(field.data.filename)) is None:
            logger.warning("Invalid file extension: " + field.data.filename)
            raise ValueError("Invalid file extension")

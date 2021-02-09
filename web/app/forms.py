from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import DateField, SelectMultipleField, IntegerField, FloatField, SelectField, FileField
from wtforms.validators import DataRequired, ValidationError
from datetime import date
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
    start_date = DateField("Start Date", default=date(1000, 1, 1),
                           validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField("End Date", default=date(9000, 12, 31),
                         validators=[DataRequired()], format='%Y-%m-%d')
    start_odometer = IntegerField("Start Odometer", default=1,
                                  validators=[DataRequired()])                             
    end_odometer = IntegerField("End Odometer", default=1000000,
                                validators=[DataRequired()])
    names = SelectMultipleField("Stations Names",
                                validators=[DataRequired()])
    trans_allow = SubmitField("Allow")

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
    start_price = IntegerField("Start Price", default=0,
                               validators=[DataRequired()]) 
    end_price = IntegerField("End Price", default=1000,
                             validators=[DataRequired()])
    fuel_allow = SubmitField("Allow")

    def validate_start_price(form, field):
        if field.data > form.end_price.data:
            logger.warning("Start price more than end price, Navigation")
            raise ValidationError()
    
    def validate_end_price(form, field):
        if field.data < form.start_price.data:
            logger.warning("End price less than start price, Navigation")


class TransTableRowForm(FlaskForm):
    id = IntegerField("id")
    date = DateField("Date", validators=[DataRequired()])
    odometer = IntegerField("Odometer", validators=[DataRequired()])
    fuel_station = SelectField("Station", validate_choice=False)
    gallon_count = FloatField("Gallons", validators=[DataRequired()])
    save_trans = SubmitField("Save")
    delete_trans = SubmitField("Delete")


class TransTableNewRowForm(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    odometer = IntegerField("Odometer", validators=[DataRequired()])
    fuel_station = SelectField("Station", validate_choice=False)
    gallon_count = FloatField("Gallons")
    add_trans = SubmitField("Add")


class FuelTableRowForm(FlaskForm):
    id = IntegerField("id")
    name = StringField("Name", validators=[DataRequired()])
    price = StringField("Price", validators=[DataRequired()])
    save_fuel = SubmitField("Save")
    delete_fuel = SubmitField("Delete")


class FuelTableNewRowForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    price = StringField("Price", validators=[DataRequired()])
    add_fuel = SubmitField("Add")


class ReportForm(FlaskForm):
    start_date = DateField("Start Date", default=date(1000, 1, 1),
                           format='%Y-%m-%d', validators=[DataRequired()])  
    end_date = DateField("End Date", default=date(9000, 12, 31),
                         format='%Y-%m-%d', validators=[DataRequired()])
    start_odometer = IntegerField("Start Odometer", default=1,
                                  validators=[DataRequired()])                            
    end_odometer = IntegerField("End Odometer", default=1000000,
                                validators=[DataRequired()])
    names = SelectMultipleField("Stations Names")
    show_table = BooleanField("Show Table", default=True)
    show_statistic = BooleanField("Show Statistic", default=True)
    get_report = SubmitField("Get Report")

    def validate_start_date(form, field):
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


class UploadFuelForm(FlaskForm):
    file_fuel = FileField('Upload File')
    method_fuel = SelectField("Upload Method",
                              choices=[(0, "Add"),
                                       (1, "Replace")])
    upload_fuel = SubmitField("Upload")

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import DateField, SelectMultipleField, IntegerField, FloatField, SelectField, FileField
from wtforms.validators import DataRequired, ValidationError, Regexp
from datetime import date
import logging
import re

from app.database import DataBase


logger = logging.getLogger('FORMS')

db = DataBase(__file__.replace('web/app/forms.py', 'data/database.db'))



def validate_value(form, field):
    if field.data is None:
        logger.warning("Invalid " + field.name)
        raise ValidationError("Invalid value")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), validate_value])
    password = PasswordField('Password', validators=[DataRequired(), validate_value])
    remember = BooleanField('Remember')
    submit = SubmitField('Sign In')


class NavigationTransForm(FlaskForm):
    start_date_trans_navigation = DateField('Start Date', default=date(1000, 1, 1),
                                            format='%Y-%m-%d',
                                            validators=[DataRequired(), validate_value])
    end_date_trans_navigation = DateField('End Date', default=date(9000, 12, 31),
                                          format='%Y-%m-%d',
                                          validators=[DataRequired(), validate_value])
    start_odometer_trans_navigation = IntegerField('Start Odometer', default=1,
                                                   validators=[DataRequired(), validate_value])                             
    end_odometer_trans_navigation = IntegerField('End Odometer', default=1000000,
                                                 validators=[DataRequired(), validate_value])
    names_trans_navigation = SelectMultipleField('Stations Names')
    allow_trans_navigation = SubmitField('Allow')

    def validate_start_date_trans_navigation(form, field):
        if field.data and form.end_date_trans_navigation.data and field.data > form.end_date_trans_navigation.data:
            logger.warning('Start date more than end date, Navigation')
            raise ValidationError("Start must be less than end date")
    
    def validate_end_date_trans_navigation(form, field):
        if field.data is None:
            logger.warning("Invalid end, Navigation")
            raise ValidationError("Invalid value")
        if field.data and form.start_date_trans_navigation.data and field.data < form.start_date_trans_navigation.data:
            logger.warning('End date less than start date, Navigation')
            raise ValidationError("End date must be more than start date")
    
    def validate_start_odometer_trans_navigation(form, field):
        if field.data is None:
            logger.warning("Invalid start odometer, Navigation")
            raise ValidationError("Invalid value")
        if field.data and form.end_odometer_trans_navigation.data and field.data > form.end_odometer_trans_navigation.data:
            logger.warning('Start odometer more than end odometer, Navigation')
            raise ValidationError("Start odometer must be less than end odometer")
    
    def validate_end_odometer_trans_navigation(form, field):
        if field.data is None:
            logger.warning("Invalid value, Navigation")
            raise ValidationError("Invalid value")
        if field.data and form.start_odometer_trans_navigation.data and field.data < form.start_odometer_trans_navigation.data:
            logger.warning('End odometer less than start odometer, Navigation')
            raise ValidationError("End odometer must be more than start odometer")


class NavigationFuelForm(FlaskForm):
    start_price_fuel_navigation = FloatField('Start Price', default=0,
                                             validators=[DataRequired(), validate_value]) 
    end_price_fuel_navigation = FloatField('End Price', default=1000,
                                           validators=[DataRequired(), validate_value])
    allow_fuel_navigation = SubmitField('Allow')

    def validate_start_price_fuel_navigation(form, field):
        if field.data is None:
            logger.warning("Invalid value, Navigation")
            raise ValidationError("Invalid value")
        if field.data and form.end_price_fuel_navigation.data and field.data > form.end_price_fuel_navigation.data:
            logger.warning('Start price more than end price, Navigation')
            raise ValidationError()
    
    def validate_end_price_fuel_navigation(form, field):
        if field.data and form.start_price_fuel_navigation.data and field.data < form.start_price_fuel_navigation.data:
            logger.warning('End price less than start price, Navigation')
            raise ValidationError()


class TransTableRowForm(FlaskForm):
    id_trans_row = IntegerField('id')
    date_trans_row = DateField('Date', format='%Y-%m-%d',
                               validators=[DataRequired(), validate_value])
    odometer_trans_row = IntegerField('Odometer',
                                      validators=[DataRequired(), validate_value]) 
    fuel_station_trans_row = SelectField('Station', validate_choice=False)
    gallon_count_trans_row = FloatField('Gallons',
                                        validators=[DataRequired(), validate_value])
    save_trans_row = SubmitField('Save')
    delete_trans_row = SubmitField('Delete')


class TransTableNewRowForm(FlaskForm):
    date_trans_new_row = DateField('Date', format='%Y-%m-%d',
                                   validators=[DataRequired(),
                                               validate_value,
                                               Regexp('^\d{4}-\d{2}-\d{2}$')])
    odometer_trans_new_row = IntegerField('Odometer',
                                          validators=[DataRequired(), validate_value]) 
    fuel_station_trans_new_row = SelectField('Station', validate_choice=False)
    gallon_count_trans_new_row = FloatField('Gallons',
                                            validators=[DataRequired(), validate_value])
    add_trans_new_row = SubmitField('Add')


class FuelTableRowForm(FlaskForm):
    id_fuel_row = IntegerField('id')
    name_fuel_row = StringField('Name', validators=[DataRequired(),
                                                    validate_value,
                                                    Regexp('^[A-Za-z]*$')])
    price_fuel_row = FloatField('Price', validators=[DataRequired(), validate_value])
    save_fuel_row = SubmitField('Save')
    delete_fuel_row = SubmitField('Delete')


class FuelTableNewRowForm(FlaskForm):
    name_fuel_new_row = StringField('Name', validators=[DataRequired(),
                                                        validate_value,
                                                        Regexp('^[A-Za-z]*$')])
    price_fuel_new_row = FloatField('Price', validators=[DataRequired(), validate_value])
    add_fuel_new_row = SubmitField('Add')


class ReportForm(FlaskForm):
    start_date_report = DateField('Start Date', default=date(1000, 1, 1),
                                  format='%Y-%m-%d',
                                  validators=[DataRequired(), validate_value])
    end_date_report = DateField('End Date', default=date(9000, 12, 31),
                                format='%Y-%m-%d',
                                validators=[DataRequired(), validate_value])
    start_odometer_report = IntegerField('Start Odometer', default=1,
                                         validators=[DataRequired(), validate_value])                            
    end_odometer_report = IntegerField('End Odometer', default=1000000,
                                       validators=[DataRequired(), validate_value])
    names_report = SelectMultipleField('Stations Names')
    show_table_report = BooleanField('Show Table', default=True)
    show_statistic_report = BooleanField('Show Statistic', default=True)
    get_report = SubmitField('Get Report')

    def validate_start_date_report(form, field):
        if field.data and form.end_date_report.data and field.data > form.end_date_report.data:
            logger.warning('Start date more than end date, Report')
            raise ValidationError()


    def validate_end_date_report(form, field):
        if field.data and form.start_date_report.data and field.data < form.start_date_report.data:
            logger.warning('End date less than start date, Report')
            raise ValidationError()

    
    def validate_start_odometer_report(form, field):
        if field.data and form.end_odometer_report.data and field.data > form.end_odometer_report.data:
            logger.warning('Start odometer more than end odometer, Report')
            raise ValidationError()
    
    def validate_end_odometer_report(form, field):
        if field.data and form.start_odometer_report.data and field.data < form.start_odometer_report.data:
            logger.warning('End odometer less than start odometer, Report')
            raise ValidationError()



class UploadTransForm(FlaskForm):
    file_trans = FileField('Upload File',
                           validators=[])
    method_trans = SelectField('Upload Method',
                               choices=[(0, 'Add'),
                                        (1, 'Replace')])
    upload_trans = SubmitField('Upload')

    def validate_file_trans(form, field):
        if field.data and re.search('^.*.csv$', str(field.data.filename)) is None:
            logger.warning("Invalid trans upload file format")
            raise ValidationError("Invalid format")


class UploadFuelForm(FlaskForm):
    file_fuel = FileField('Upload File',
                          validators=[])
    method_fuel = SelectField('Upload Method',
                              choices=[(0, 'Add'),
                                       (1, 'Replace')])
    upload_fuel = SubmitField('Upload')

    def validate_file_fuel(form, field):
        if field.data and re.search('^.*.csv$', str(field.data.filename)) is None:
            logger.warning("Invalid fuel upload file format")
            raise ValidationError("Invalid format")

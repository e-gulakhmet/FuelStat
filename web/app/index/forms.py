from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, BooleanField
from wtforms import DateField, IntegerField, FloatField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Regexp
from datetime import date
import logging

logger = logging.getLogger('INDEX_FORMS')


def validate_value(form, field):
    if field.data is None:
        logger.warning("Invalid " + field.name)
        raise ValidationError("Invalid value")


class NavigationTransForm(FlaskForm):
    start_date_trans_navigation = DateField('Start Date',
                                            default=date(1000, 1, 1),
                                            format='%Y-%m-%d',
                                            validators=[DataRequired(),
                                                        validate_value])
    end_date_trans_navigation = DateField('End Date',
                                          default=date(9000, 12, 31),
                                          format='%Y-%m-%d',
                                          validators=[DataRequired(),
                                                      validate_value])
    start_odometer_trans_navigation = IntegerField('Start Odometer',
                                                   default=1,
                                                   validators=[DataRequired(),
                                                               validate_value])                             
    end_odometer_trans_navigation = IntegerField('End Odometer',
                                                 default=1000000,
                                                 validators=[DataRequired(),
                                                             validate_value])
    names_trans_navigation = SelectMultipleField('Stations Names')
    allow_trans_navigation = SubmitField('Allow')

    def validate_start_date_trans_navigation(form, field):
        if field.data and form.end_date_trans_navigation.data and field.data > form.end_date_trans_navigation.data:
            logger.warning('Start date more than end date, Navigation')
            raise ValidationError("Start must be less than end date")
    
    def validate_end_date_trans_navigation(form, field):
        if field.data and form.start_date_trans_navigation.data and field.data < form.start_date_trans_navigation.data:
            logger.warning('End date less than start date, Navigation')
            raise ValidationError("End date must be more than start date")
    
    def validate_start_odometer_trans_navigation(form, field):
        if field.data and form.end_odometer_trans_navigation.data and field.data > form.end_odometer_trans_navigation.data:
            logger.warning('Start odometer more than end odometer, Navigation')
            raise ValidationError("Start odometer must be less than end odometer")
    
    def validate_end_odometer_trans_navigation(form, field):
        if field.data and form.start_odometer_trans_navigation.data and field.data < form.start_odometer_trans_navigation.data:
            logger.warning('End odometer less than start odometer, Navigation')
            raise ValidationError("End odometer must be more than start odometer")


class NavigationFuelForm(FlaskForm):
    start_price_fuel_navigation = FloatField('Start Price', default=10,
                                             validators=[DataRequired(),
                                                         validate_value]) 
    end_price_fuel_navigation = FloatField('End Price', default=1000,
                                           validators=[DataRequired(),
                                                       validate_value])
    allow_fuel_navigation = SubmitField('Allow')

    def validate_start_price_fuel_navigation(form, field):
        if field.data and form.end_price_fuel_navigation.data and field.data > form.end_price_fuel_navigation.data:
            logger.warning('Start price more than end price, Navigation')
            raise ValidationError('Start price must be less than end price')
    
    def validate_end_price_fuel_navigation(form, field):
        if field.data and form.start_price_fuel_navigation.data and field.data < form.start_price_fuel_navigation.data:
            logger.warning('End price less than start price, Navigation')
            raise ValidationError('End price must be more than start price')


class ReportForm(FlaskForm):
    start_date_report = DateField('Start Date',
                                  default=date(1000, 1, 1),
                                  format='%Y-%m-%d',
                                  validators=[DataRequired(),
                                              validate_value])
    end_date_report = DateField('End Date',
                                default=date(9000, 12, 31),
                                format='%Y-%m-%d',
                                validators=[DataRequired(),
                                            validate_value])
    start_odometer_report = IntegerField('Start Odometer',
                                         default=1,
                                         validators=[DataRequired(),
                                                     validate_value])                            
    end_odometer_report = IntegerField('End Odometer',
                                       default=1000000,
                                       validators=[DataRequired(),
                                                   validate_value])
    names_report = SelectMultipleField('Stations Names')
    show_table_report = BooleanField('Show Table', default=True)
    show_statistic_report = BooleanField('Show Statistic', default=True)
    get_report = SubmitField('Get Report')

    def validate_start_date_report(form, field):
        if field.data and form.end_date_report.data and field.data > form.end_date_report.data:
            logger.warning('Start date more than end date, Report')
            raise ValidationError("Start date must be less than end date")


    def validate_end_date_report(form, field):
        if field.data and form.start_date_report.data and field.data < form.start_date_report.data:
            logger.warning('End date less than start date, Report')
            raise ValidationError("End date must be more than start date")

    
    def validate_start_odometer_report(form, field):
        if field.data and form.end_odometer_report.data and field.data > form.end_odometer_report.data:
            logger.warning('Start odometer more than end odometer, Report')
            raise ValidationError("Start odometer must be less than end odometer")
    
    def validate_end_odometer_report(form, field):
        if field.data and form.start_odometer_report.data and field.data < form.start_odometer_report.data:
            logger.warning('End odometer less than start odometer, Report')
            raise ValidationError("End odometer must be more than start odometer")


class TransTableRowForm(FlaskForm):
    id_trans_row = StringField('id', default="-1")
    date_trans_row = DateField('Date', format='%Y-%m-%d',
                               default=date(1000, 1, 1),
                               validators=[DataRequired(),
                                           validate_value])
    odometer_trans_row = IntegerField('Odometer', default=10,
                                      validators=[DataRequired(),
                                                  validate_value]) 
    fuel_station_trans_row = SelectField('Station',
                                         validate_choice=False)
    gallon_count_trans_row = FloatField('Gallons', default=10.0,
                                        validators=[DataRequired(),
                                                    validate_value])
    save_trans_row = SubmitField('Save')
    delete_trans_row = SubmitField('Delete')


class TransTableNewRowForm(FlaskForm):
    date_trans_new_row = DateField('Date',
                                   format='%Y-%m-%d',
                                   default=date(1000, 1, 1),
                                   validators=[DataRequired(),
                                               validate_value])
    odometer_trans_new_row = IntegerField('Odometer',
                                          default=10,
                                          validators=[DataRequired(),
                                                      validate_value]) 
    fuel_station_trans_new_row = SelectField('Station',
                                             validate_choice=False)
    gallon_count_trans_new_row = FloatField('Gallons',
                                            default=10.0,
                                            validators=[DataRequired(),
                                                        validate_value])
    add_trans_new_row = SubmitField('Add')


class FuelTableRowForm(FlaskForm):
    id_fuel_row = StringField('id', default="-1")
    name_fuel_row = StringField('Name', default="Shell",
                                validators=[DataRequired(),
                                            validate_value,
                                            Regexp('^[A-Za-z]*$')])
    price_fuel_row = FloatField('Price', default=60.0,
                                validators=[DataRequired(),
                                            validate_value])
    save_fuel_row = SubmitField('Save')
    delete_fuel_row = SubmitField('Delete')


class FuelTableNewRowForm(FlaskForm):
    name_fuel_new_row = StringField('Name', default="Shell",
                                    validators=[DataRequired(),
                                                validate_value,
                                                Regexp('^[A-Za-z]*$')])
    price_fuel_new_row = FloatField('Price', default=60.0,
                                    validators=[DataRequired(),
                                                validate_value])
    add_fuel_new_row = SubmitField('Add')
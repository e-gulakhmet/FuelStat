from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import DateField, SelectMultipleField, IntegerField, FloatField, SelectField, FileField
from wtforms.validators import DataRequired, ValidationError
from datetime import date
import logging
import re

logger = logging.getLogger('FORMS')


def validate_value(form, field):
    if field.data is None:
        logger.warning("Invalid " + field.name)
        raise ValidationError("Invalid value")


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       validate_value])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         validate_value])
    remember = BooleanField('Remember')
    submit = SubmitField('Sign In')


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

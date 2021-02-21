from flask_wtf import FlaskForm
from wtforms import SelectField, FileField, SubmitField
from wtforms.validators import ValidationError
import logging
import re

logger = logging.getLogger('UPLOAD_FORMS')


def validate_value(form, field):
    if field.data is None:
        logger.warning("Invalid " + field.name)
        raise ValidationError("Invalid value")


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

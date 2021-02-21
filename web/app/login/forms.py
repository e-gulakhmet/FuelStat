from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError
import logging

logger = logging.getLogger('LOGIN_FORMS')


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

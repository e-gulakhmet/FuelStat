from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import DateField, SelectMultipleField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import date


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember")
    submit = SubmitField('Sign In')


class NavigationForm(FlaskForm):
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
    

class TableRowForm(FlaskForm):
    id = IntegerField("Id")
    date = DateField("Date", validators=[DataRequired()], format='%Y-%m-%d')
    odometer = IntegerField("Odometer", validators=[DataRequired()])
    fuel_station = SelectField("Station", validators=[DataRequired()])
    gallon_count = FloatField("Gallons", validators=[DataRequired()])
    save = SubmitField("Save")
    delete = SubmitField("Delete")
    add = SubmitField("Add")
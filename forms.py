from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField 
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    username = StringField('username', validators = [DataRequired(),
                                    Length(min = 5,max = 20)])
    password = PasswordField('password', validators = [DataRequired(),Length(min = 6,max = 20)])
    email = StringField('email', validators = [DataRequired(), Email()])
    role = SelectField('role',validators = [DataRequired()])
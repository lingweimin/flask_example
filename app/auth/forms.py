from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from app.models import User


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')


class RegisterForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only'
                                                          'letters, numbers, dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('password2', message='Passwords must match'),
                                                     Length(6, 20)])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field).first():
            raise ValidationError('Email already register.')

    def validate_username(self, field):
        if User.query.filter_by(username=field).first():
            raise ValidationError('Username already in use.')


class ChangePasswordForm(Form):
    pass



from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import users
from werkzeug.security import check_password_hash

# def validate_password(self, password):
#     email = self.email
#     user = user.query.filter_by(email=email.data).first()
#         if user is None or not check_password_hash(user.password, self.password.data):
#             raise ValidationError('Incorrect password.')

def validate_email_login(self, email):
    exists = users.query.filter_by(email=email.data).first()
    if exists is None:
            raise ValidationError('Incorrect email or account does not exist.')

def validate_email_create(self, email):
    exists = users.query.filter_by(email=email.data).first()
    if exists:
            raise ValidationError('Email in use.')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired("please enter email"), validate_email_login])
    password = PasswordField('password', validators=[DataRequired("please enter password")])
    submit = SubmitField('Sign In')


class CreateForm(FlaskForm):
    userName = StringField('Username', validators=[DataRequired("please enter name")])
    fullName = StringField('Full Name', validators=[DataRequired("please enter name")])
    email = StringField('Email', validators=[DataRequired("please enter email"), validate_email_create])
    password = PasswordField('Password', validators=[DataRequired("please enter password")])
    submit = SubmitField('Sign Up')
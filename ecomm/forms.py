from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Login",validators=[DataRequired()])

class RegisterForm(FlaskForm):
    firstname = StringField("First Name",validators=[DataRequired()])
    lastname = StringField("Last Name",validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    confirm_password = StringField("Confirm Pasword",validators=[DataRequired()])
    phone_no = StringField("Phone No",validators=[DataRequired()])
    submit = SubmitField("Register Now",validators=[DataRequired()])
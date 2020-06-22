from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError
from ecomm.models import User

class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=6,max=15)])
    submit = SubmitField("Login",validators=[DataRequired()])

class RegisterForm(FlaskForm):
    firstname = StringField("First Name",validators=[DataRequired(),Length(min=2,max=55)])
    lastname = StringField("Last Name",validators=[DataRequired(),Length(min=2,max=55)])
    email = StringField("Email", validators=[DataRequired(),Email()])
    password = StringField("Password", validators=[DataRequired(),Length(min=6,max=15)])
    confirm_password = StringField("Confirm Pasword",validators=[DataRequired(),Length(min=6,max=15),EqualTo('password')])
    phone_no = StringField("Phone No",validators=[DataRequired(),Length(min=10)])
    submit = SubmitField("Register Now",validators=[DataRequired()])

    def validate_email(sel,email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError("Email already in use, choose another")
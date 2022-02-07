import email
import imp
from flask_wtf import FlaskForm #for to create form of flask
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField,FileField # get data of type 
from wtforms.validators import DataRequired, ValidationError, Length, Email, EqualTo # check data input in form if not display message
from flask_wtf.file import FileAllowed
from todos.models import User

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=5, max=20)])
    email  = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another username!')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose another email!')
    
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")
    
class UpdateUserForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=5, max=20)])
    email  = EmailField("Email", validators=[DataRequired(), Email()])
    picture = FileField("Update Your Image", validators=[FileAllowed(['jpeg', 'png', 'jpg'])])
    submit = SubmitField("Update User")
    
    
class TaskForm(FlaskForm):
    task = StringField("Task", validators=[DataRequired()], render_kw={'placeholder': "Enter your task"})
    submit = SubmitField('Add Task')
    
    
    
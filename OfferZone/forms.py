from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from OfferZone.models import User,Mall,Shop,Product
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import SelectField

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class MallRegistrationForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=5, max=40)])
    desc = StringField('Description',
                        validators=[DataRequired(),Length(min=0, max=199)])
    addr1 = StringField('Address', validators=[DataRequired(),Length(min=5, max=99)])
    addr2 = StringField('City', validators=[DataRequired(),Length(min=3, max=99)])
    #addr3 = StringField('Pin Code', validators=[DataRequired(),Length(min=3, max=99)])
    #phone = StringField('Phone', validators=[DataRequired(),Length(min=5, max=99)])
    #open_time = StringField('Opening Time', validators=[DataRequired()])
    #close_time= StringField('Closing Time', validators=[DataRequired()])
    
    submit = SubmitField('Save')



    
    #def validate_name(self, name):
    #    selected_mall = Mall.query.filter_by(name=name.data).first()
    #    if selected_mall:
    #        raise ValidationError('That Mall is already registrated.')


class ShopRegistrationForm(FlaskForm):
           
            name = StringField('Name',
                                validators=[DataRequired(), Length(min=5, max=40)])

            addr = StringField('Address', validators=[DataRequired(),Length(min=5, max=99)])
            phoneno = StringField('Phone:', validators=[DataRequired(),Length(min=5, max=99)])
            desc = StringField('Description',
                                validators=[DataRequired(),Length(min=0, max=199)])
           
        
           
          
            submit = SubmitField('Save')







class ProductRegistrationForm(FlaskForm):
            name = StringField('Name',
                                    validators=[DataRequired(), Length(min=5, max=40)])

            company = StringField('Company', validators=[DataRequired(),Length(min=0, max=99)])
            price = StringField('Price:', validators=[DataRequired(),Length(min=0, max=99)])
            desc = StringField('Description',
                                        validators=[DataRequired(),Length(min=0, max=199)])
                
            submit = SubmitField('Save')



            

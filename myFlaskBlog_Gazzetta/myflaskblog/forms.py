# Preparazione Lezione 5

from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed
from flask_ckeditor import CKEditorField
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField , SelectField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from myflaskblog.models import User
from wtforms.widgets import TextArea
'''
Registrazione:
username
email
password
confirm_password

Login:
email
password
remembre_me
'''


class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[
                           Length(min=2, max=30), DataRequired()])
#    email = EmailField('email', validators=[Length(2, 100)])
    email = StringField('Email', validators=[
                        Length(min=2, max=100), Email(), DataRequired()])
    password = PasswordField('Password', validators=[
                             Length(min=8, max=100), DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[Length(min=8, max=100),
                                                 DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Register Now!')

    # def validate_field(self, field):
    #     if True:
    #         raise ValdationError('Validation Message')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already registered')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
                        Length(min=2, max=100), Email(), DataRequired()])
    password = PasswordField('Password', validators=[
                             Length(min=8, max=100), DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


#create a new post Form
class PostForm(FlaskForm):
    #liste per i campi select
    patch_choises = ["13.6" , "13.5" , "13.4"]
    role_choises = ["Top" , "Jungle" , "Mid" , "Bot" , "Support"]
    #effettivi spazi del form
    title = StringField("Title" , validators=[DataRequired()])
    patch = SelectField(u'Patch', choices = patch_choises, validators = [DataRequired()])
    role = SelectField(u'Role', choices = role_choises, validators = [DataRequired()])
    champion = StringField("Champion" , validators=[DataRequired()])
    enemy = StringField("Enemy" , validators=[DataRequired()])
    #post_content= StringField("Content" , validators=[DataRequired()] , widget=TextArea())
    post_content = CKEditorField('Content' , validators=[DataRequired()])
    submit = SubmitField('Create Post')

#form per aggiornare i dati dell'utente
class UpdateUserForm(FlaskForm):
    username = StringField('Username', validators=[
                           Length(min=2, max=30), DataRequired()])
    email = StringField('Email', validators=[
                        Length(min=2, max=100), Email(), DataRequired()])
    
    image_file = FileField('Update your Avatar' , validators=[FileAllowed(['jpg' , 'png'])])

    submit = SubmitField('Update')


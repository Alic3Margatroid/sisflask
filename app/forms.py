from flask_wtf import Form,FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(Form):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	email = StringField('Email',validators=[DataRequired()])
	name = StringField('Name',validators=[DataRequired()])
	phoneno = StringField('Phone Number',validators=[DataRequired()])

class EditForm(Form):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	name = StringField('Name',validators=[DataRequired()])
	email = StringField('Email',validators=[DataRequired()])
	phoneno = StringField('Phone Number',validators=[DataRequired()])

class MessageForm(Form):
	content = StringField('Content',validators=[DataRequired()])

class PhotoForm(FlaskForm):
	photo = FileField(validators=[FileRequired()])
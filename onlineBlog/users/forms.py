from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField
from wtforms.validators import DataRequired,Email,EqualTo,Length,ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user

from onlineBlog.models import User


class RegistrationForm(FlaskForm):
	username = StringField('Username',
		validators=[DataRequired(),
		Length(min=2,max=20)])
	email = StringField('Email',
		validators=[DataRequired(),Email()])
	password = PasswordField('Passowrd',validators=[DataRequired(),EqualTo('pass_confirm',message='Password Must Match')])
	pass_confirm = PasswordField('Confirm Passowrd',validators=[DataRequired()])
	submit = SubmitField('Register')

	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Your Email Has Been Registered ALready')

	def validate_username(self,field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Your UserName Has Been Registered ALready')


class LoginForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Passowrd',validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Log In')



class UpdateuserForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Email()])
	username = StringField('UserName',validators=[DataRequired()])
	picture = FileField('Update Profile Avatar',validators=[FileAllowed(['jpg','png'])])
	submit = SubmitField('Update')

	def validate_username(self,username):
		if username.data != current_user.username:
			if User.query.filter_by(username=username.data).first():
				raise ValidationError('Your Email Has Been Registered ALready')

	def validate_email(self,email):
		if email.data != current_user.email:
			if User.query.filter_by(email=email.data).first():
				raise ValidationError('Your UserName Has Been Registered ALready')



class RequestResetForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Email()])
	submit = SubmitField('Reset password')

	def validate_email(self,field):
		user = User.query.filter_by(email=field.data).first()
		if user is None:
			raise ValidationError('There Is No Account With That Email')


class ResetPasswordForm(FlaskForm):
	password = PasswordField('Passowrd',validators=[DataRequired(),EqualTo('pass_confirm',message='Password Must Match')])
	pass_confirm = PasswordField('Confirm Passowrd',validators=[DataRequired()])
	submit = SubmitField('Reset Password')

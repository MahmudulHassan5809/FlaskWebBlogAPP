from flask import render_template,url_for,flash,redirect,request,Blueprint
from onlineBlog.users.forms import (
	LoginForm,
	RegistrationForm,
	UpdateuserForm,
	ResetPasswordForm,
	RequestResetForm)
from flask_login import login_user,current_user,logout_user,login_required
from werkzeug.security import generate_password_hash
from onlineBlog import db,mail
from onlineBlog.models import User,BlogPost
from onlineBlog.users.picture_handler import add_profile_pic
from flask_mail import Message

users = Blueprint('users',__name__)


@users.route("/register",methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('core.home'))
	form = RegistrationForm()
	error = None;
	if request.method == 'POST' and form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			error = "Email Already Exists"
		else:
			user = User(email=form.email.data,
						username=form.username.data,
						password=form.password.data)
			db.session.add(user)
			db.session.commit()
			flash('Thanks For Registration','success')
			return redirect(url_for('users.login'))

	return render_template('register.html',form=form,error=error)


@users.route("/login",methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('core.home'))
	form = LoginForm()
	error = None
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			if user.check_password(form.password.data) and user is not None:
				login_user(user,remember=form.remember.data)
				flash('Log in Success','success')
				next = request.args.get('next')
				if next == None or not next[0] == '/':
					next = url_for('core.home')
				return redirect(next)
			else:
				error = 'Password DoesNot Match'
		else:
			error = 'No User Found'

	return render_template('login.html',error=error,form=form)


@users.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for("core.home"))



@users.route("/account",methods=['GET','POST'])
@login_required
def account():
	form = UpdateuserForm()
	if form.validate_on_submit():
		if form.picture.data:
			username =  current_user.username
			pic = add_profile_pic(form.picture.data,username)
			current_user.profile_image = pic
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('User Account Updated','success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data    = current_user.email
	profile_image = url_for('static',filename='profile_pics/' + current_user.profile_image)
	return render_template('account.html',title=current_user.username,profile_image=profile_image,form=form)



@users.route("/<username>/posts")
def user_posts(username):
	page = request.args.get('page',1,type=int)
	user = User.query.filter_by(username=username).first_or_404()
	blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.created_at.desc()).paginate(page=page,per_page=5)
	return render_template('home.html',title=user.username+'Posts',posts=blog_posts,user=user)


def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
	msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
	mail.send(msg)

@users.route("/reset_passowrd",methods=['GET','POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('core.home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An Email Has Been Sent With Instructions To reset Your Password','info')
		return redirect(url_for('users.login'))
	return render_template('reset_request.html',title='Reset Password',form=form)



@users.route("/reset_passowrd/<token>",methods=['GET','POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('core.home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an Invalid Or Expried Token','warning')
		return redirect(url_for('users.reset_request'))

	form = ResetPasswordForm()
	if form.validate_on_submit():

		user.password_hash = generate_password_hash(form.password.data)

		db.session.commit()
		flash('Your PassWord Has Been SuccessFully Changed','success')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html',title='Reset Password',form=form)

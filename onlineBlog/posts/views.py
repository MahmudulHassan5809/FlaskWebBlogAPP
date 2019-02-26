from flask import render_template,url_for,flash,redirect,request,Blueprint,abort
from flask_login import current_user,login_required
from onlineBlog import db
from onlineBlog.models import BlogPost
from onlineBlog.posts.forms import BlogPostForm


posts = Blueprint('posts',__name__)



# create
@posts.route("/create",methods=['GET','POST'])
@login_required
def create_post():
	form = BlogPostForm()
	if request.method == 'POST' and form.validate() and form.validate_on_submit():
		blog_post = BlogPost(title=form.title.data,text=form.text.data,user_id=current_user.id)
		db.session.add(blog_post)
		db.session.commit()
		flash('Post Created','success')
		return redirect(url_for('core.home'))
	return render_template('create_post.html',title='Create Post',form=form)


# View Post
@posts.route("/post/<int:post_id>",methods=['GET','POST'])
def post(post_id):
	post = BlogPost.query.get_or_404(post_id)
	return render_template('post.html',title=post.title,post=post)

# Update
@posts.route("/post/<int:post_id>/update",methods=['GET','POST'])
@login_required
def update_post(post_id):
	post = BlogPost.query.get_or_404(post_id)
	if post.author != current_user:
		#return render_template('error_pages/403.html') , 403
		abort(403)

	form = BlogPostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.text = form.text.data
		db.session.commit()
		flash('Post Updated','success')
		return redirect(url_for('posts.post',title=post.title, post_id=post.id))

	elif request.method == 'GET':
		form.title.data = post.title
		form.text.data = post.text
		return render_template('create_post.html',title=post.title,form=form)

# Delete
@posts.route("/post/<int:post_id>/delete",methods=['GET','POST'])
@login_required
def delete_post(post_id):
	post = BlogPost.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
		#return render_template('error_pages/403.html') , 403
	db.session.delete(post)
	db.session.commit()
	flash('Post Deleted','success')
	return redirect(url_for('core.home'))

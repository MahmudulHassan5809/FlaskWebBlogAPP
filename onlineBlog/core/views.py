from flask import render_template,request,Blueprint
from onlineBlog.models import BlogPost

core = Blueprint('core',__name__)


@core.route("/")
@core.route("/home")
def home():
	page = request.args.get('page',1,type=int)
	posts = BlogPost.query.order_by(BlogPost.created_at.desc()).paginate(page=page,per_page=4)
	return render_template('home.html',posts=posts)

@core.route("/about")
def about():
	return render_template('about.html')

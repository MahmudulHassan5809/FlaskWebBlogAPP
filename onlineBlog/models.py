from onlineBlog import db,login_manager,app
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(db.Model,UserMixin):
    '''
    User
    '''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True,index=True,nullable=False)
    profile_image = db.Column(db.String(64),nullable=False,default='default.png')
    email = db.Column(db.String(64),unique=True,index=True)

    password_hash = db.Column(db.String(128))


    posts = db.relationship('BlogPost',backref='author',lazy=True)


    def get_reset_token(self,expires_sec=1800):
         s = Serializer(app.config['SECRET_KEY'],expires_sec)
         return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except :
            return None
        return User.query.get(user_id)


    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)




    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def  __repr__(self):
        return f"User('{self.username}','{self.email}','{self.profile_image}')"




class BlogPost(db.Model):
    users = db.relationship(User)

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140),nullable=False)
    text = db.Column(db.Text,nullable=False)



    def __init__(self,title,text,user_id):
        self.title = title
        self.text = text
        self.user_id = user_id


    def  __repr__(self):
        return f"Post ID {self.id}"

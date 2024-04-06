from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)


  
class User(db.Model):
  __tablename__ ='users'
  
  user_id=db.Column(db.Integer,
               primary_key=True,
               autoincrement=True)
  
  First_Name = db.Column(db.String(20),
                     nullable=False,)
  
  Last_Name = db.Column(db.String(20),
                     nullable=False,)
  
  Profile_Pic = db.Column(db.String(2000),
                     nullable=False,)
  
  owner = db.relationship('Post')
  
class Post(db.Model):
  
  __tablename__='post'
  
  id=db.Column(db.Integer, primary_key=True, autoincrement=True)
  
  title=db.Column(db.String(100),
                     nullable=False,)
  
  comment=db.Column(db.String(1000),
                     nullable=False,)
  
  user_ref =db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'))
  
  owner_id = db.relationship('User')
  tags = db.relationship("Tag", secondary='post_Tags', backref='posts')
  
  
class Tag(db.Model):
  
  __tablename__='tags'
  
  id=db.Column(db.Integer, primary_key=True, autoincrement=True)
  
  name=db.Column(db.String(20),
                     nullable=False,
                     unique=True)
  
  
  
class PostTag(db.Model):
  
  __tablename__='post_Tags'
  
  post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'),primary_key=True)
    
  tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'),primary_key=True)
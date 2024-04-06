from flask import Flask, request, render_template, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pepe1@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] ='lolo'

connect_db(app)
app.app_context().push()

@app.route('/')
def Home_Page():
    users = User.query.all()
    return render_template('home.html',users=users)

@app.route('/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_ref == user_id)
    return render_template('details.html',user = user,posts=posts)

@app.route('/user_create')
def show_create():
    return render_template('create.html')

@app.route('/user_create',methods=['POST'])
def create_user():
    First_Name = request.form['First_Name']
    Last_Name = request.form['Last_Name']
    Profile_Pic = request.form['Profile_Pic']
    
    new_user = User(First_Name=First_Name, Last_Name=Last_Name, Profile_Pic=Profile_Pic)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(f'/{new_user.user_id}')

@app.route('/delete',methods=['POST'])
def delete_user():
    user = request.form['id']
    User.query.filter(User.user_id == user).delete()
    db.session.commit()

    return redirect('/')

@app.route('/edit')
def show_edit():
    user_id= request.args['id']
    user=User.query.get(user_id)
    return render_template('edit.html',user=user)

@app.route('/edit',methods=['POST'])
def edit_user():
    user_id= request.form['id']
    First_Name = request.form['First_Name']
    Last_Name = request.form['Last_Name']
    Profile_Pic = request.form['Profile_Pic']
    
    User.query.get(user_id).First_Name=First_Name
    User.query.get(user_id).Last_Name=Last_Name 
    User.query.get(user_id).Profile_Pic=Profile_Pic
    db.session.commit()
    
    return redirect('/')

@app.route('/add_post')
def add_post():
    user_id= request.args['id']
    user=User.query.get(user_id)
    tags=Tag.query.all()
    return render_template('add_post.html', user=user,tags=tags)

@app.route('/sub_post', methods=['POST'])
def add_post_to_db():
    title = request.form['title']
    comment = request.form['comment']
    user_ref= request.form['id']
    tag_id=request.form.getlist('tag_id')
    
    new_post=Post(title=title,comment=comment,user_ref=user_ref)
    db.session.add(new_post)
    db.session.commit()
    new_post.tags=Tag.query.filter(Tag.id.in_(tag_id)).all()
    db.session.add(new_post)
    db.session.commit()
    
    return redirect(f'/{user_ref}')


@app.route('/p<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags= db.session.query(Tag.name,Tag.id).join(PostTag).filter( PostTag.post_id == post_id).all()
    return render_template('post_details.html',post=post,tags=tags)

@app.route('/edit_post')
def show_edit_post():
    post_id= request.args['id']
    post=Post.query.get(post_id)
    tags=Tag.query.all()
    return render_template('edit_post.html',post=post,tags=tags)


@app.route('/edit_post',methods=['POST'])
def edit_post():
    post_id= request.form['id']
    title = request.form['title']
    comment = request.form['comment']
    post=Post.query.get(post_id)
    tag_id=request.form.getlist('tag_id')
    
    
    Post.query.get(post_id).title=title
    Post.query.get(post_id).comment=comment
    Post.query.get(post_id).tags=Tag.query.filter(Tag.id.in_(tag_id)).all()
    db.session.commit()
    
    return redirect(f'/{post.user_ref}')

@app.route('/deleteP',methods=['POST'])
def delete_Post():
    post = request.form['id']
    get_post = Post.query.get(post)
    user= User.query.get(get_post.user_ref)
    Post.query.filter(Post.id == post).delete()
    db.session.commit()
    
    return redirect(f'/{user.user_id}')


@app.route('/tag_list')
def tag_list():
    tags = Tag.query.all()
    return render_template('tag_list.html',tags=tags)

@app.route('/t<int:tag_id>')
def show_post_tag(tag_id):
    tags = Tag.query.get_or_404(tag_id)
    tags_post = Tag.query.all()
    return render_template('tag_posts.html',tags=tags,tags_post=tags_post)


@app.route('/create_tag')
def create_tag():
    return render_template('add_tag.html')



@app.route('/create_tag', methods=['POST'])
def add_tag_to_db():
    name = request.form['name']

    new_tag=Tag(name=name)
    
    db.session.add(new_tag)
    db.session.commit()
    
    return redirect('tag_list')

@app.route('/edit_tag')
def show_edit_tag():
    tag_id= request.args['id']
    tag=Tag.query.get(tag_id)
    
    return render_template('edit_tag.html',tag=tag)


@app.route('/edit_tag', methods=['POST'])
def edit_tag():
    tag_id= request.form['id']
    name = request.form['name']
    tag=Tag.query.get(tag_id)
   
    Tag.query.get(tag_id).name=name
    
    db.session.commit()
    
    return redirect(f'/t{tag.id}')

@app.route('/deleteT',methods=['POST'])
def delete_Tag():
    tag = request.form['id']
    Tag.query.filter(Tag.id == tag).delete()
    db.session.commit()
    
    return redirect('tag_list')
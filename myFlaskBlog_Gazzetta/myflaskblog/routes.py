# Preparazione Lezione 5
import os 
import secrets
from flask import render_template, url_for, redirect, flash , abort , request
from myflaskblog import app, db, bcrypt
from myflaskblog.forms import RegistrationForm, LoginForm , PostForm , UpdateUserForm
from myflaskblog.models import User , Post
from flask_login import login_user, logout_user, current_user, login_required


# from wtforms import


""""posts = [
    {"author": "Pico de Paperis",
     "title": "This is a Blog",
     "content": "This is a post by PdP. Se il post e' lunghissimo non cambia niente ?",
     "date_posted": "16-11-2022 15:48"
     },
    {"author": "Paolino Paperino",
     "title": "Qua Qua Qua",
     "content": "Paperino ha scritto in italiano",
     "date_posted": "15-11-2022 20:48"
     }
]"""
"""
posts = [
    {"id":1,
     "author": "Cookie",
     "character" : "Kai'sa",
     "enemy" : "Caitlyn",
     "role": "ADC",
     "patch": "13.2"},
     {"id":2,
     "author": "Cookie",
     "character" : "Tristana",
     "enemy" : "Ezreal",
     "role": "ADC",
     "patch": "13.2.1"},
     {"id":3,
     "author": "Cookie",
     "character" : "Tristana",
     "enemy" : "Ezreal",
     "role": "ADC",
     "patch": "13.2.1"}
]"""
#useful to reset the database for debugging purposes
#with app.app_context():
#    db.drop_all()
#    db.create_all()

@app.route("/")
@app.route("/home")
def home():
    #get posts from db
    posts = Post.query.order_by(Post.date_posted)
    return render_template("home.html", title="Home Page", posts=posts)

#@app.route("/post")
#def post():
#    return render_template("post.html", title="General Post")

@app.route("/post/<int:id>")
def post(id):
    
    post = Post.query.get_or_404(id)
    #getting the image file of the user who wrote the post
    image_file = url_for("static" , filename=f"images/{User.query.get_or_404(post.user_id).image_file}" )
    return render_template("post.html", title=f"{post.title}"  ,post=post , image_file=image_file)


@app.route("/update_post/<int:id>", methods=['POST', 'GET'])
@login_required
def update_post(id):
    form = PostForm()
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash("You can't edit this post", category="danger")
        return redirect(url_for("post", id=post.id))
    if form.validate_on_submit():
        post.title = form.title.data
        post.post_content = form.post_content.data
        post.patch = form.patch.data
        post.role = form.role.data
        post.champion = form.champion.data
        post.enemy = form.enemy.data
        db.session.add(post)
        db.session.commit()
        flash("Post has been updated", category="success")
        return redirect(url_for("post", id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.post_content.data = post.post_content
        form.patch.data = post.patch
        form.role.data = post.role
        form.champion.data = post.champion
        form.enemy.data = post.enemy
    return render_template("update_post.html", title="Update Post", form=form, legend="Update Post")

@app.route("/delete_post/<int:id>")
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash("You can't delete this post", category="danger")
        return redirect(url_for("post", id=post.id))
    db.session.delete(post)
    db.session.commit()
    flash("Post has been deleted", category="danger")
    return redirect(url_for("home"))




@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        candidate = form.password.data
        if user and bcrypt.check_password_hash(user.password, candidate):
            login_user(user, remember=form.remember_me.data)
            flash('Welcome', category='success')
            return redirect('home')

        else:
            flash('Wrong email or password', category='danger')
            return redirect('login')
    else:
        return render_template("login.html", title="Login Page", form=form)


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        password = form.password.data
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=form.username.data,
                    password=pw_hash,
                    email=form.email.data)
        with app.app_context():

            db.session.add(user)
            db.session.commit()

        flash(
            f"Your account has been created {form.username.data}", category="success")
        return redirect('/home')

    return render_template("register.html", title="Register Page", form=form)


#the page to create a new post, must be logged to access it
@app.route("/new_post", methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    
    if form.validate_on_submit():
        #getting the post datas from the form
        post = Post(title = form.title.data ,
        post_content = form.post_content.data ,
        patch = form.patch.data ,
        role=form.role.data ,
        champion = form.champion.data ,
        enemy = form.enemy.data,
        user_id = current_user.id )
        
        #add the post to the database
        with app.app_context():
            db.session.add(post)
            db.session.commit()
        #Return a message
        flash("Blog post submitted", category="success")
        post.__delattr__
        return render_template("new_post.html", form = form,  title="New Post")
    form.title.data = ''
    form.post_content.data = ''
    form.patch.data = ''
    form.role.data = ''
    form.champion.data = ''
    form.enemy.data = ''
    return render_template("new_post.html", form = form,  title="New Post")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(f'Logged Out', category='info')
    return redirect('/home')

@app.route("/user_account")
@login_required
def user_account():
    image_file = url_for("static" , filename=f"images/{current_user.image_file}" )
    return render_template("user_account.html", title=f"{current_user.username} Page",
    image_file = image_file)


@app.route("/edit_account" , methods=['POST', 'GET'])
@login_required
def edit_account():
    image_file = url_for("static" , filename=f"images/{current_user.image_file}" )
    form = UpdateUserForm()
    
    if form.validate_on_submit():

        if form.image_file.data:
            new_file_name = save_image_file(form.image_file.data)
            current_user.image_file = new_file_name
        if current_user.username != form.username.data:
            current_user.username = form.username.data
        if current_user.email != form.email.data:
            current_user.email = form.email.data
        
        
        
        flash(f'Account has been updated {form.username.data}', category="success")
        db.session.commit()
        return redirect(url_for('user_account'))
    else:
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    
    return render_template("edit_account.html",form = form, title=f"{current_user.username} Page" , image_file = image_file)

def save_image_file(image_file_data):
    #getting path to the old image file
    old_file_path = os.path.join(os.getcwd(), "myflaskblog",
                             "static", "images", current_user.image_file)
    #deleting the old image file if it exists and it's not the default image
    if os.path.exists(old_file_path) and current_user.image_file != "default_img.jpg":
        os.remove(old_file_path)
    
    _, file_ext = os.path.splitext(image_file_data.filename)

    new_name = secrets.token_hex(8)
    new_file_name = new_name + file_ext
    file_path = os.path.join(os.getcwd(), "myflaskblog",
                             "static", "images", new_file_name)

    image_file_data.save(file_path)
    
    return new_file_name

@app.route("/other_user_account/<string:user_username>/<int:id>")
@login_required
def other_user_account(id , user_username):
    post = Post.query.get_or_404(id)
    user = User.query.get_or_404(post.user_id)
    #getting the image file of the user who wrote the post
    image_file = url_for("static" , filename=f"images/{user.image_file}")
    return render_template("other_user_account.html", title=f"{user.username} Page",
    image_file = image_file , user=user , id=id)

@app.route("/flt_posts/<string:user_username>")
def flt_posts(user_username):
    #get posts from db
    posts = User.query.filter_by(username=user_username).first().posts
    return render_template("home.html", title="Home Page", posts=posts)
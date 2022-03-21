
from asyncio import tasks
from flask_login import login_user,logout_user,current_user,login_required
from todos import app, bcrypt,db
from flask import render_template, redirect, url_for, request,flash
from todos.forms import RegisterForm, LoginForm, TaskForm, UpdateUserForm
from todos.models import User, Todo, Task
import email,secrets,os
from datetime import date
@app.route("/")
def home():
    return render_template("index.html", title = "Home Page")
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password = hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in!", "success")
        return redirect(url_for("login"))
    
    return render_template("register.html", form = form, title= "Register")
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user =User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash("You have been logged in!", 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login Unsuccessfull. Please check email and password!", 'danger')
    return render_template("login.html",form = form, title= "Login")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

def save_picture(img):
    random_hex = secrets.token_hex(8)
    f_name, f_ext =os.path.splitext(img.filename)
    image_name = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/img', image_name)
    img.save(image_path)
    return image_name

def remove_picture(img):
    os.remove(os.path.join(app.root_path, 'static/img', img))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:
            if current_user.user_image != 'default.png':
               remove_picture(current_user.user_image)
            picture_file = save_picture(form.picture.data)
            current_user.user_image = picture_file
            
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", title = "Account Page", form=form)

@app.route("/todo", methods=["GET", "POST"])
@login_required
def todo():
    form = TaskForm()
    todo = Todo.query.filter(Todo.date_created == date.today(), Todo.user_id==current_user.id).first()
    if todo:
        tasks = Task.query.filter(Task.todo_id==todo.id)
    else:
        tasks = None
    if form.validate_on_submit():
        t = form.task.data
        task = Task(task=t, todo_id=todo.id)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('todo'))
        
    return render_template("todo.html",todo= todo, title= "Todo Today",form = form,tasks = tasks)

@app.route("/new_todo")
@login_required
def new_todo():
    date_created = date.today()
    new_todo = Todo(date_created=date_created, user_id=current_user.id)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('todo'))

@app.route("/task/completed/<int:id>")
def task_completed(id):
    task = Task.query.filter_by(id=id).first()
    task.completed = True
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('todo'))


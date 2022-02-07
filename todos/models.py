from email.policy import default
from enum import unique
import imp
from todos import db ,login_manager
from datetime import date
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    user_image = db.Column(db.String(50), default='default.png')
    password = db.Column(db.String(100), nullable=False)
    todos = db.relationship('Todo', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f"<User: {self.username}>"
    
    
class Todo(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date_created = db.Column(db.Date(), default=date.today())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    tasks = db.relationship("Task", backref="todo", lazy='dynamic')
    
    def __repr_(self):
        return f"<Todo: {self.date_created}>"
    
class Task(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    task = db.Column(db.String(50), nullable=False)
    completed = db.Column(db.Boolean(), default=False)
    todo_id = db.Column(db.Integer(), db.ForeignKey('todo.id'), nullable=False)
    
    def __repr__(self):
        return f'<Task: {self.task}>'
    
    
    
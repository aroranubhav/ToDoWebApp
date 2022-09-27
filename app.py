import json
from urllib import response
from flask import Flask, jsonify, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://maxi@127.0.0.1:5432/todowebapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = false

db = SQLAlchemy(app)
migrate = Migrate(app = app, db = db)

class ToDo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(), nullable = False)
    completed = db.Column(db.Boolean, nullable = False, default = False)
    todo_category_id = db.Column(db.Integer, db.ForeignKey('todoslists.id'), nullable = False)

    def __repr__(self) -> str:
        return f'<ToDo: {self.id} {self.description} {self.completed}>'

class ToDoList(db.Model):
    __tablename__ = 'todoslists'
    id = db.Column(db.Integer, primary_key = True)
    todo_category = db.Column(db.String(), nullable = False)
    todos = db.relationship('ToDo', backref = 'list', lazy = True)
    completed = db.Column(db.Boolean, nullable = False, default = False)

    def __repr__(self) -> str:
        return f'<ToDoList {self.id} {self.todo_category}>'

@app.route('/')
def index(): #route handler
    return redirect(url_for('get_category_todos', list_id = 1))

@app.route('/lists/<list_id>')
def get_category_todos(list_id):
    return render_template('index.html',
    list = ToDoList.query.all(),
    active_list = ToDoList.query.get(list_id),
    todos = ToDo.query.filter_by(todo_category_id = list_id).order_by('id').all())

@app.route('/add-todo-category', methods = ['POST'])
def add_todo_category():
    error = False
    body = {}
    try:
        category = request.get_json()['todo_category']
        new_category = ToDoList(todo_category = category)
        db.session.add(new_category)
        db.session.commit()
        body['id'] = new_category.id
        body['todo_category'] = new_category.todo_category
        body['completed'] = False
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    
    if error:
        abort(400)
    else:
        return jsonify(body)


@app.route('/todos/create', methods = ['POST'])
def create_todo():
    error = False
    body = {}
    try:
        todo_description = request.get_json()['description']
        new_todo = ToDo(description = todo_description, completed = False)
        db.session.add(new_todo)
        db.session.commit()
        body['id'] = new_todo.id
        body['description'] = new_todo.description
        body['completed'] = new_todo.completed
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    
    if error:
        abort(400)
    else:
        return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods = ['POST'])
def set_completed_todo(todo_id):
    try:
        completed_state = request.get_json()['completed']
        print(todo_id)
        todo = ToDo.query.get(todo_id)
        todo.completed = completed_state
        db.session.commit()
    except:
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()
    
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>/delete', methods = ['DELETE'])
def delete_todo(todo_id):
    try:
        todo = ToDo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()

    return jsonify({'success' : True})


if __name__ == '__main__':
    app.run(debug = True, port = 5000)
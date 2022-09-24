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

    def __repr__(self) -> str:
        return f'<ToDo: {self.id} {self.description} {self.completed}>'

@app.route('/')
def index(): #route handler
    return render_template('index.html', todos = ToDo.query.order_by('id').all())

@app.route('/todos/create', methods = ['POST'])
def create_todo():
    error = False
    body = {}
    try:
        todo_description = request.get_json()['description']
        new_todo = ToDo(description = todo_description)
        db.session.add(new_todo)
        db.session.commit()
        body['description'] = todo_description
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


if __name__ == '__main__':
    app.run(debug = True, port = 5000)
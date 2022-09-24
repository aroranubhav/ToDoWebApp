from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false
from flask_migrate import Migrate

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

@app.route('/')
def index(): #home route handler
    return render_template('index.html', todos = ToDo.query.order_by('id').all())

@app.route('/todos/create', methods = ['POST'])
def create_todo():
    todo_description = request.form.get('description')
    new_todo = ToDo(description = todo_description)
    print(todo_description)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug = True, port = 3000)
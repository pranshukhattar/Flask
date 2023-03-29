#  Video link - https://www.youtube.com/watch?v=oA8brF3w5XQ&ab_channel=CodeWithHarry
#  Run this in same folder to run virtual environment: venv\Scripts\activate.bat

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_DATABASE_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
@app.route('/', methods=['GET'])
def index():
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/new', methods=['POST'])
def new_item():
    title = request.form['title']
    desc = request.form['desc']
    todo = Todo(title=title, desc=desc)
    db.session.add(todo)
    db.session.commit()
    return redirect("/")


@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit() 
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    print(todo)
    return render_template('update.html', todo=todo )


@app.route('/delete/<int:sno>')
def delete(sno):
    task = Todo.query.filter_by(sno=sno).first()
    db.session.delete(task)
    db.session.commit()
    print(task)
    return redirect("/")

@app.route('/show')
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'This is show page'

if __name__ == "__main__" :
    app.run(debug = True)
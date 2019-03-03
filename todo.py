from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////kodlamalar_vs/TODO/todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)
    #username = db.Column(db.String(80), unique=True, nullable=False)
    #email = db.Column(db.String(120), unique=True, nullable=False)

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos = todos)

@app.route("/add", methods = ["POST"]) #sadece post olursa çalışacak
def addTodo():
    title = request.form.get("title")
    newTodo = Todo(title = title, complete = False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<string:id>")
def updateTodo(id):
    title = request.form.get("title")
    todo = Todo.query.filter_by(id = id).first()
    todo.title = title
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    todo.complete = not(todo.complete)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))



if __name__ == "__main__":
    #from yourapplication import db
    db.create_all() 
    #DB ilk başta çalıştırılıyor
    app.run(debug=True)

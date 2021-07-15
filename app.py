from flask import Flask,request,render_template, redirect, url_for, flash
import pickle
import json
import requests
from os import truncate 
from flask_sqlalchemy import SQLAlchemy  # For the database which is required to store our todos
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("login.html")
database={'guest':'123','aditya':'coditas'}

@app.route('/form_login',methods=['POST','GET'])
def login():
    name1=request.form['username']
    pwd=request.form['password']
    if name1 not in database:
	    return render_template('login.html',info='Invalid User')
    else:
        if database[name1]!=pwd:
            return render_template('login.html',info='Invalid Password')
        else:
	         return render_template('home.html',name=name1)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
  
# A decorator used to tell the application
# which URL is associated function

class Todo(db.Model):                                          # creating the class for database
    sno = db.Column(db.Integer, primary_key=True )
    title = db.Column(db.String(200), nullable=False )
    desc = db.Column(db.String(500), nullable=False )
    date_created = db.Column(db.DateTime, default = datetime.utcnow )

    def __repr__(self) -> str:   # This ia to show that what do we want to see in the output
        return f"{self.sno} - {self.title}"

    
@app.route('/testing', methods = ['GET','POST'])                 # we nned to call our POST method request here
def hello():
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)                              # to add the todos to our database
        db.session.commit()                                # commit the changes

    allTodo = Todo.query.all()
    return render_template('testing.html', allTodo=allTodo)  
    

@app.route('/show')      
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'Learning FLASK'

@app.route('/update/<int:sno>',methods = ['GET','POST'])      
def update(sno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/testing")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todo)
    

@app.route('/delete/<int:sno>')      
def delete(sno):
 
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/testing")

@app.route('/index')
def snake_game():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
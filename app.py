from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#initializing flaskapplication to app
app = Flask(__name__)  
#sqllite database of name todo.db will be used  for app
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)      
# 1. SQLAlchemy(app): here we are creating S obj of QLAlchemy class and passing our Flask app  as an argument
# This instance will be used to interact with your database.
# 2. db: This is a variable that holds the SQLAlchemy instance, allowing you to use it 
# throughout our application to define models, create tables, and perform database operations.


class Todo(db.Model): #making it a model class for SQLAlchemy. This means it will be mapped to a database table.
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"

#Todo class inherit from db.model i.e defines a table with columns for a sno, title, desc, and creation date. 
# The __repr__ method provides a readable string representation of the Todo instances(llke tostring in java).

@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        print("post")
        title = request.form['title']
        desc = request.form['desc']
  
        todo = Todo(title=title, desc=desc) #Creating a Todo Instance:
        db.session.add(todo) #Adding to the Database:
        db.session.commit() #Committing to Databse:

        return redirect(url_for('hello_world'))  # Redirect after form submission

    allTodo = Todo.query.all()
    #This line queries the  database for all entries in the Todo table and stores them in the allTodo variable.
    print(allTodo)  #print on console
    return render_template('index.html', allTodo=allTodo)
    #This line renders the index.html template, passing the list of all Todo instances (allTodo) to the template.
    # This allows you to display the todos on the webpage.
   

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods=['GET','POST'])
def update(sno):
    if request.method =='POST':
         title = request.form['title']
         desc = request.form['desc']
         todo = Todo.query.filter_by(sno=sno).first()
         todo.title=title
         todo.desc=desc
         db.session.add(todo)
         db.session.commit()
         return redirect("/") 

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
   
    

if __name__ == "__main__":

    app.run(debug=True, port=8000)
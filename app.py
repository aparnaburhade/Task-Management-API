from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

#create the flask app
app = Flask(__name__)

#Set up the database configuration
#sqlite:///tasks.db means we are using sqlite and the database file will be named 'tasks.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

#disable a feature that is not needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

#connect Flask to db
db = SQLAlchemy(app)

#define a "task" model , a blueprint for the task we'll store in the database 
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    done = db.Column(db.Boolean, default = False)

    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'

#Define a simple home page route 
@app.route('/')
def home():
    return "Welcome to the Task Management API!"

if __name__ == 'main':
    db.create_all()
    app.run(debug=True, port=5001)

    print("App is running..")

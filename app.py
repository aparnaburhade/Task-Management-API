from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Create the Flask app
print("Starting Flask app...")
app = Flask(__name__)

# Set up the database configuration
# sqlite:///tasks.db means we are using SQLite and the database file will be named 'tasks.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

# Disable a feature that is not needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Connect Flask to the database
db = SQLAlchemy(app)

# Define a "Task" model, a blueprint for the tasks we'll store in the database
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'

# Define a simple home page route
@app.route('/')
def home():
    return "Welcome to the Task Management API!"

# POST endpoint to create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    # Get the JSON data from the request
    data = request.get_json()

    # Extract required fields
    title = data.get('title')
    description = data.get('description', '')  # Optional field
    done = data.get('done', False)  # Default to False if not provided

    # Validate title
    if not title:
        return jsonify({"error": "Title is required"}), 400

    # Create a new Task instance
    new_task = Task(title=title, description=description, done=done)

    # Add the task to the database
    db.session.add(new_task)
    db.session.commit()

    # Return the created task as a JSON response
    return jsonify({
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "done": new_task.done
    }), 201


@app.route('/tasks', methods=['GET'])
def get_tasks():
    #Fetch all tasks from the database
    tasks = Task.query.all()

    #convert each task object into a dictionary
    tasks_list = []
    for task in tasks:
        tasks_list.append({
            "id":task.id,
            "title": task.title,
            "description": task.description,
            "done": task.done
        })

    return jsonify(tasks_list), 200

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database and tables are created
    print("Running Flask app...")
    app.run(debug=True, port=5001)  # Corrected "portal" to "port"

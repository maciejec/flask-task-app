from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfiguracja bazy danych SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definicja modelu Task
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='created')

# Tworzenie bazy danych (raz, na starcie)
with app.app_context():
    db.create_all()

# Strona główna
@app.route('/')
def home():
    return "Task App działa!"

# Frontend – ładowanie index.html
@app.route('/frontend')
def frontend():
    return render_template('index.html')

@app.route('/edit.html')
def edit_task_view():
    return render_template('edit.html')
    

# Endpoint GET /tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    tasks_list = []
    for task in tasks:
        tasks_list.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status
        })
    return jsonify(tasks_list)

# Endpoint POST /tasks
'''@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()

    new_task = Task(
        title=data['title'],
        description=data['description'],
        status=data.get('status', 'created')  # domyślnie "created"
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        'message': 'Task added successfully',
        'task': {
            'id': new_task.id,
            'title': new_task.title,
            'description': new_task.description,
            'status': new_task.status
        }
    }), 201'''
# ... (wszystko co już masz)

# Endpoint POST /tasks
'''@app.route('/tasks', methods=['POST'])
def add_task():
    # ...
    return jsonify({...}), 201'''

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()

    new_task = Task(
        title=data['title'],
        description=data['description'],
        status=data.get('status', 'created')  # domyślnie "created"
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        'message': 'Task added successfully',
        'task': {
            'id': new_task.id,
            'title': new_task.title,
            'description': new_task.description,
            'status': new_task.status
        }
    }), 201


# 🔽 WSTAW TO TUTAJ (przed if __name__)
# Pobierz jedno zadanie
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status
    })


@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    task = Task.query.get_or_404(id)

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)

    db.session.commit()

    return jsonify({'message': 'Zadanie zaktualizowane.'})


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Zadanie usunięte.'})




# Uruchomienie aplikacji
if __name__ == '__main__':
    app.run(debug=True)

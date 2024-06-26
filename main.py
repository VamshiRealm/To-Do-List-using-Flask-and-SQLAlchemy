from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initializing the application
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///todolist.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        title = request.form.get('title')
        desc = request.form.get('description')

        if title and desc:
            todo = Todos(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()

    all_todos = Todos.query.all()
    return render_template('index.html', todos=all_todos)

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todos.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    todo = Todos.query.get_or_404(id)
    if request.method == "POST":
        todo.title = request.form['title']
        todo.desc = request.form['description']
        db.session.commit()
        return redirect('/')
    return render_template('update.html', todo=todo)

if __name__ == '__main__':
    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(port=5002, debug=True)

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from models import Todo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ma = Marshmallow(app)

db = SQLAlchemy(app)

@app.route('/', methods = ['GET'])
def index():
    return render_template('base.html')

@app.route('/add', methods = ['POST'])
def add():
    title = request.form['title']
    todo = Todo(title=title)

    db.session.add(todo)
    db.session.commit()
   # Todo.query_all()


    import pdb; pdb.set_trace()

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ma = Marshmallow(app)

db = SQLAlchemy(app)
db.create_all()

# ROUTES
@app.route('/', methods = ['GET'])
def index():
    todos = Todo.query.all()        # get all the todos from the database
    return render_template('base.html', todos=todos)     # todos=todos pass this variable 'todos', and use this variable base.html

@app.route('/add', methods = ['POST'])
def add():
    title = request.form['title']   # gets the title from the form. request is an object that holds the form data
    due_date = request.form['due_date']
    todo = Todo(title=title,due_date=due_date)        # use the Todo class from line 29 to create a todo and save it in a variable

    db.session.add(todo)            # get the todo ready to save
    db.session.commit()             # save todo to the database
    return redirect('/')            # redirect to the main page 

# CLASSES
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(120))
    due_date = db.Column(db.String(120))

    def __repr__(self):
        return "Todo('{}')".format(self.title)

class TodoSchema(ma.Schema):
    class Meta:
        fields = ('titles',)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

# @app.route('delete/<string:id_data>', methods = ('POST', 'GET') )
# def delete(id_data):
    
#     cur = mysql.connection.cursor()
#     cur.excute("DELETE FROM Todo where id = %s", (id_data))
#     mysql.connection.commit()
#     return redirect(url_for('Index'))



""" *******
   1. How to loop over data in the html file. THere is a variable called 'todos' which is an array. How to display that information in the html file.
     - look for {% %} type stuff when reading about flask
   2. read those articles i sent, your data is called 'todos'
""" 
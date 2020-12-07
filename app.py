import os
from flask import Flask, render_template, request, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from dotenv import load_dotenv

project_folder = os.path.expanduser('./') 
load_dotenv(os.path.join(project_folder, '.env'))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_email'] = 'app.dev.test.2020@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
db = SQLAlchemy(app)
mail = Mail(app)
app.secret_key='asdsdfsdfs13sdf_df%&'

# CLASSES
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(120))
    due_date = db.Column(db.String(120))

    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date
    #return "Todo('{}')".format(self.title)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        session['email']=request.form['email']
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect(url_for('index'))

# ROUTES
@app.route('/', methods = ['GET'])
def index():
    if "email" in session and len(session["email"]):
        todos = Todo.query.all()        # get all the todos from the database
        return render_template('base.html', todos=todos)     # todos=todos pass this variable 'todos', and use this variable base.html
    return render_template('login.html')

@app.route("/home",methods = ['GET'])
def home():
    return render_template('login_home.html')
     

@app.route('/add', methods = ['POST'])
def add():
    title = request.form['title']   # gets the title from the form. request is an object that holds the form data
    due_date = request.form['due_date']
    todo = Todo(title=title,due_date=due_date)        # use the Todo class from line 29 to create a todo and save it in a variable

    db.session.add(todo)            # get the todo ready to save
    db.session.commit()             # save todo to the database

    msg = Message('New Task', sender = 'app.dev.test.2020@gmail.com', recipients = [session["email"]])
    msg.body = f"{title}\nDue Date: {due_date}"
    mail.send(msg)
    return redirect('/')            # redirect to the main page 

@app.route('/delete/<string:id_data>', methods = ('POST', 'GET') )
def delete(id_data):
    todo = Todo.query.filter_by(id=id_data).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)





""" *******
   1. How to loop over data in the html file. THere is a variable called 'todos' which is an array. How to display that information in the html file.
     - look for {% %} type stuff when reading about flask
   2. read those articles i sent, your data is called 'todos'
""" 
import os
from flask import jsonify, url_for, redirect, session
from flask import Flask
from flask import render_template
from flask import request
import sqlite3 as sql
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "data.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Consumer(db.Model):   
    TicketID = db.Column(db.Integer, nullable=False, primary_key=True)
    Form = db.Column(db.String(80), nullable=False)
    Method = db.Column(db.String(80), nullable=False)
    Issue = db.Column(db.String(80), nullable=False)
    City = db.Column(db.String(80), nullable=False)
    State = db.Column(db.String(80), nullable=False)
    Zip = db.Column(db.Integer, nullable=False)


@app.route('/')
def homepage():    
    return render_template('index.html')  

@app.route('/game_home')
def game_home():    
    return render_template('home.html')

#Bulk Insert records into in-memory database. 
#Also Add data validation based on your assumptions in html page home.html

@app.route("/add_game", methods=["GET", "POST"])
def add_game():

    if request.form:
        try:
            __tablename__ = 'consumer'
            TicketID=request.form.get("TicketID")
            Form=request.form.get("Form")
            Method= request.form.get("Method")
            Issue= request.form.get("Issue")
            City=request.form.get("City")
            State= request.form.get("State")
            Zip=request.form.get("Zip")
            consume = Consumer(TicketID=TicketID, Form=Form, Method=Method, Issue=Issue, City=City, State=State, Zip=Zip)
            db.session.add(consume)
            db.session.commit()
            print("data inserted sucessfully")
        except Exception as e:
            print("Failed to add list")
    #conss = Consumer.query.all()
    return render_template("out2.html")


@app.route('/search')
def search():    
    return render_template('logon.html')

# Filter and fetch records provided one or all fields. At least one field should be compulsory
@app.route('/searching', methods=["GET", "POST"])
def searching():   
    cons= None

    if request.method =="POST":
        con = sql.connect("data.db")
        cur = con.cursor()
        TicketID=request.form.get("TicketID")
        cur.execute("SELECT * FROM consumer where TicketID = ?", (TicketID, ))
        cons = cur.fetchall()
        con.close()
    return render_template('out.html',cons=cons)
 
           
# complete data of csv load in to Html page
@app.route('/details')
def details():
    con = sql.connect("data.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM consumer")
    cons1 = cur.fetchall()
    con.close()
    return render_template('out1.html',cons1=cons1)


if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=8000, debug=True)


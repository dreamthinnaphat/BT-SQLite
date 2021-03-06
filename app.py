from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With sqlite3
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

#Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):

        self.name = name
        self.email = email
        self.phone = phone

class DataA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(100))

    def __init__(self, Username):

        self.Username = Username

#This is the index route where we are going to
#query on all our employee data
@app.route('/')
def Index():
    all_data = (
        db.session.query(Data.id, Data.name, Data.email, Data.phone, DataA.Username)
        .filter(Data.id == DataA.id)
        .all()
    )
    return render_template("index.html", employees = all_data)

#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        Username = request.form['Username']

        my_data = Data(name, email, phone)
        my_data1 = DataA(Username)
        db.session.add(my_data)
        db.session.add(my_data1)
        db.session.commit()

        flash("Employee Inserted Successfully")

        return redirect(url_for('Index'))

#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':

        my_data = Data.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()
        flash("Employee Updated Successfully")
        return redirect(url_for('Index'))

#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    my_dataA = DataA.query.get(id)
    db.session.delete(my_dataA)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")

    return redirect(url_for('Index'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
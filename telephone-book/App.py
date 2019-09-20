from flask import Flask
from flask import render_template
from flask import request
from flask import redirect , jsonify
import Database as db
from DBClasses import Address, Base, Contact, engine, Phone
import datetime as dt
import json

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    contacts = db.getContacts()
    return render_template("index.html", contacts=contacts, date = dt.datetime)

@app.route("/create", methods=["POST"])
def create():
        try:
            name=request.form.get("name")
            birthDate=request.form.get("birthDate")
            birthDateformater=dt.datetime.strptime(birthDate,'%d/%m/%Y')
            street=request.form.get("street")
            number=request.form.get("number")
            zipCode=request.form.get("zipCode")
            phone=request.form.get("phone")
            contact = Contact(name=name,birthDate=birthDateformater)
            address = Address(street=street,number=number,zipCode=zipCode)
            contact.adresses.append(address)
            phone = Phone(phone=phone)
            contact.phones.append(phone)
            db.insertContact(contact)
        except Exception as e:
            print("Unable to save Contact")
            print(e)
        return redirect("/") 

@app.route("/update", methods=["GET","POST"])
def update():
    try:
        id = request.form.get("id")
        contact = db.getContactById(id)
        name=request.form.get("name")
        birthDate=request.form.get("birthDate")
        birthDateformater=dt.datetime.datetime.strptime(birthDate,'%d/%m/%Y')
        contact.name = name
        contact.birthDate = birthDateformater
        db.putContact(contact)
    except Exception as e:
        print("Unable to update Contact")
        print(e)
    return redirect("/")

@app.route("/delete/<id>", methods=["GET","POST"])
def delete(id):
    try:
        db.deleteContact(id)
    except Exception as e:
        print("Unable to delete Contact")
        print(e)
    return redirect("/")

@app.route("/api/getContactsAsDict", methods=["GET"])
def getContactsAsDict():
    contacts = db.getContactsAsDict()
    return contacts

@app.route("/api/getContactsDict", methods=["GET"])
def getContactsDict():
    contacts = db.getContactsDict(True)
    return contacts

@app.route("/api/getContactById/<id>", methods=["GET"])
def getContactById(id):
    contact = db.getContactById(id)
    data = {
        "birthDate" : dt.datetime.strftime(contact.birthDate, '%d/%m/%Y'),
        "name": contact.name,
    }
    return jsonify(data), 200

@app.route("/api/getContactName/<name>" , methods=["GET"])
def apigetContatoNome(name = None):
    data = []
    for contact in db.getContactByName(name):
        data.append({
            "birthDate": dt.datetime.strftime(contact.birthDate, '%d/%m/%Y'),
            "name": contact.name,
        })
    return jsonify(data), 200

@app.route("/api/getContactAniversario/<month>" , methods=["GET"])
def apigetContatoAniversario(month):
    data = []
    for contact in db.getContactByMes(month):
        data.append({
            "birthDate": dt.datetime.strftime(contact.birthDate, '%d/%m/%Y'),
            "name": contact.name,
        })
    return jsonify(data), 200


if __name__ == "__main__":
    app.run(debug=True)
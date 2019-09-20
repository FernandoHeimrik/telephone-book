from sqlalchemy import create_engine, extract
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import sessionmaker
from DBClasses import Address, Base, Contact, engine, Phone, as_dict
import json

DBSession = sessionmaker(bind=engine)

def insertContact(contact):
    session = DBSession()
    c = contact
    session.add(c)
    session.commit()
    session.close()

def getContacts():
    session = DBSession()
    contacts = session.query(Contact).options(joinedload('adresses'),joinedload('phones')).all()
    session.close()
    return contacts

def putContact(contact):
    session = DBSession()
    c = contact
    session.add(c)
    session.commit()
    session.close()

def deleteContact(id):
    session = DBSession()
    contact = getContactById(id)
    session.delete(contact)
    session.commit()
    session.close()

def getContactById(id):
    session = DBSession()
    contact = session.query(Contact).options(joinedload('adresses'),joinedload('phones')).filter(Contact.id == id).one()
    session.commit()
    session.close()
    return contact

def getContactsAsDict():
    session = DBSession()
    contacts = session.query(Contact).options(joinedload('adresses')).all()
    data = {'contacts' : [ as_dict(contact) for contact in contacts ] }
    session.close()
    return data 

def getContactsDict(adr=True):
    session = DBSession()
    contacts = session.query(Contact).options(joinedload('adresses')).all()
    data = {'contacts' : [ contact.to_dict(adr) for contact in contacts ]}
    session.close()
    return data

def getContactByName(name):
    try:
        session = DBSession()
        obj = session.query(Contact).options().filter(
            Contact.name.like('%'+name+'%')).all()
        session.close()
        return obj
    except:
        print('Error could not be found')

def getContactByMes(month):
    try:
        session = DBSession()
        obj = session.query(Contact).filter(
            extract('month', Contact.birthDate) == month).all()
        session.close()
        return obj
    except:
        print('Error could not be found')

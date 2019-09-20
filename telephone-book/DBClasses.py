import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import inspect

Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    birthDate = Column(Date(), nullable=False)
    adresses = relationship("Address")
    phones = relationship("Phone")

    def to_dict(self, includeAddress=False, includePhones=False):
        data = {
            'id'  : self.id,
            'name': self.name,
            'birthDate': self.birthDate
        }
        if includeAddress :
            data['adresses'] = [ item.to_dict() for item in self.adresses ]
        if includePhones :
            data['phones'] = [ item.to_dict() for item in self.phones ]
        return data

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    street = Column(String(250))
    number = Column(String(250))
    zipCode = Column(String(250), nullable=False)
    contact_id = Column(Integer, ForeignKey('contact.id'))

    def to_dict(self):
        data = {
            'id'  : self.id,
            'street': self.street,
            'number': self.number,
            'zipCode' : self.zipCode
        }
        return data


class Phone(Base):
    __tablename__ = 'phone'
    id = Column(Integer, primary_key=True)
    phone = Column(String(20))
    contact_id 	= Column(Integer, ForeignKey('contact.id'))

    def to_dict(self):
        data = {
            'id'  : self.id,
            'phone': self.phone,
        }
        return data


def as_dict(obj):
    mapper = inspect(obj).mapper
    data = {c.key: getattr(obj, c.key)
            for c in mapper.column_attrs}

    for relation in mapper.relationships :
        if relation.direction.name == 'MANYTOONE' : continue
        items = getattr(obj, relation.key)
        array = []
        for item in items:
            array.append(as_dict(item))
        data[relation.key] = array

    return data

# Cria o engine apontando para o arquivo pessoa.db
engine = create_engine('sqlite:///contacts.db')
#engine = create_engine('mysql://versatek2:aluno123!!@xmysql2.versatek.com.br:3306/versatek2')

# Apaga todas as entradas nas tabelas criadas caso essas existam
#metadata = MetaData()
#for tbl in reversed(Base.metadata.sorted_tables):
#    engine.execute(tbl.delete())

# drop todas as tabelas do metadata
#Base.metadata.drop_all(engine)

# Cria todas as tabelas. Isso e equivalente ao "Create Table" do SQL
Base.metadata.create_all(engine)


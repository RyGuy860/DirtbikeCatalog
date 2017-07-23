import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Manufacture(Base):
    __tablename__ = 'manufacture'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }


class Bikes(Base):
    __tablename__ = 'bikes'

    name = Column(String(20), nullable=False)
    id = Column(Integer, primary_key=True)
    size = Column(String(80), nullable=False)
    description = Column(String(350))
    price = Column(String(12))
    manufacture_id = Column(Integer, ForeignKey('manufacture.id'))
    manufacture = relationship(Manufacture)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'size': self.size,
        }

engine = create_engine('sqlite:///dirtbike.db')

Base.metadata.create_all(engine)

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
class Person(Base):
    __tablename__ = 'personTable'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    contacts = Column(String(100), nullable=False)
    name = Column(String(250), nullable=False)


class Message(Base):
    __tablename__ = 'messageTable'
    # Here we define columns for the message table.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    message_body = Column(String(1000))
    time_stamp = Column(TIMESTAMP,nullable=True)
    person_id = Column(Integer, ForeignKey('personTable.id'))
    person = relationship(Person)


# Create an engine that stores data in the local directory's
# appDatabase.db file.
engine = create_engine('sqlite:///appDatabase.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

#inserting data


engine = create_engine('sqlite:///appDatabase.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
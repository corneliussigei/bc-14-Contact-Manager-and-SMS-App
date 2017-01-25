import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from consumeAfTalkingAPI import FowardMessage

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

#class to insert contacts in db
class AddContacts(Person, Message, Base):
    def __init__(self,name, phone_number):
        self.name=name
        self.phone_number=str(phone_number)
        #function to perfom the data entry
    def insertInformation(self):
        new_person = Person(name=self.name, contacts=self.phone_number)
        session.add(new_person)
        session.commit()
        person = session.query(Person)
        for instance in person:
            print(instance.id, instance.name,"|", instance.contacts)

#class to insert contacts in db
class SendMessage(Person, Message, Base):
    def __init__(self,messsage_recipient, message):
        self.messsage_recipient=messsage_recipient
        self.message=message
        #function to perfom the data entry
    def saveMessage(self):
        new_message = Message(name=self.messsage_recipient, message_body=self.message)
        session.add(new_message)
        session.commit()
        messages = session.query(Message)
        for instance in messages:
            print(instance.person_id, ": ", instance.message_body)

class SearchContact(Person,Base):
    def __init__(self,name):
        self.name=name

    def search(self):
        searchResults = session.query(Person).filter(Person.name.ilike("%"+self.name+"%"))
        total = searchResults.count()
        if(total>1):
            # searchResults.split()
            # askForRequired = input("Which "+self.name+"?")
            for instance in searchResults:
                print(total,". ",instance.name, instance.contacts)
        elif(total==0):
            for instance in searchResults:
                print(total, ". ", instance.name)
        else:
            print("No records found!")

class ContactsSync(Person, Base):
    """"  """

def main():
    pass
commands_help_values = {"add -n <name> -p <contacts>":"Add <name> and <contacts> to the database",
                        "help?":"Check commands and their values",
                        "search <keyword>":"search for a contact and display",
                        "text <name> -m <message>":"send <message> to <name> in the database",
                        "sync contacts":"Sync contacts with Firebase",
                         "exit":"Exit from prgram"}
if __name__ == '__main__':
    main()
    while True:
        userInput = input("%>") #save user input in string variable

        input_words_list = userInput.replace('"','').split()  #split user input string words into list using spaces

        if ((input_words_list[0] == 'add') and (input_words_list[1] == '-n') and (input_words_list[3] == '-p')):
            name = input_words_list[2]
            phone_number = input_words_list[4]
            # Insert a Person in the person table
            a_contacts = AddContacts(name, phone_number)
            a_contacts.insertInformation()
            session.commit()
        elif ((input_words_list[0] == 'search') and (input_words_list[1] != '')):
            search_keyword = input_words_list[1]
            searcher = SearchContact(search_keyword)
            searcher.search()


        elif ((input_words_list[0] == 'text') and (input_words_list[2] == '-m') and (input_words_list[3] != '')):
            name_to_text = input_words_list[1]
            msg = ""
            for i in range(3, len(input_words_list)):
                msg =msg +" " + input_words_list[i]
                # Insert a Person in the person table
            #save_message = SendMessage(name, message_to_send)
            #save_message.saveMessage()
            searchRslts = session.query(Person).filter(Person.name.ilike(name_to_text))
            total = searchRslts.count()
            if total <=0:
                print("The contact name you entered does not exist, please try another name.")
            else:
                for instance in searchRslts:
                    phone_number = instance.contacts
                    forward = FowardMessage(phone_number, msg)
                    forward.getAndSend()



        elif ((input_words_list[0] == 'sync') and (input_words_list[1] == 'contacts')):
            print("Syncing contacts.....")


        elif (input_words_list[0] == 'help?'):
            for key, value in commands_help_values.items():
                print("      ", key, "   :   ", value)

        elif (input_words_list[0] == 'exit'):
            exit()


        else:#if the user enters a wrong command
            print("You entered a wrong command. Please type 'help?' to see valid commands.")

session.close()


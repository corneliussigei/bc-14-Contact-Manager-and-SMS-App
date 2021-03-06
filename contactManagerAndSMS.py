
from CManager_SMS_Model import Person, Message, Base, session
from consumeAfTalkingAPI import FowardMessage
from tabulate import tabulate, tabulate_formats,_table_formats

#class to insert contacts in db
class AddContacts(Person, Message, Base):
    def __init__(self,name, phone_number):
        self.name=name.upper()
        self.phone_number=str(phone_number)
        #function to perfom the data entry
    def insertInformation(self):
        new_person = Person(name=self.name, contacts=self.phone_number)
        session.add(new_person)
        session.commit()
        person = session.query(Person)
        table = [[self.name, self.phone_number]]

        print(tabulate(table, headers = ["Name", "Contact"],tablefmt="grid"))

#class to display all contacts
class ViewContacts(Person,Base):
    def display(self):
        searchResults = session.query(Person).all()
        headers = ["Contact ID", "Contact Name", "Phone Number"]
        table = [[instance.id, instance.name, instance.contacts] for instance in searchResults]
        print(tabulate(table, headers, tablefmt="grid"))


class SearchContact(Person,Base):
    def __init__(self,name):
        self.name=name
    def search(self):
        searchResults = session.query(Person).filter(Person.name.ilike("%"+self.name+"%"))
        total = searchResults.count()
        if(total>1):
            print("Which "+self.name+"?")
            counter = 0
            matching = []
            for instance in searchResults:
                counter+=1
                matching.append("Name: "+instance.name+"  Contacts: "+ instance.contacts)
                name_list = (instance.name).upper().split()
                other_names =list(set(name_list)-set([(self.name).upper()]))
                print("         ["+str(counter)+"]",other_names )
            userChoice = input()
            try:
                choice = int(userChoice) - 1
                if (choice not in range(1, counter)):
                    print("The number you entered is out of range")
                else:
                    print(matching[choice])
            except ValueError:
                print("You entered an invalid choice")

        elif(total==1):
            for instance in searchResults:
                print("Name: " + instance.name + "  Contacts: " + instance.contacts)
        else:
            print("No records found!")

class ContactsSync(Person, Base):
    """" To sync contacts """

def main():
    pass
commands_help_values = {"add -n <1stname_2ndname> -p <contacts>":"Add <name> and <contacts> to the database",
                        "help?":"Check commands and their values",
                        "search <keyword>":"search for a contact and display",
                        "text <name> -m <message>":"send <message> to <name> in the database",
                        "exit":"Exit from prgram",
                        "view all":"Display all contacts that have been added."
                        }
if __name__ == '__main__':
    main()
    table = [[k,v] for k,v in commands_help_values.items()]
    headers = ["Command", "Command Meaning"]
    print("          HELLO, WELCOME TO S&M")
    print("       A CONTACT MANAGER AND SMS APP")
    print(tabulate(table, headers))

    while True:
        userInput = input("%>") #save user input in string variable

        input_words_list = userInput.replace('"','').split()  #split user input string words into list using spaces

        try:
            if ((input_words_list[0] == 'add') and (input_words_list[1] == '-n') and (input_words_list[3] == '-p')):
                try:
                    name = input_words_list[2]
                    names_string = name.replace('_',' ')
                    phone_number = input_words_list[4]
                    # Insert a Person in the person table
                    searchRslts = session.query(Person).filter(Person.name==names_string.upper())
                    total = searchRslts.count()
                    if total<1:
                        a_contacts = AddContacts(names_string, phone_number)
                        a_contacts.insertInformation()
                    else:
                        print("That name already exists in the database. Please use another name.")
                    session.commit()
                except IndexError:
                    print("You did not enter a phone number. Check your command and try again")
            elif ((input_words_list[0] == 'search') and (input_words_list[1] != '')):
                try:
                    search_keyword = input_words_list[1]
                    searcher = SearchContact(search_keyword)
                    searcher.search()
                except IndexError:
                    print("You did not enter a search key word. Check your command and try again")
            elif ((input_words_list[0] == 'view') and (input_words_list[1] == 'all')):
                try:
                    view_obj = ViewContacts()
                    view_obj.display()
                except IndexError:
                    print("Please enter the correct view command.")

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
        except IndexError:
            print("Please enter a full command. Type help? to check valid commands.")

session.close()

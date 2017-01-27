#Contact Manager and SMS Application.
##Description
This is an Andela bootcamp week 2 project. The app is a console Python application that accepts commands from the user to save contacts in a database. The app also enables a user to send messages using commands to a person in the contacts list. It uses AfricasTalking SMS API to send messages. The app also Syncs contacts with FireBase.
##Feature Summary
###Add contacts using commands.
To add contacts in the database, run the contactManagerAndSMS.py file and type the command:
######add -n <1stname_2ndname> -p <contacts>
If the command is properly entered, the the program saves the name in a database table and displays the saved contact, otherwise it displays and appropriate error message.
###Send messages using commands.
To send a message, run the contactManagerAndSMS.py file and type the command:
######text <name> -m <message>
The program sends the message and returns a success message, otherwise it rturns an appropriate error message.

###Search.
To search for a contact run the contactManagerAndSMS.py file and type the command:
######search <keyword>
The program returns a list of all matching records. If the records are more than 1, it asks the user which contact to view. If the record is 1, it
 displays the name and contacts, otherwise it informs the user that no record was found
###View all contacts
To view all contacts in the database, run the contactManagerAndSMS.py file and type the command:
######view all
The program displays all contacts in the database
###Exit the program
The program runs until the user enters "exit". The exit command closes the program.

##Program files
    contactManagerAndSMS.py - controller + views
    consumeAfTalkingAPI.py - Fires the AfricasTalkingGateway into action by calling its send function.
    AfricasTalkingGateway.py - The SMS gateway
    CManager_SMS_Model.py - Model of the project.
    fire_base.py - to sync contacts
    README.md - project summary
    .gitignore - to list files to be ignored


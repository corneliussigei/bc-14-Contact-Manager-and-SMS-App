import os
import sys
from AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException

class FowardMessage(object):
    def __init__(self,phone_number, message):
        self.phone_number = phone_number
        self.message = message
    def getAndSend(self):
        # Specify your login credentials
        username = "corneliussigei"
        apikey = "47e9812f75116188f36aa74037b99ff5f1b22e699712146f90b65b6564178648"

        # Please ensure you include the country code (+254 for Kenya in this case)
        to = self.phone_number
        message =self.message

        # Create a new instance of our awesome gateway class
        gateway = AfricasTalkingGateway(username, apikey)

        try:
            # Thats it, hit send and we'll take care of the rest.

            results = gateway.sendMessage(to, message)

            for recipient in results:
                # status is either "Success" or "error message"
                print('    You message is: %s ' % message)
                print('    You successfully sent the message to: %s'%recipient['number'])
                print('    Status: %s' % recipient['status'])
        except AfricasTalkingGatewayException as e:
            print('Encountered an error while sending: %s' % str(e))

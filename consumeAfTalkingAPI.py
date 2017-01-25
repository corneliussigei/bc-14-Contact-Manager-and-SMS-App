import os
import sys
from africastalking.AfricasTalkingGateway import (AfricasTalkingGateway, AfricasTalkingGatewayException)

# Specify your login credentials
username = "corneliussigei"
apikey = "94de736e83189cc456d7c59273d702212f6209044bc9e2909ef9c1ceaed405bb"

# Please ensure you include the country code (+254 for Kenya in this case)
to      = "+254719221624"

message = "My message"

# Create a new instance of our awesome gateway class
gateway = AfricasTalkingGateway(username, apikey)

try:
    # Thats it, hit send and we'll take care of the rest.

    results = gateway.sendMessage(to, message)

    for recipient in results:
        # status is either "Success" or "error message"
        print('number=%s;status=%s;messageId=%s;cost=%s' %(recipient['number'],
                                                        recipient['status'],
                                                        recipient['messageId'],
                                                        recipient['cost']))
except AfricasTalkingGatewayException:
    print('Encountered an error while sending: %s' % str(AfricasTalkingGatewayException))
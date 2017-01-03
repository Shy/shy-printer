from Adafruit_Thermal import *

from flask import Flask, request
from twilio import twiml

import textwrap
import csv
import re
import arrow

printer = Adafruit_Thermal("/dev/ttyS0", 19200, timeout=5)

app = Flask(__name__)


@app.route('/sms', methods=['POST'])
def sms():
    contact_list = []
    with open('assets/contacts.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
                contact_list.append(line)

    number = re.sub("\D", "", request.form['From'])
    for item in contact_list:
        if item['Phone'] == number:
            sender = '{} {}'.format(item['First'],item['Last'])
            break
    else:
        sender = number
    timestamp = arrow.now().format('M/D/YY h:mm A')

    message_body = textwrap.wrap(request.form['Body'],32)

    printer.boldOn()
    printer.underlineOn(2)
    printer.println("{}-{}".format(sender,timestamp))
    printer.boldOff()
    printer.underlineOff()

    for line in message_body:
        printer.println(line)
    printer.println("\n")

    resp = twiml.Response()
    resp.message('From {} Printing: {}'.format(sender,message_body))
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)


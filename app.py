from Adafruit_Thermal import *

from flask import Flask, request
from twilio import twiml
import textwrap

printer = Adafruit_Thermal("/dev/ttyS0", 19200, timeout=5)

app = Flask(__name__)


@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']

    resp = twiml.Response()
    resp.message('Printing: {}'.format(textwrap.wrap(message_body,32)))

    printer.boldOn()
    printer.underlineOn(2)
    printer.println(number)
    printer.boldOff()
    printer.underlineOff()

    for line in message_body:
        printer.print(line + "\n")

    return str(resp)

if __name__ == '__main__':
    app.run()


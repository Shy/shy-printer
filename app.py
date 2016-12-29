from Adafruit_Thermal import *

from flask import Flask, request
from twilio import twiml

printer = Adafruit_Thermal("/dev/ttyS0", 19200, timeout=5)

app = Flask(__name__)


@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']

    resp = twiml.Response()
    resp.message('Printing: {}'.format(message_body))

    printer.boldOn()
    printer.underlineOn(2)
    printer.print(number)
    printer.setDefault()
    printer.println(message_body)

    return str(resp)

if __name__ == '__main__':
    app.run()

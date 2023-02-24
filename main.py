from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import re
from escpos.printer import Network
import base64

app = Flask(__name__)
CORS(app)


@app.route('/text/<addr>', methods=['GET','POST'])
def print_text(addr):
    data, printer, message = setup_for_command(request, addr)
    if message:
        return message
    printer.text(data)
    cut(printer=printer)
    return jsonify(message="Success!", code=200)

@app.route('/block/<addr>', methods=['GET','POST'])
def print_block(addr):
    data, printer, message = setup_for_command(request, addr)
    if message:
        return message
    printer.block_text(data)
    cut(printer=printer)
    return jsonify(message="Success!", code=200)

@app.route('/img/<addr>', methods=['GET','POST'])
def print_img(addr):
    data, printer, message = setup_for_command(request, addr, data_type="img")
    if message:
        return message
    printer.image(data)
    cut(printer=printer)
    return jsonify(message="Success!", code=200)

@app.route('/status/<addr>', methods=['GET'])
def print_status(addr):
    try:
        cut(addr=addr, request=request)
        return jsonify(message="Success!", code=200)
    except:
        return jsonify(message="Error!", code=500)

@app.route('/cut/<addr>', methods=['GET'])
def print_cut(addr):
    return cut(addr=addr, request=request)

def cut(printer=False, addr=False, request=False):
    if printer:
        return printer.cut()
    data, printer, message = setup_for_command(request, addr)
    printer.cut()
    return jsonify(message="Success!", code=200)
    
def setup_for_post_command(request, addr, data_type="txt"):
    if request.method != 'POST':
        return False, False, jsonify(message="This should be used with POST method.", code=405)
    return setup_for_command(request, addr, data_type)

def setup_for_post_command(request, addr, data_type="txt"):
    if request.method != 'GET':
        return False, False, jsonify(message="This should be used with GET method.", code=405)
    return setup_for_command(request, addr, data_type)

def setup_for_command(request, addr, data_type="txt"):
    if not validate_address(addr):
        return False, False, jsonify(message="Not a valid url or ip address.", code=406)

    data = get_data(request.data, data_type)
    printer = create_network(addr)

    if not printer:
        return False, False, jsonify(message="Error ocurred", code=504)
    app.logger.info(data or "no data")
    if printer and not data:
        try:
            printer.cut()
        except:
            return False, False, jsonify(message="No connection could be made to the address.", code=406)
        
        return False, False, jsonify(message="Printer found on ip: %s" % addr, code=202)
    
    return data, printer, False

def get_data(data, data_type):
    try:
        if data_type == "txt":
            return str(data.decode('utf-8'))
        app.logger.info(data)
        imgdata = base64.b64decode(data)
        filename = "temp_receipt.jpg"
        with open(filename, 'wb') as f:
            app.logger.info(filename)
            f.write(imgdata)
        return filename
    except:
        return False

def create_network(addr):
    try:
       printer = Network(addr)
       return printer
    except TimeoutError:
        return False

def validate_address(addr):
    regex = re.compile(
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, addr)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
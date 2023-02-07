from flask import Flask, request, jsonify, make_response
import re
from escpos.printer import Network
import base64

app = Flask(__name__)


@app.route('/text/<addr>', methods=['GET','POST'])
def print_text(addr):
    data, printer, message = setup_for_command(request, addr)
    if message:
        return message
    printer.text(data)
    cut(printer=printer)
    return _corsify_actual_response(jsonify(message="Success!", code=200))

@app.route('/block/<addr>', methods=['GET','POST'])
def print_block(addr):
    data, printer, message = setup_for_command(request, addr)
    if message:
        return message
    printer.block_text(data)
    cut(printer=printer)
    return _corsify_actual_response(jsonify(message="Success!", code=200))

@app.route('/img/<addr>', methods=['GET','POST'])
def print_img(addr):
    data, printer, message = setup_for_command(request, addr, data_type="img")
    if message:
        return message
    printer.image(data)
    cut(printer=printer)
    return _corsify_actual_response(jsonify(message="Success!", code=200))

@app.route('/cut/<addr>', methods=['GET','POST'])
def print_cut(addr):
    return cut(addr=addr, request=request)

def cut(printer=False, addr=False, request=False):
    if printer:
        return printer.cut()
    data, printer, message = setup_for_command(request, addr)
    printer.cut()
    return _corsify_actual_response(jsonify(message="Success!", code=200))
    

def setup_for_command(request, addr, data_type="txt"):
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    app.logger.info(validate_address(addr))
    if not validate_address(addr):
        return False, False, _corsify_actual_response(jsonify(message="Not a valid url or ip address.", code=406))

    if request.method != 'POST':
        return False, False, _corsify_actual_response(jsonify(message="This should be used with post method.", code=405))

    data = get_data(request.data, data_type)
    printer = create_network(addr)

    if not printer:
        return False, False, _corsify_actual_response(jsonify(message="Error ocurred", code=504))

    if printer and not data:
        try:
            printer.cut()
        except:
            return False, False, _corsify_actual_response(jsonify(message="No connection could be made to the address.", code=406))
        
        return False, False, _corsify_actual_response(jsonify(message="Printer found on ip: %s" % addr, code=202))
    
    return data, printer, False

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "localhost")
    response.headers.add('Access-Control-Allow-Headers', "localhost")
    response.headers.add('Access-Control-Allow-Methods', "localhost")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "localhost")
    response.headers.add('Access-Control-Allow-Headers', "localhost")
    response.headers.add('Access-Control-Allow-Methods', "localhost")
    return response

def get_data(data, data_type):
    try:
        if data_type == "txt":
            return str(data.decode('utf-8'))
        data = data.replace(' ', "+")
        imgdata = base64.b64decode(data)
        filename = "temp_receipt.jpg"
        with open(filename, 'wb') as f:
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
    app.run(debug=True)
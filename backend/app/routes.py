from flask.helpers import send_file, send_from_directory
from app import app
import os
from flask import jsonify

@app.route('/')
@app.route('/index')
def index():
    return 'Hello World'

'''Endpoint to list the currect sleepcasts'''
@app.route('/files')
def list_files():
    files = []
    for filename in os.listdir('app/assets/sleepcasts'):
        path = os.path.join('app/assets/sleepcasts', filename)
        if os.path.isfile(path):
            files.append(filename)
    return(jsonify(files))

'''Endpoint to Download specific file'''
@app.route('/files/<path:filename>', methods=['GET', 'POST'])
def get_file(filename):
    return send_from_directory(app.config['SLEEPCAST_DIRECTORY'], filename, as_attachment=True)


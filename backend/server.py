'''
A flask server for the backend of the 'helpr' application.

GET routes are passed arguments as URL parameters. POST and DELETE routes are
passed arguments as JSON data in the body of the request. All routes return data
as JSON.
'''

from flask import Flask, request
from flask_cors import CORS

from werkzeug.exceptions import BadRequest

from json import dumps

import config
import helpr

APP = Flask(__name__)
CORS(APP)

@APP.route('/make_request', methods=['POST'])
def make_request():
    '''
    A route for helpr.make_request()

    Params: {"zid", "description"}

    Raises: BadRequest if helpr.make_request() raises a KeyError or ValueError.

    Returns: {}
    '''
    input_data = request.get_json()
    zid = input_data['zid']
    description = input_data['description']
    try:
        helpr.make_request(zid,description)
    except (KeyError,ValueError):
        raise BadRequest
    return dumps({})

@APP.route('/queue', methods=['GET'])
def queue():
    '''
    A route for helpr.queue()

    Returns: A list in the same format as helpr.queue()
    '''
    result = helpr.queue()
    return dumps(result)

@APP.route('/remaining', methods=['GET'])
def remaining():
    '''
    A route for helpr.remaining()

    Params: ("zid")

    Raises: BadRequest if helpr.remaining() raises a KeyError.

    Returns: { 'remaining': n } where n is an integer
    '''
    zid = request.args.get('zid')
    try:
        result = helpr.remaining(zid)
    except KeyError:
        raise BadRequest
    return dumps({
        'remaining': result, 
    })

@APP.route('/help', methods=['POST'])
def help():
    '''
    A route for helpr.help()

    Params: {"zid"}

    Raises: BadRequest if helpr.help() raises a KeyError.

    Returns: {}
    '''
    input_data = request.get_json()
    zid = input_data['zid']
    try:
        helpr.help(zid)
    except KeyError:
        raise BadRequest    
    return dumps({})

@APP.route('/resolve', methods=['DELETE'])
def resolve():
    '''
    A route for helpr.resolve()

    Params: {"zid"}

    Raises: BadRequest if helpr.resolve() raises a KeyError.

    Returns: {}
    '''
    input_data = request.get_json()
    zid = input_data['zid']
    try:
        helpr.resolve(zid)
    except KeyError:
        raise BadRequest
    return dumps({})

@APP.route('/cancel', methods=['DELETE'])
def cancel():
    '''
    A route for helpr.cancel()

    Params: {"zid"}

    Raises: BadRequest if helpr.cancel() raises a KeyError.

    Returns: {}
    '''
    input_data = request.get_json()
    zid = input_data['zid']
    try:
        helpr.cancel(zid)
    except KeyError:
        raise BadRequest
    return dumps({})

@APP.route('/revert', methods=['POST'])
def revert():
    '''
    A route for helpr.revert()

    Params: {"zid"}

    Raises: BadRequest if helpr.revert() raises a KeyError.

    Returns: {}
    '''
    input_data = request.get_json()
    zid = input_data['zid']
    try:
        helpr.revert(zid)
    except KeyError:
        raise BadRequest
    return dumps({})

@APP.route('/reprioritise', methods=['POST'])
def reprioritise():
    '''
    A route for helpr.reprioritise()

    Returns: {}
    '''
    helpr.reprioritise()
    return dumps({})

@APP.route('/end', methods=['DELETE'])
def end():
    '''
    A route for helpr.end()

    Returns: {}
    '''
    helpr.end()
    return dumps({})

if __name__ == "__main__":
    # Run the Flask webserver.
    # Listen for all requests to localhost at config.PORT.
    APP.run(port=config.PORT, debug=True)
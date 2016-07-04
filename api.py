import eventlet
eventlet.monkey_patch()

from flask import Flask, request
import requests
import traceback

import eventlet.wsgi

from create_terrain_objects import save_terrain, create_or_update_terrain_object, get_all_food, get_all_obstacles

app = Flask(__name__)

# microservices_urls = {
#   'socket':'http://localhost:9000',
#   'terrain': 'http://159.203.226.234',
#   'field_objects': 'http://192.241.215.101', 
# }
microservices_urls = {
    'socket': 'http://104.236.155.241',
    'terrain': 'http://159.203.226.234:7000',
    'field_objects': 'http://192.241.215.101:7001',
}
@app.route('/')
def test_connect():
    return "connected to objects service"

@app.route('/terrain_objects', methods=['GET'])
def get_terrain_objects():
    requests.post(microservices_urls["socket"]+'/send_field_objects', json ={'food':get_all_food(), 'obstacles': get_all_obstacles()})
    return 'OK'

@app.route('/update_object', methods=['GET'])
def update_object():
    objId = request.args.get('id')
    objType = request.args.get('type')
    data = create_or_update_terrain_object(objType, objId)
    return data

@app.route('/store_terrain', methods=['POST'])
def save_landscape():
    height = 250
    width = 250
    save_terrain(height, width, request.json["terrain"])
    return 'Ok'

    
# error handling
@app.errorhandler(500)
def internal_error(exception):
    """Show traceback in the browser when running a flask app on a production server.
    By default, flask does not show any useful information when running on a production server.
    By adding this view, we output the Python traceback to the error 500 page.
    """
    trace = traceback.format_exc()
    return("<pre>" + trace + "</pre>"), 500

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 7001)), app, debug=True)

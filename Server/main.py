from flask import Flask, abort, request
from flask_cors import CORS
from pymongo import MongoClient, cursor
from bson.objectid import ObjectId
from geopy import distance as geopy_d

#region Constants
HUB_RADIUS = 5	# Radius/size of any given hub, written in feet
DEBUG = False

#endregion

#region Server Handling, Logging, and Initialization
def make_logger(file):
    def log(message):
        if DEBUG:
            with open(file, 'a') as f:
                f.write(message)
    def clear():
        with open(file, 'w') as f:
            f.write('')
    log.clear = clear
    return log

log = make_logger('log.txt')
log('Launched server.\n')

def start_db(*hostargs):
    client = MongoClient(*hostargs)
    db = client.moment_db
    users = db.users
    hubs = db.hubs
    return client, db, users, hubs

app = Flask(__name__)
client, db, users, hubs = start_db('localhost', 27017)

#endregion

#region Helpers and Utilities
def queryargs(*argnames):
    def querydecorator(func):
        def wrapper(*args):
            #assert len(argnames) == len(args), 'The number of querystring parameter names must be same as the number of parameters to take in.'
            qAs = [request.args.get(name) for name in argnames]
            log(f'For {func.__name__}: argnames: {argnames}\tqAs: {qAs}\n')
            return func(*qAs)
        wrapper.__name__ = func.__name__
        return wrapper
    return querydecorator

#endregion

@app.route('/clear_log', methods=['POST'])
def clear_log():
    log.clear()
    return ''

#region Hubs
@app.route('/all_hubs', methods=['GET'])
def get_all_hubs():
    result = hubs.find({})
    return str([hub for hub in result])

@app.route('/get_hubs', methods=['GET'])
@queryargs('lat', 'lon', 'radius')
def get_hubs(lat, lon, radius):
    hub_cursor = hubs.find({})
    nearby_hubs = []
    for doc in hub_cursor:
        try:
            dist = geopy_d.distance((doc['location'][0], doc['location'][1]), (lat, lon)).ft
            if dist <= radius:
                nearby_hubs.append(doc)
        except BaseException as e:
            return f'Error: {e}'
    return str(nearby_hubs)

@app.route('/get_hub', methods=['GET'])
@queryargs('id')
def get_hub(id):
    result = hubs.find_one({'_id': ObjectId(id)})
    return str(result)

@app.route('/create_hub', methods=['POST'])
@queryargs('root', 'palette_types', 'lat', 'lon')
def create_hub(root, palette_types, lat, lon):
    # Check for hubs that are too nearby
    hub_cursor = hubs.find({})
    for doc in hub_cursor:
        try:
            dist = geopy_d.distance((doc['location'][0], doc['location'][1]), (lat, lon)).ft
            if (dist < HUB_RADIUS):
                return f'Bad hub location; too close to hub {doc["_id"]}.'
        except BaseException as e:
            return f'Error: {e}'
    # If not too nearby, then add new hub
    hub_data = {
        'root_node': root,
        'palette_types': palette_types,
        'location': [lat, lon],
        'items': []
    }
    result = hubs.insert_one(hub_data)
    return str(result.inserted_id)

@app.route('/add_item', methods=['POST'])
@queryargs('hub_id', 'item')
def add_item(hub_id, item):
    result = hubs.update(
        { '_id': ObjectId(hub_id) },
        { '$push': { 'items': item } }
    )
    return str(result)

#endregion

#region Users
# TODO: Handle login using Google
# All of this code is likely somewhat irrelevant at this point--it'll all depend on Google auth stuff
@app.route('/create_user', methods=['POST'])
@queryargs('username')
def create_user(username):
    user_data = {
        'username': username,
        'hubs_created': [],
        'hubs_visited': []
    }
    result = users.insert_one(user_data)
    return result.inserted_id

@app.route('/login', methods=['POST'])
@queryargs('username', 'password')
def login(username, password):
    raise NotImplementedError()

@app.route('/get_user', methods=['GET'])
@queryargs('id')
def get_user(id):
    raise NotImplementedError()

#endregion

#region Todos
# TODO: For right now, we need...
# - Find way to handle latitude and longitude difference (implement distance function)
# - Implement checking of proper location in create_hub
# - Write functions for updating (not just creating for getting) data
# - Implement user authentication (including authentication for adding or changing a hub--must be a valid user to change things)
#	- Can take lazy route and just have users be based on username login for now
# 	- Or make login based on Google or Facebook account (preferred option!)
#		- Look into this integration
# - Test integration with sending over SCNNode objects from Swift--what displays on the backend? What is the datatype? How do we add it to our DB without things breaking?

# TODO: Later in scope (ignore for now)
# Other things we'll need to be able to do but seem more like they belong on the frontend:
# - Get the route from where user is to a desired hub (Actually, this could very well be a backend thing! Depends on how Google Maps works.)
# - Render the hub and all of its items
# 	- So as it turns out, we'll need to store a hub as a single rootNode. We'll want to do this so that we can build the actual scene with its lighting on the frontend; the scene's items should be stored in the database.
# - Create the scene for the hub
# - Aggregate all of the items into a scene and render it

#endregion
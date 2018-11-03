from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

# Constants
HUB_RADIUS = 5	# Radius/size of any given hub, written in feet

#region Server Handling
def start_db(*hostargs):
	client = MongoClient(*hostargs)
	db = client.moment_db
	users = db.users
	hubs = db.hubs
	return client, db, users, hubs

#endregion

#region Hubs
@Flask.route('/get_hubs', 'GET')
def get_hubs(lat, lon, radius):
	raise NotImplementedError()

@Flask.route('/get_hub', 'GET')
def get_hub(id):
	result = hubs.find({'_id': id})
	return result[0]

@Flask.route('/create_hub', 'POST')
def create_hub(scene_root, palette_types, lat, lon):
	# TODO: Create handling for hub that already exists too nearby (use queries!).
	hub_data = {
		'root_node': scene_root,
		'palette_types': palette_types,
		'location': [lat, lon],
		'items': []
	}
	result = hubs.insert_one(hub_data)
	return result.inserted_id

@Flask.route('/add_item', 'POST')
def add_item(hub_id, item):
	result = hubs.update(
		{ '_id': hub_id },
		{ '$push': { 'items': item } }
	)
	return result # NOTE: What does this result actually return?

#endregion

#region Users
# TODO: Handle login using Google
# All of this code is likely somewhat irrelevant at this point--it'll all depend on Google auth stuff
@Flask.route('/create_user', 'POST')
def create_user(username):
	user_data = {
		'username': username,
		'hubs_created': [],
		'hubs_visited': []
	}
	result = users.insert_one(user_data)
	return result.inserted_id

@Flask.route('/login', 'POST')
def login(username, password):
	raise NotImplementedError()

@Flask.route('/get_user', 'GET')
def get_user(id):
	raise NotImplementedError()

#endregion

#region Helpers and Utilities
class Location:
	def __init__(self, lat: int, lon: int):
		self.lat = lat
		self.lon = lon

def distance(l1: Location, l2: Location):
	'''Determines the distance between two Locations in feet.'''
	raise NotImplementedError()

#endregion

client, db, users, hubs = start_db('localhost', 27017)

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

from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

def start_db(*hostargs):
	client = MongoClient(*hostargs)
	db = client.moment_db
	users = db.users
	hubs = db.hubs
	return client, db, users, hubs

@Flask.route('/get_hubs', 'GET')
def get_hubs(location, radius):
	raise NotImplementedError()

@Flask.route('/get_hub', 'GET')
def get_hub(id):
	raise NotImplementedError()

@Flask.route('/create_hub', 'POST')
def create_hub(scene_root, palette_types):
	hub_data = {
		'root_node': scene_root,
		'palette_types': palette_types
	}
	result = hubs.insert_one(hub_data)
	return result.inserted_id

@Flask.route('/add_item', 'POST')
def add_item(hub, item):
	raise NotImplementedError()

@Flask.route('/get_user', 'GET')
def get_user(id):
	raise NotImplementedError()

@Flask.route('/create_user', 'POST')
def create_user(username):
	user_data = {
		'username': username,
		'hubs_created': [],
		'hubs_visited': []
	}
	result = users.insert_one(user_data)
	return result.inserted_id

client, db, users, hubs = start_db('localhost', 27017)

# Other things we'll need to be able to do but seem more like they belong on the frontend:
# - Get the route from where user is to a desired hub (Actually, this could very well be a backend thing! Depends on how Google Maps works.)
# - Render the hub and all of its items
# 	- So as it turns out, we'll need to store a hub as a single rootNode. We'll want to do this so that we can build the actual scene with its lighting on the frontend; the scene's items should be stored in the database.
# - Create the scene for the hub
# - Aggregate all of the items into a scene and render it

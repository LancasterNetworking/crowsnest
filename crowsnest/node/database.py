import pymongo

from crowsnest import config

connection = pymongo.Connection(config.database['host'], int(config.database['port'])) 
database = connection[config.database['name']]

def get_collections():
	return database.collection_names(include_system_collections=False)

def write_to_collection(collection_name, record):
	collection = database[collection_name]
	collection.insert(record)

def find(collection_name, projection={}, limit=0, sort_order=pymongo.ASCENDING):
	collection = database[collection_name]
	return collection.find({}, projection, limit=limit).sort('timestamp', sort_order)
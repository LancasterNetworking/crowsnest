from pymongo import Connection

from crowsnest import config

connection = Connection(config.database['host'], int(config.database['port'])) 
database = connection[config.database['name']]

def get_collections():
	global database
	database.collection_names(include_system_collections=False)

def write_to_collection(collection_name, record):
	global database
	collection = database[collection_name]
	collection.insert(record)
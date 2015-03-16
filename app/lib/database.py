from crowsnest import config
from pymongo import Connection

def _open_connection():
	connection = Connection(config.database['host'], int(config.database['port']))
	return connection

def open_database(database_name=config.database['name']):
	connection = _open_connection()
	return connection[database_name]

def write_to_collection(database, collection_name, data):
	collection = database[collection_name]
	collection.insert(data)
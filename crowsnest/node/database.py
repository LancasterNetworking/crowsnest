import pymongo

from crowsnest import config

connection = pymongo.Connection(config.database['host'], int(config.database['port'])) 
database = connection[config.database['name']]

def get_collections():
	""" Find all collections available in the configured database """
	return database.collection_names(include_system_collections=False)

def write_to_collection(collection_name, record):
	""" Store a record in a given collection """
	collection = database[collection_name]
	collection.insert(record)

def find(collection_name, projection={}, limit=0, sort_order=pymongo.ASCENDING):
	""" Finds records in a given collection
 	
 	Args:
 		collection_name: the name of the collection where you will search for records
 		projection: a dict of the fields you wish to [not] display, e.g
 			{'file_': 1, 'timstamp': 1} where find will only return the fields 'timestamp'
 			and 'file_' from all found records
 		limit: the maximum number of records returned
 		sort_order: the order in which the records are sorted when returned

 	Returns:
 		A list of dicts of all the records that matched the calling parameters, e.g
			[
				{
			  		"timestamp": 1426522232,
			  		"file_": "bunny_2s1.m4s",
				},
				...
			]
	"""

	projection['_id'] =  0
	collection = database[collection_name]
	return collection.find({}, projection, limit=limit).sort('timestamp', sort_order)
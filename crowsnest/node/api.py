import threading

import pymongo
from bson.json_util import dumps
from flask import Flask, url_for, jsonify, request

from crowsnest import config
from crowsnest.node import database

app = Flask(__name__)

@app.route('/')
def api_root():
	return 'Welcome'

@app.route('/api/sessions')
def api_sessions():
	collections = database.get_collections()
	return jsonify(sessions=collections)

@app.route('/api/sessions/<path:id_>')
def api_specific_sessions(id_):
	sessions = set(id_.split(','))

	fields = request.args.get('fields')
	if fields:
		fields = fields.split(',')
		for field in fields:
			projection[field] = 1

	most_recent = request.args.get('mostRecent')
	print str(request.args)
	if most_recent:
		limit = 1
		sort_order = pymongo.DESCENDING
	else:
		limit = 0
		sort_order = pymongo.ASCENDING

	collections = database.get_collections()

	response = {}
	for session in sessions:
		if session in collections:
			response[session] = list()
			for document in database.find(session, projection, limit=limit, sort_order=sort_order):
				response[session].append(document)

	return dumps(response)

class api_thread(threading.Thread):
	daemon = True
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		app.run(host=config.api['host'], port=config.api['port'])
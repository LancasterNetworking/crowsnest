from threading import Thread, Timer
from time import sleep

import gevent
from flask import Flask, render_template, jsonify, copy_current_request_context
from flask.ext.socketio import SocketIO, emit

from crowsnest import config
from crowsnest.node import database

app = Flask(__name__)
socketio = SocketIO(app)

broadcaster = None

@app.route('/')
def homepage():
	return render_template('index.html', sessions=database.get_collections())

@socketio.on('my event')
def test_message(message):
	@copy_current_request_context
	def background_thread():
		while(True):
			emit('my response', {'data': '42'}, broadcast=True)
			sleep(3)

	global broadcaster
	if broadcaster is None:
		print 'i made a new thread'
		broadcaster = Thread(target=background_thread)
		broadcaster.start()
	else:
		print 'no need for a new thread'

@socketio.on('disconnect')
def test_disconnect():
    print 'client disconnected'

class webserver_thread(Thread):
	daemon = True
	def __init__(self):
		Thread.__init__(self)
	
	def run(self):
		socketio.run(app, host=config.gui['host'], port=config.gui['port'])
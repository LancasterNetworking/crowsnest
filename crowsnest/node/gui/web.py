from threading import Thread, Timer
from time import sleep
import pprint

from flask import Flask, render_template, jsonify, copy_current_request_context
from flask.ext.socketio import SocketIO, emit

from crowsnest import config
from crowsnest.node import database

app = Flask(__name__)
socketio = SocketIO(app)

broadcaster = None
manager = None

@app.route('/')
def homepage():
	return render_template('index.html')

@socketio.on('client connected')
def test_message(message):
	emit('my response', {'sessions': database.get_collections()})
	@copy_current_request_context
	def background_thread():
		while(True):
			emit('my response', {'sessions': database.get_collections()}, broadcast=True)
			sleep(3)

	global broadcaster
	if broadcaster is None:
		broadcaster = Thread(target=background_thread)
		broadcaster.start()

@socketio.on('disconnect')
def test_disconnect():
    print 'client disconnected'

@socketio.on('session_changed')
def session_changed(message):
	minimum = manager.find_bitrate_stats(message['session'], 'min')
	emit('bitrate_stats', {'minimum': minimum})

	average = manager.find_bitrate_stats(message['session'], 'avg')
	emit('bitrate_stats', {'average': average})

	maximum = manager.find_bitrate_stats(message['session'], 'max')
	emit('bitrate_stats', {'maximum': maximum})

	range_ = manager.find_bitrate_stats(message['session'], 'range')
	emit('bitrate_stats', {'range': range_})

	timeseries = manager.get_timeseries_data(message['session'], 'bitrate')
	emit('timeseries', {'bitrate': timeseries})

	timeseries = manager.get_timeseries_data(message['session'], 'height')
	emit('timeseries', {'height': timeseries})

	timeseries = manager.get_timeseries_data(message['session'], 'width')
	emit('timeseries', {'width': timeseries})

	timeseries= manager.get_video_quality(message['session'])
	emit('timeseries', {'quality': timeseries})

class webserver_thread(Thread):
	daemon = True
	def __init__(self, _manager):
		global manager
		manager = _manager
		Thread.__init__(self)
	
	def run(self):
		socketio.run(app, host=config.gui['host'], port=config.gui['port'])
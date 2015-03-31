import re
import os
import requests
import json
from time import sleep

from pymongo import Connection

import sniffer
import api
import engine
from gui import web
from mpd_parser import Parser
from session import Session
from crowsnest import config
from crowsnest.node import database

class Manager(object):
    sessions = {}
    path_to_mpds = 'mpds/'

    def __init__(self):
        """ Start crowsnest and its various services """
        sniff = sniffer.sniffing_thread(self)
        sniff.start()

        _api = api.api_thread()
        _api.start()

        gui = web.webserver_thread(self)
        gui.start()
        while(1):
            self.check_for_expired_sessions()
            sleep(5)

    def handle_mpd_request(self, request):
        """ Hand off processing of packets requesting MPD files """ 
        if not self.file_available_locally(self.path_to_mpds + request.file_):
            self.get_file(request.host + request.path)
        self.new_session(request)

    def file_available_locally(self, file_):
        """ True/False if a file is available on the local filesystem """
        path = ""
        for split in file_.split('/')[:-1]:
            path = path + split + "/"
        if not os.path.exists(path):
            os.makedirs(path)
        return os.path.isfile(file_)

    def get_file(self, url):
        """ Request a file from a remote location, typically used for
        downloading remote MPD files to be parsed later """
        file_ = url.split('/')[-1]

        with open(self.path_to_mpds + file_, 'wb') as handle:
            if not "http" in url:
                url = 'http://' + url
            response = requests.get(url, verify=False, allow_redirects=True, stream=True)

            if not response.ok:
                return

            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)

    def send_data_to_engine(self):
        r = requests.get('http://' + config.api['host'] + ':' + str(config.api['port']) + '/api/sessions')
        response = json.loads(r.text)

        for session in response['sessions']:
            r = requests.get('http://' + config.api['host'] + ':' + str(config.api['port']) + '/api/sessions/' + session + '?fields=timestamp,duration,bitrate,width,height')
            print r.text
            entries = json.loads(r.text)
            data = []
            for entry in entries:
                for document in entries[entry]:
                    data.append(document)
            engine.test_add_videoTime(data)

    def find_bitrate_stats(self, session_identifier, method):
        """ Wraps the engine call of the same name """
        documents = database.find(session_identifier, {'bitrate': 1})
        result = engine.find_bitrate_stats(documents, method)
        return result

    def get_timeseries_data(self, session_identifier, metric):
        """ Wraps the engine call of the same name """
        documents = database.find(session_identifier, {metric: 1, 'timestamp': 1})
        data_points = list()
        for document in documents:
            data_points.append([document['timestamp'], document[metric]])
        return data_points

    def get_video_quality(self, session_identifier):
        documents = database.find(session_identifier, {'height': 1, 'bitrate': 1, 'timestamp': 1})
        video_quality = engine.calc_videoQuality(documents)
        return video_quality

    def handle_m4s_request(self, request):
        """ Find the correct session that this m4s belongs to,
        and then write get request information to the database """ 
        session_identifier = self.find_session_identifier(request)
        if session_identifier is None:
            print 'cant find a session for this m4s request, has the client requested an mpd first?'
            return
        session = self.sessions[session_identifier]
        session.reset_time_since_last_update()

        key = request.path
        key = key.split('/')[-2] + '/' + key.split('/')[-1]

        entry = dict(request.__dict__.items() + session.mpd[key].items())
        bitrate = self.get_playback_bitrate(entry['path'])
        entry['bitrate'] = bitrate

        database.write_to_collection(session_identifier, entry)

    def new_session(self, request):
        """ Create a new user session by using data extracted
        from the HTTP request packet """
        parser = Parser(self.path_to_mpds + request.file_)
        mpd = parser.mpd
        session = Session(request.src_ip, request.host, mpd, request.timestamp)
        session_identifier = self.create_session_identifier(request)
        self.sessions[session_identifier] = session

    def create_session_identifier(self, request):
        """ Find a suitable identifier for each request """
        return str(request.src_ip) + ' ' + str(request.host) + ' ' + str(request.timestamp)

    def find_session_identifier(self, request):
        newest_session = None
        newest_timestamp = 0
        for session in self.sessions:
            (src_ip, destination, timestamp) = tuple(session.split(' '))
            if src_ip == request.src_ip and destination == request.host:
                if timestamp > newest_timestamp:
                    newest_timestamp = timestamp
                    newest_session = session
        return newest_session

    def check_for_expired_sessions(self):
        """ Expire sessions if they exceed the configured expirey time """
        for session in self.sessions:
            if self.sessions[session].time_since_last_update >= config.sessions['expirey_time']:
                self.sessions[session].end_session()

    def get_playback_bitrate(self, url):
        """Parse the URL to unreliably(!) determine the playback bitrate."""
        pattern = re.compile(ur'.*\_(.*kbit).*')
        match = re.match(pattern, url)
        bitrate = int(match.group(1).replace('kbit', ''))
        return bitrate or 0
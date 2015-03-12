from threading import Timer

class Session(object):
    def __init__(self, src_ip, host, mpd, start_time):
        self.mpd = mpd
        self.host = host
        self.src_ip = src_ip
        self.start_time = start_time
        self.time_since_last_update = 0
        self.rt = RepeatedTimer(1, self.increment_time_since_last_update)

    def increment_time_since_last_update(self):
    	self.time_since_last_update = self.time_since_last_update + 1

    def reset_time_since_last_update(self):
    	self.time_since_last_update = 0

    def end_session(self):
    	self.rt.stop()

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.daemon = True
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
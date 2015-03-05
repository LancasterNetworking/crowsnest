class Session(object):
    def __init__(self, mpd, start_time):
        self.mpd = mpd
        self.start_time = start_time
        self.elapsed_time = 0
class Listener:
    def __init__(self, port, host, backlog=1000):
        self.port = port
        self.host = host
        self.backlog = backlog

    def __repr__(self):
        return str(host)

    def start(self):
        pass

    def stop(self):
        pass

    def accept(self):
        pass

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.stop()

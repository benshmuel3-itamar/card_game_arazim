from connection import Connection
import socket


class Listener:
    def __init__(self, port, host, backlog=1000):
        self.port = port
        self.host = host
        self.backlog = backlog
        self._serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._serv.bind((host, port))

    def __repr__(self):
        return f"Listener(port={self.port}, host={self.host}, backlog={self.backlog}"

    def start(self):
        self._serv.listen(self.backlog)

    def stop(self):
        self._serv.close()

    def accept(self):
        connection = Connection(self._serv)
        return connection

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.stop()

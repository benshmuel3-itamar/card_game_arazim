import socket
import struct


class Connection:
    def __init__(self, connection: socket.socket):
        self._connection = connection

    def __repr__(self):
        return str(self._connection)

    def send_message(self, message: bytes):
        header = struct.pack(">I", len(message))
        self._connection.send(header + message)

    def receive_message(self):
        """
        recieves data from one client. the data comes with a header (it's length)
        """
        try:
            message = ""
            header = ""
            while len(header) < 4:
                data = self._connection.recv(1)
                header += data.decode()
            message_length = struct.unpack(">I", header.encode())[0]
            while len(message) < message_length:
                data = self._connection.recv(message_length - len(message))
                message += data.decode()
            self._connection.close()
        except Exception as error:
            print(f"ERROR: {error}")
        return message

    @classmethod
    def connect(cls, host, port):
        connection = Connection(socket.create_connection((host, port)))
        return connection

    def close(self):
        self._connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

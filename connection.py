import socket
import struct
import traceback


class Connection:
    def __init__(self, connection: socket.socket = 0):
        if connection == 0:
            return
        self._connection = connection
        self._conn, _ = self._connection.accept()

    def __repr__(self):
        return str(self._connection)

    def send_message(self, message: bytes):
        header = struct.pack(">I", len(message))
        self._conn.send(header + message)

    def receive_message(self):
        """
        recieves data from one client. the data comes with a header (it's length)
        """
        try:
            message = b""
            header = ""
            while len(header) < 4:
                data = self._conn.recv(1)
                header += data.decode()
            message_length = struct.unpack(">I", header.encode())[0]
            while len(message) < message_length:
                data = self._conn.recv(message_length - len(message))
                message += data
            message = message.decode()
            self._conn.close()
        except Exception as error:
            print(f"ERROR: {error}")
            traceback.print_exc()
        return message

    @classmethod
    def connect(cls, host, port):
        connection = Connection()
        connection._conn = socket.create_connection((host, port))
        return connection

    def close(self):
        self._conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

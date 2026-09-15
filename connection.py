import socket
import struct
import traceback


class Connection:
    def __init__(self, connection: socket.socket):
        self._connection = connection

    def __repr__(self) -> str:
        return str(self._connection)

    def send_message(self, message: bytes) -> None:
        header = struct.pack("<I", len(message))
        self._connection.send(header + message)

    def receive_message(self) -> str:
        """
        recieves data from one client. the data comes with a header (it's length)
        """
        try:
            message = b""
            header = ""
            while len(header) < 4:
                data = self._connection.recv(4 - len(header))
                header += data.decode()
            message_length = struct.unpack("<I", header.encode())[0]
            while len(message) < message_length:
                data = self._connection.recv(message_length - len(message))
                message += data
            message = message.decode()
            self._connection.close()
        except Exception as error:
            print(f"ERROR: {error}")
            traceback.print_exc()
        return message

    @classmethod
    def connect(cls, host, port):
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.connect((host, port))
        return Connection(my_socket)

    def close(self):
        self._connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

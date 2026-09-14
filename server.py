import argparse
import socket
import struct
import sys
import threading

###########################################################
####################### YOUR CODE #########################
###########################################################
BACKLOG = 100


def recv_data(conn):
    """
    recieves data from one client. the data comes with a header (it's length)
    """
    try:
        message = ""
        header = ""
        while len(header) < 4:
            data = conn.recv(1)
            header += data.decode()
        message_length = struct.unpack(">I", header.encode())[0]
        while len(message) < message_length:
            data = conn.recv(message_length - len(message))
            message += data.decode()
        conn.close()
        print(f"Recieved data: {message}")
    except Exception as error:
        print(f"ERROR: {error}")


def make_socket(args):
    """creates a new docket' listening on the specified port"""
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind((args.server_ip, args.server_port))
    serv.listen(BACKLOG)
    return serv


def get_args():
    parser = argparse.ArgumentParser(description="Send data to server.")
    parser.add_argument("server_ip", type=str, help="the server's ip")
    parser.add_argument("server_port", type=int, help="the server's port")
    return parser.parse_args()


def main():
    """
    Implementation of CLI and recieving data.
    """
    args = get_args()
    try:
        serv = make_socket(args)
        while True:
            conn, _ = serv.accept()
            t = threading.Thread(target=recv_data, args=(conn,))
            t.start()
    except Exception as error:
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

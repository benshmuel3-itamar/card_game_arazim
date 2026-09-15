import argparse
import sys
import threading
import traceback

from card import Card
from connection import Connection
from listener import Listener

###########################################################
####################### YOUR CODE #########################
###########################################################
BACKLOG = 100


def recv_data(connection: Connection):
    """
    recieves data from one client. the data comes with a header (it's length)
    """
    with connection:
        my_message = connection.receive_message()
        my_card = Card.deserialize(my_message)
        print(f"Received card '{my_card.name}' by {my_card.creator}")
        my_card.image.image.show()
        return my_card


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
        with Listener(args.server_port, args.server_ip) as listener:
            while True:
                connection = listener.accept()
                t = threading.Thread(target=recv_data, args=(connection,))
                t.start()
    except Exception as error:
        print(f"ERROR: {error}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

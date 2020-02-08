import socket
import threading
import sys

HOST = '18.195.107.195'
PORT = 5378
BUFFER = 4096


class Client:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        self.connect()

        # login

        # send & receive
        while True:
            thread_send = threading.Thread(target=self.send)
            thread_send.start()

            thread_receive = threading.Thread(target=self.receive)
            thread_receive.start()

        # disconnect

    def send(self):
        string_bytes = sys.stdin.readline().encode("utf-8")
        self.sock.send(string_bytes)

    def receive(self):
        data = self.sock.recv(BUFFER)

        if not data:
            print("Socket is closed.")
            # FIXME if user exists, print is executed endlessly
        else:
            print(data.decode("utf-8"))

    def login(self):
        pass

    def connect(self):
        try:
            self.sock.connect((HOST, PORT))
        except:
            print('Cannot establish connection. Aborting.')
            sys.exit()

        print('Connected to remote host.')

    def disconnect(self):
        self.sock.close()


client = Client()

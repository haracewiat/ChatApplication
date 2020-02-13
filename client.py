#!/usr/bin/env python

"""
    Client side script to allow communication with the server.

    The program recognizes the following commands:
        !who    : returns a list of available users
        !quit   : quits the connection

    To send a message, type:
        @<username> <message>

    To login, simply type the chosen username:
        <username>

"""

import socket
import threading
import sys
from api import parser

HOST = '18.195.107.195'
PORT = 5378
BUFFER = 4096


class Client:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    messages = []
    sent = False
    connected = True

    def __init__(self):

        # Connect to the host
        self.connect()

        # Send and receive messages
        thread_receive = threading.Thread(target=self.receive)
        thread_receive.start()

        self.send()

        # Disconnect
        self.disconnect(thread_receive)

    def receive(self):

        message = b''

        while True:
            data = self.sock.recv(BUFFER)

            if not data:
                print('Closed connection with the server.')
                break

            message += data

            if message[-1] == 10:
                print(parser.decode(message))
                message = b''

    def send(self):
        while True:
            message = parser.encode(input())

            if message == b'QUIT\n':
                return

            self.sock.sendall(message)

    def connect(self):
        try:
            self.sock.connect((HOST, PORT))
        except:
            print("Cannot establish connection. Aborting.")
            sys.exit()

        print("Connected to remote host.")

    def disconnect(self, thread):
        self.sock.shutdown(1)
        thread.join()
        self.sock.close()
        print("Disconnected.")
        sys.exit()


client = Client()

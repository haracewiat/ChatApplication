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
from api import parser, util

HOST = '18.195.107.195'
PORT = 5378
BUFFER = 4096


class Client:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
                break

            message += data

            if util.is_eol(message):
                self.handle_receive(message)
                message = b''

    def handle_receive(self, message):

        # Print the decoded message
        print(parser.decode(message))

        # Handle special cases
        if util.causes_disconnection(message):
            self.reconnect()

    def send(self):
        while True:
            message = parser.encode(input())

            if message == b'QUIT\n':
                return

            if message != b'INVALID\n':
                self.sock.sendall(message)

    def connect(self):
        try:
            self.sock.connect((HOST, PORT))
        except:
            print("Cannot establish connection. Aborting.")
            sys.exit()

        print("Connected to remote host.")

    def reconnect(self):
        print('Connection lost. Trying to reconnect...')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def disconnect(self, thread):
        self.sock.shutdown(1)
        thread.join()
        self.sock.close()
        print("Disconnected.")
        sys.exit()


client = Client()

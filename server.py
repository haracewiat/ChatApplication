#!/usr/bin/env python

"""
    Server side script to allow communication with the server.

    To connect to the server, run the script first and connect
    with a client to:
        HOST: 127.0.0.1
        PORT: 5378


    1. socket
    2. bind
    3. listen
    4. accept (blocks)
    5. receive (blocks)
    6. send
    7. close

"""

import socket
import threading
import time
import sys
import modules.server.parser as parser
import modules.server.util as util


HOST = '127.0.0.1'
PORT = 5378
NO_CONNECTIONS = 64
BUFFER = 4096


class Server:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CONNECTIONS = []

    def __init__(self):

        # Bind
        self.sock.bind((HOST, PORT))

        # Listen for incoming connections
        self.sock.listen(NO_CONNECTIONS)

        # Start threads for accepting and handling connections
        thread_accept_connections = threading.Thread(
            target=self.accept_connections)
        thread_accept_connections.start()

        thread_receive = threading.Thread(
            target=self.receive)
        thread_receive.start()

        self.broadcast()

    def accept_connections(self):
        while True:
            connection, address = self.sock.accept()
            # login
            self.CONNECTIONS.append(connection)

            # Start a send/receive thread for the new connection
            # thread_handle_connection = threading.Thread(
            #    target=self.handle_connection(connection))
            # thread_handle_connection.start()

    def handle_connection(self, connection):
        while True:
            pass

    def receive(self):
        message = b''

        while True:
            for connection in self.CONNECTIONS:
                data = connection.recv(BUFFER)

                if not data:
                    break

                message += data

                if util.is_eol(message):
                    self.respond(message, connection)
                    message = b''

    def respond(self, message, connection):
        connection.sendall(b'HELLO user\n')

    def broadcast(self):
        for connection in self.CONNECTIONS:
            connection.sendall(b'HELLO broadcast\n')

    def remove(self, connection):
        if connection in self.connections:
            self.CONNECTIONS.remove(connection)


server = Server()

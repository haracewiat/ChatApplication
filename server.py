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
import select
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
    USERS = []

    def __init__(self):

        # Bind
        self.sock.bind((HOST, PORT))
        self.CONNECTIONS.append(self.sock)

        # Listen for incoming connections
        self.sock.listen(NO_CONNECTIONS)

        # Start threads for accepting and handling connections
        while True:
            read_sockets, write_sockets, error_sockets = select.select(
                self.CONNECTIONS, [], [])

            for connection in read_sockets:
                print(len(self.CONNECTIONS))
                if connection == self.sock:
                    print('new connection!')
                    self.accept_connection()
                else:
                    print('reading from the socket...')
                    self.receive(connection)

        self.sock.close()

    def accept_connection(self):
        print('adding the new connection...')
        connection, address = self.sock.accept()
        self.CONNECTIONS.append(connection)

    def handle_connection(self, connection):
        while True:
            pass

    def receive(self, connection):
        message = b''

        while True:
            data = connection.recv(BUFFER)

            if data:
                message += data

                if util.is_eol(message):
                    self.respond(message, connection)
                    message = b''
                    return
            else:
                # If no data is received, the connection should be closed
                self.disconnect(connection)
                return

    def respond(self, message, connection):
        print(util.get_header(message))
        if util.get_header(message) == 'HELLO-FROM':
            connection.sendall(b'HELLO user\n')
        elif util.get_header(message) == 'WHO':
            connection.sendall(b'WHO-OK\n')
        elif util.get_header(message) == 'SEND':
            #self.send_message_to(util.get_message(message), connection, util.get_recipient(message))
            self.broadcast(util.get_message(message))

    def send_message_to(self, message, sender, recipient):
        print(message)
        print(sender)
        print(recipient)

    def broadcast(self, message):
        for connection in self.CONNECTIONS:
            if connection is not self.sock:
                connection.sendall(b'HELLO broadcast\n')

    def disconnect(self, connection):
        # if connection in self.CONNECTIONS:
        connection.close()
        self.CONNECTIONS.remove(connection)


server = Server()

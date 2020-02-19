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
    CONNECTIONS = dict()

    def __init__(self):

        # Bind
        self.sock.bind((HOST, PORT))
        self.CONNECTIONS['SERVER'] = self.sock

        # Listen for incoming connections
        self.sock.listen(NO_CONNECTIONS)

        # Start threads for accepting and handling connections
        while True:
            read_sockets, write_sockets, error_sockets = select.select(
                self.CONNECTIONS.values(), self.CONNECTIONS.values(), [])

            for connection in read_sockets:
                if connection == self.sock:
                    self.accept_connection()
                else:
                    self.receive(connection)

        self.sock.close()

    def accept_connection(self):
        connection, address = self.sock.accept()
        # FIXME add timeout for the handshake
        self.receive(connection)

    def register_user(self, username, connection):
        if username not in self.CONNECTIONS.keys():
            self.CONNECTIONS[username] = connection
            connection.sendall(bytes('HELLO ' + username + '\n', 'utf-8'))
        else:
            connection.sendall(b'IN-USE\n')

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
            self.register_user(util.get_username(message), connection)
        elif util.get_header(message) == 'WHO\n':
            connection.sendall(util.get_active_users(
                list(self.CONNECTIONS.keys())))
        elif util.get_header(message) == 'SEND':
            self.send_message_to(util.get_message(
                message), self.get_value(connection), util.get_recipient(message))

    def send_message_to(self, message, sender, recipient):
        if recipient not in self.CONNECTIONS.keys():
            sender.sendall(b'UNKNOWN\n')
        else:
            self.CONNECTIONS.get(sender).sendall(b'SEND-OK\n')
            text = 'DELIVERY ' + sender + ' ' + message
            self.CONNECTIONS.get(recipient).sendall(bytes(text, 'utf-8'))

    def broadcast(self, message):
        for connection in self.CONNECTIONS:
            if connection is not self.sock:
                connection.sendall(b'HELLO broadcast\n')

    def disconnect(self, connection):
        for key, value in self.CONNECTIONS.items():
            if value == connection:
                connection.close()

        del self.CONNECTIONS[key]

    def get_value(self, connection):
        for key, value in self.CONNECTIONS.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
            if value == connection:
                return key


server = Server()

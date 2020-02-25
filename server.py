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
                self.CONNECTIONS.values(), [], [])

            for connection in read_sockets:
                if connection == self.sock:
                    self.accept_connection()
                else:
                    self.receive(connection)

        self.sock.close()

    def accept_connection(self):
        connection, address = self.sock.accept()

        if len(self.CONNECTIONS) > NO_CONNECTIONS:
            connection.sendall(b'BUSY\n')
            return

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

                if util.contains_eol(message):
                    text = util.extract(message)
                    for t in text:
                        self.respond(bytes(t, 'utf-8'), connection)
                    message = util.remove(text, message)
                    return
            else:
                # If no data is received, the connection should be closed
                self.disconnect(connection)
                return

    def respond(self, message, connection):
        if self.get_value(connection) is None:
            self.handle_handshake(message, connection)
        else:
            if util.get_header(message) == 'WHO\n':
                self.handle_who(message, connection)
            elif util.get_header(message) == 'SEND':
                self.handle_send(message, connection)
            else:
                connection.sendall(b'BAD-RQST-HDR\n')
                self.disconnect(connection)

    def handle_handshake(self, message, connection):
        if util.get_header(message) == 'HELLO-FROM':
            if len(message.decode('utf-8').split(' ')) == 2:
                self.register_user(util.get_username(message), connection)
            else:
                connection.sendall(b'BAD-RQST-BODY\n')
                self.disconnect(connection)
        else:
            connection.sendall(b'BAD-RQST-HDR\n')
            self.disconnect(connection)

    def handle_send(self, message, connection):
        if len(message.decode('utf-8').split(' ')) > 2:
            if self.CONNECTIONS.get(util.get_recipient(message)) is None:
                connection.sendall(b'UNKNOWN\n')
            else:
                self.send_message_to(util.get_message(
                    message), self.get_value(connection), util.get_recipient(message))
        else:
            connection.sendall(b'BAD-RQST-BODY\n')
            self.disconnect(connection)

    def send_message_to(self, message, sender, recipient):
        if recipient not in self.CONNECTIONS.keys():
            sender.sendall(b'UNKNOWN\n')
        else:
            self.CONNECTIONS.get(sender).sendall(b'SEND-OK\n')
            text = 'DELIVERY ' + sender + ' ' + message
            self.CONNECTIONS.get(recipient).sendall(bytes(text, 'utf-8'))

    def handle_who(self, message, connection):
        if len(message.decode('utf-8').split(' ')) == 1:
            connection.sendall(util.get_active_users(
                list(self.CONNECTIONS.keys())))
        else:
            connection.sendall(b'BAD-RQST-BODY\n')
            self.disconnect(connection)

    def disconnect(self, connection):
        if self.get_value(connection) is not None:
            del self.CONNECTIONS[self.get_value(connection)]
        connection.close()

    def get_value(self, connection):
        for key, value in self.CONNECTIONS.items():
            if value == connection:
                return key
        return None


server = Server()

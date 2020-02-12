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
import time
from modules import parser as Parser

HOST = '18.195.107.195'
PORT = 5378
BUFFER = 4096


class Client:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    messages = []
    sent = False

    def __init__(self):

        # Connect to the host
        self.connect()

        # Send and receive messages
        thread_send = threading.Thread(target=self.send)
        thread_send.start()

        thread_receive = threading.Thread(target=self.receive, daemon=True)
        thread_receive.start()

        thread_handle_receive = threading.Thread(target=self.handle_receive)
        thread_handle_receive.start()

    def receive(self):
        while True:
            message = self.sock.recv(BUFFER)
            self.messages.append(message)
            # if message:
            #    self.handle_receive(message)

    def handle_receive(self):
        while True:

            if len(self.messages) > 0:
                message = self.messages[0]

               # Handle special cases
                if message == bytes('IN-USE\n', 'utf-8'):
                    self.sock = socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM)
                    self.connect()

                if message == bytes('SEND-OK\n', 'utf-8'):
                    self.sent = True

                if message[:6] == bytes('WHO-OK', 'utf-8'):
                    self.sent = True

                if message[:5] == bytes('HELLO', 'utf-8'):
                    self.sent = True

                # Print the decoded message
                print(Parser.decode(message))

                # Pop the message
                self.messages.remove(message)

    def send(self):
        while True:
            message = Parser.encode(input())
            self.handle_send(message)

            while not self.sent:
                time.sleep(1)

            self.sent = False

    def handle_send(self, message):
        # Handle special cases
        if message == bytes('QUIT\n', 'utf-8'):
            self.disconnect()

        if message == bytes('INVALID\n', 'utf-8'):
            return

        # Print the encoded message
        self.sock.sendall(message)

    def connect(self):
        try:
            self.sock.connect((HOST, PORT))
        except:
            print("Cannot establish connection. Aborting.")
            sys.exit()

        print("Connected to remote host.")

    def disconnect(self):
        self.sock.close()
        print("Disconnected.")
        sys.exit()


client = Client()

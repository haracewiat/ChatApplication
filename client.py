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

HOST = '18.195.107.195'
PORT = 5378
BUFFER = 4096


class Client:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):

        # Connect to the host
        self.connect()

        # Send and receive messages
        thread_send = threading.Thread(target=self.send)
        thread_send.start()

        thread_receive = threading.Thread(target=self.receive, daemon=True)
        thread_receive.start()

    def receive(self):
        while True:
            message = self.sock.recv(BUFFER)
            if message:
                self.handle_receive(message)

    def handle_receive(self, message):
        # Handle special cases
        if message == bytes('IN-USE\n', 'utf-8'):
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect()

        # Print the decoded message
        print(Parser.decode(message))

    def send(self):
        while True:
            message = Parser.encode(input())
            self.handle_send(message)

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


class Parser:

    def encode(message):
        '''
        Chat Application Protocol for the CLIENT side:
        <username>  : HELLO-FROM <username>
        @<username> : SEND <username> <message>
        !who        : WHO
        !quit       : QUIT
        '''

        # Case of an invalid message: don't send to the server
        if len(message) == 0:
            return bytes('INVALID\n', 'utf-8')

        switch = {
            '!': message[1:].upper() + '\n',
            '@': 'SEND ' + message[1:] + '\n'
        }

        translated_message = switch.get(
            message[0], 'HELLO-FROM ' + message + '\n')

        # Encode to utf-8
        encoded_message = translated_message.encode('utf-8')

        return encoded_message

    def decode(message):
        '''
        Chat Application Protocol for the SERVER side:
        HELLO           : Successfully logged in as <username>
        WHO-OK          : Available users: <username>, ...
        SEND-OK\n       : Sent successfully.
        UNKNOWN\n       : Username does not exist
        DELIVERY        : <username>: <message>
        IN-USE\n        : The username <username> is already taken.
        BUSY\n          : The total number of users is exceeded. Try later.
        BAD-RQST-HDR\n  : Unknown command. 
        BAD-RQST-BODY\n : Your message contains an error and cannot be sent.
        '''

        # Decode from utf-8 and seperate the words
        decoded_message = message.decode('utf-8')
        decoded_message = decoded_message.split(' ')
        argument = ['', '']

        if len(decoded_message) > 1:
            argument[0] = decoded_message[1]
        if len(decoded_message) > 2:
            argument[1] = decoded_message[2:]

        switch = {
            'HELLO': 'Successfully logged in as ' + argument[0],
            'WHO-OK': 'Available users: ' + argument[0],
            'SEND-OK\n': 'Sent successfully.',
            'UNKNOWN\n': 'Username does not exist',
            'DELIVERY':  argument[0] + ': ' + ' '.join(argument[1]),
            'IN-USE\n': 'The username ' + argument[0] + ' is already taken. Choose a different one.',
            'BUSY\n': 'The total number of users is exceeded. Try connecting later.',
            'BAD-RQST-HDR\n': 'Unknown command.',
            'BAD-RQST-BODY\n': 'Your message contains an error and cannot be sent.'
        }

        # Look for translation in the switch
        translated_message = switch.get(
            decoded_message[0], 'Unknown response.')

        return translated_message


client = Client()

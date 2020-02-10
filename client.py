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

        thread_receive = threading.Thread(target=self.receive)
        thread_receive.start()

    def receive(self):
        # FIXME should loop to allow another try
        while True:
            data = self.sock.recv(BUFFER)
            if not data:
                print("Socket is closed.")
                self.disconnect()
            else:
                print(Parser.decode(data))

    def send(self):
        # FIXME Why are the messages not sent? Wrong encoding?
        while True:
            message = Parser.encode(input())
            print(message, type(message))
            self.sock.sendall(message)

            '''
            message = input(f'{username} > ')
            '''

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

        # FIXME QUIT is not a message to the server but to the client class to call self.disconnect()!

        switch = {
            # anything that follows '!' is a command itself
            '!': message[1:].upper()  + '\n',
            # anything that follows '@' needs to be preceded with 'SEND '
            '@': 'SEND ' + message[1:] + '\n'
        }

        # Default (starts neither with '!' or '@'): must be first hand-shake (login)
        translated_message = switch.get(message[0], 'HELLO-FROM ' + message + '\n')

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

        print(decoded_message)

        # FIXME Strings have different lenght. Can't hardcode indexes like decoded_message[1],
        #       because SEND-OK has no index of 1 and it will throw an error.
        #       Find a way to go around this issue (index out of bounds) and replace the dynamic
        #       values.

        switch = {
            'HELLO': 'Successfully logged in as <username>',
            'WHO-OK': 'Available users: <username>, ...',
            'SEND-OK\n': 'Sent successfully.',
            'UNKNOWN\n': 'Username does not exist',
            'DELIVERY': '<username>: <message>',
            'IN-USE\n': 'The username <username> is already taken. Choose a different one.',
            'BUSY\n': 'The total number of users is exceeded. Try connecting later.',
            'BAD-RQST-HDR\n': 'Unknown command.',
            'BAD-RQST-BODY\n': 'Your message contains an error and cannot be sent.'
        }

        # Look for translation in the switch
        translated_message = switch.get(
            decoded_message[0], 'Unknown response.')

        return translated_message


client = Client()

# FIXME Why can't I exit with ctrl+c?
